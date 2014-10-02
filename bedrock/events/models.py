# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from django.db import models
from django.db.models.query import QuerySet

from icalendar import Calendar

from bedrock.events.countries import country_to_continent


class EventQuerySet(QuerySet):
    def future_count(self):
        return self.future().count()

    def future(self):
        return self.filter(start_time__gt=datetime.utcnow()).order_by('start_time')


class EventManager(models.Manager):
    def get_query_set(self):
        return EventQuerySet(self.model, using=self._db)

    def next_upcoming(self, count=1):
        return self.get_query_set().next_upcoming(count)

    def sync_with_ical(self, ical_feed):
        """
        Parse an icalendar feed and sync the events in the database with it.

        :param ical_feed: ical formatted string.
        :return: None
        """
        cal = Calendar.from_ical(ical_feed)
        current_uids = self.values_list('id', flat=True)
        new_uids = []
        for event in cal.walk('vevent'):
            uid = event.decoded('uid')
            sequence = event.decoded('sequence')
            new_uids.append(uid)
            try:
                event_obj = self.get(id=uid)
                if event_obj and event_obj.sequence == sequence:
                    continue
            except Event.DoesNotExist:
                event_obj = Event()

            event_obj.update_from_ical(event)
            event_obj.save()

        to_delete = set(current_uids) - set(new_uids)
        self.filter(id__in=list(to_delete)).delete()


class Event(models.Model):
    id = models.CharField(max_length=40, primary_key=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    sequence = models.SmallIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    url = models.URLField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    country_code = models.CharField(max_length=2)
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

    class Meta:
        ordering = ('start_time',)

    def __unicode__(self):
        return self.title

    def update_from_ical(self, ical_event):
        for field, ical_prop in self.field_to_ical.iteritems():
            setattr(self, field, ical_event.decoded(ical_prop))

    def save(self, *args, **kwargs):
        self.country_code = self.country_code.upper()
        self.continent_code = country_to_continent.get(self.country_code, None)
        super(Event, self).save(*args, **kwargs)
