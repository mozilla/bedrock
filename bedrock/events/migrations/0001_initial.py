# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'events_event', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sequence', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('continent_code', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
        ))
        db.send_create_signal(u'events', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'events_event')


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
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['events']