# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from builtins import object
from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet

from icalendar import Calendar
from pytz import timezone

from bedrock.events.countries import country_to_continent


def calendar_id_from_google_url(feed_url):
    return feed_url.split('/')[5]


def calendar_url_for_event(event, calendar_id):
    template = 'https://www.google.com/calendar/embed?showCalendars=0&mode=week&wkst=1&' \
               'src={calendar_id}&ctz=America/Los_Angeles&' \
               'dates={event.start_time:%Y%m%d}%2f{event.end_time:%Y%m%d}'
    return template.format(calendar_id=calendar_id, event=event)


def utcnow():
    if settings.USE_TZ:
        # We have to be sure to use a tz-aware datetime because otherwise
        # it will be converted using django.utils.timezone.make_aware, which
        # will throw an error during DST change, because Zen.
        # https://code.djangoproject.com/ticket/22598
        return timezone('UTC').localize(datetime.utcnow())

    return datetime.utcnow()


class EventQuerySet(QuerySet):
    def future(self):
        return self.filter(start_time__gt=utcnow()).order_by('start_time')

    def past(self):
        return self.filter(end_time__lte=utcnow()).order_by('end_time')

    def current_and_future(self):
        return self.filter(end_time__gt=utcnow()).order_by('start_time')


class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def future(self):
        return self.get_queryset().future()

    def past(self):
        return self.get_queryset().past()

    def current_and_future(self):
        return self.get_queryset().current_and_future()

    def sync_with_ical(self, ical_feed, feed_url):
        """
        Parse an icalendar feed and sync the events in the database with it.

        :param ical_feed: ical formatted string.
        :return: None
        """
        today = utcnow().date()
        cal = Calendar.from_ical(ical_feed)
        for event in cal.walk('vevent'):
            uid = event.decoded('uid')
            sequence = event.decoded('sequence')
            try:
                event_obj = self.get(id=uid)
                if event_obj and event_obj.sequence == sequence:
                    continue
            except Event.DoesNotExist:
                event_obj = Event()

            event_obj.update_from_ical(event)
            end_date = event_obj.end_time
            if isinstance(end_date, datetime):
                # use date since some feeds only produce date objects
                end_date = end_date.date()

            if today > end_date:
                continue

            if not event_obj.url and 'google.com' in feed_url:
                event_obj.url = calendar_url_for_event(event_obj,
                                                       calendar_id_from_google_url(feed_url))

            event_obj.save()


class Event(models.Model):
    id = models.CharField(max_length=40, primary_key=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    sequence = models.SmallIntegerField()
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField()
    url = models.URLField(blank=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    country_code = models.CharField(max_length=2, blank=True)
    continent_code = models.CharField(max_length=2, null=True)

    objects = EventManager()

    field_to_ical = {
        'id': 'uid',
        'title': 'summary',
        'description': 'description',
        'location': 'location',
        'sequence': 'sequence',
        'start_time': 'dtstart',
        'end_time': 'dtend',
        'url': 'url',
        'latitude': 'x-coordinates-lat',
        'longitude': 'x-coordinates-lon',
        'country_code': 'x-country-code',
    }

    class Meta(object):
        ordering = ('start_time',)

    def __unicode__(self):
        return self.title

    @property
    def day_of_month(self):
        return self.start_time.strftime('%d')

    @property
    def month_abbr(self):
        """Return the abbreviated month name with the abbr html tag."""
        # for l10n, the abbreviated month strings include the tag
        return u'<abbr>{0:%b}</abbr>'.format(self.start_time)

    def update_from_ical(self, ical_event):
        for field, ical_prop in self.field_to_ical.items():
            try:
                value = ical_event.decoded(ical_prop)
            except KeyError:
                pass
            else:
                if isinstance(value, str):
                    value = value.strip()
                setattr(self, field, value)

    def save(self, *args, **kwargs):
        self.country_code = self.country_code.upper()
        self.continent_code = country_to_continent.get(self.country_code, None)
        super(Event, self).save(*args, **kwargs)
