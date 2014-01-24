# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from django.db import models
from django_extensions.db.fields import CreationDateTimeField


class TimeStampedModel(models.Model):
    """
    Replacement for django_extensions.db.models.TimeStampedModel
    that updates the modified timestamp by default, but allows
    that behavior to be overridden by passing a modified=False
    parameter to the save method
    """
    created = CreationDateTimeField()
    modified = models.DateTimeField(editable=False, blank=True, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if kwargs.pop('modified', True):
            self.modified = datetime.now()
        super(TimeStampedModel, self).save(*args, **kwargs)


class Release(TimeStampedModel):
    CHANNELS = [(x, x) for x in ('Nightly', 'Aurora', 'Beta', 'Release')]
    PRODUCTS = [(x, x) for x in
                ('Firefox', 'Firefox for Android',
                 'Firefox Extended Support Release', 'Firefox OS')]

    product = models.CharField(max_length=255, choices=PRODUCTS)
    channel = models.CharField(max_length=255, choices=CHANNELS)
    version = models.CharField(max_length=255)
    release_date = models.DateTimeField()
    text = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    bug_list = models.TextField(blank=True)
    bug_search_url = models.CharField(max_length=2000, blank=True)
    system_requirements = models.TextField(blank=True)

    def notes(self):
        """
        Retrieve a list of Note instances that should be shown for this
        release, grouped as either new features or known issues.
        """
        notes = self.note_set.all()

        new_features = (note for note in notes if
                        not note.is_known_issue_for(self))
        known_issues = (note for note in notes if
                        note.is_known_issue_for(self))

        return new_features, known_issues

    def __unicode__(self):
        return '{product} v{version} {channel}'.format(
            product=self.product, version=self.version, channel=self.channel)

    class Meta:
        #TODO: see if this has a significant performance impact
        ordering = ('product', '-version', 'channel')


class Note(TimeStampedModel):
    TAGS = [(x, x) for x in ('New', 'Changed', 'HTML5', 'Fixed', 'Developer')]

    bug = models.IntegerField(null=True, blank=True)
    html = models.TextField(blank=True)
    releases = models.ManyToManyField(Release, blank=True)
    is_known_issue = models.BooleanField(default=False)
    fixed_in_release = models.ForeignKey(Release, null=True, blank=True,
                                         related_name='fixed_note_set')
    tag = models.CharField(max_length=255, blank=True, choices=TAGS)
    sort_num = models.IntegerField(null=True, blank=True)

    def is_known_issue_for(self, release):
        return self.is_known_issue and self.fixed_in_release != release

    class Meta:
        ordering = ('sort_num',)

    def __unicode__(self):
        return self.html
