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


class Channel(TimeStampedModel):
    name = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(unique=True, max_length=255)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Tag(TimeStampedModel):
    text = models.TextField()
    sort_num = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('sort_num',)

    def __unicode__(self):
        return self.text


class Note(TimeStampedModel):
    bug = models.IntegerField(null=True, blank=True)
    html = models.TextField(blank=True)
    first_version = models.IntegerField(null=True, blank=True)
    first_channel = models.ForeignKey(
        Channel, null=True, blank=True, related_name='first_channel_notes')
    fixed_in_version = models.IntegerField(null=True, blank=True)
    fixed_in_channel = models.ForeignKey(
        Channel, null=True, blank=True, related_name='fixed_in_channel_notes')
    tag = models.ForeignKey(Tag, null=True, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True)
    sort_num = models.IntegerField(null=True, blank=True)
    fixed_in_subversion = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('sort_num',)

    def __unicode__(self):
        return self.html


class Release(TimeStampedModel):
    product = models.ForeignKey(Product)
    channel = models.ForeignKey(Channel)
    version = models.IntegerField()
    sub_version = models.IntegerField()
    release_date = models.DateTimeField()
    text = models.TextField(blank=True)

    def __unicode__(self):
        return self.text
