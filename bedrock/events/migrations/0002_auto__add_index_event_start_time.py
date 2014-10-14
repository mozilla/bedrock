# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Event', fields ['start_time']
        db.create_index(u'events_event', ['start_time'])


    def backwards(self, orm):
        # Removing index on 'Event', fields ['start_time']
        db.delete_index(u'events_event', ['start_time'])


    models = {
        u'events.event': {
            'Meta': {'ordering': "('start_time',)", 'object_name': 'Event'},
            'continent_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True', 'db_index': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'sequence': ('django.db.models.fields.SmallIntegerField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['events']