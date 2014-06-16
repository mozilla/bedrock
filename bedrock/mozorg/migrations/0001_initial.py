# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TwitterCache'
        db.create_table(u'mozorg_twittercache', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('tweets', self.gf('picklefield.fields.PickledObjectField')(default=[])),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'mozorg', ['TwitterCache'])


    def backwards(self, orm):
        # Deleting model 'TwitterCache'
        db.delete_table(u'mozorg_twittercache')


    models = {
        u'mozorg.twittercache': {
            'Meta': {'object_name': 'TwitterCache'},
            'account': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tweets': ('picklefield.fields.PickledObjectField', [], {'default': '[]'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        }
    }

    complete_apps = ['mozorg']