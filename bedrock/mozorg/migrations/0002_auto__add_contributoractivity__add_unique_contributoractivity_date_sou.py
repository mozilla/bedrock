# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContributorActivity'
        db.create_table(u'mozorg_contributoractivity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('source_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('team_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
            ('new', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mozorg', ['ContributorActivity'])

        # Adding unique constraint on 'ContributorActivity', fields ['date', 'source_name', 'team_name']
        db.create_unique(u'mozorg_contributoractivity', ['date', 'source_name', 'team_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'ContributorActivity', fields ['date', 'source_name', 'team_name']
        db.delete_unique(u'mozorg_contributoractivity', ['date', 'source_name', 'team_name'])

        # Deleting model 'ContributorActivity'
        db.delete_table(u'mozorg_contributoractivity')


    models = {
        u'mozorg.contributoractivity': {
            'Meta': {'ordering': "['-date']", 'unique_together': "(('date', 'source_name', 'team_name'),)", 'object_name': 'ContributorActivity'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new': ('django.db.models.fields.IntegerField', [], {}),
            'source_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'total': ('django.db.models.fields.IntegerField', [], {})
        },
        u'mozorg.twittercache': {
            'Meta': {'object_name': 'TwitterCache'},
            'account': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tweets': ('picklefield.fields.PickledObjectField', [], {'default': '[]'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        }
    }

    complete_apps = ['mozorg']