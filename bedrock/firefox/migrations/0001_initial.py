# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FirefoxOSFeedLink'
        db.create_table(u'firefox_firefoxosfeedlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=2000)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('locale', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
        ))
        db.send_create_signal(u'firefox', ['FirefoxOSFeedLink'])


    def backwards(self, orm):
        # Deleting model 'FirefoxOSFeedLink'
        db.delete_table(u'firefox_firefoxosfeedlink')


    models = {
        u'firefox.firefoxosfeedlink': {
            'Meta': {'object_name': 'FirefoxOSFeedLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '2000'}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        }
    }

    complete_apps = ['firefox']