# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArticleImage'
        db.create_table(u'openstandard_articleimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('local_path', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal(u'openstandard', ['ArticleImage'])

        # Adding model 'Article'
        db.create_table(u'openstandard_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openstandard.ArticleImage'], null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('published', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'openstandard', ['Article'])


    def backwards(self, orm):
        # Deleting model 'ArticleImage'
        db.delete_table(u'openstandard_articleimage')

        # Deleting model 'Article'
        db.delete_table(u'openstandard_article')


    models = {
        u'openstandard.article': {
            'Meta': {'object_name': 'Article'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openstandard.ArticleImage']", 'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        u'openstandard.articleimage': {
            'Meta': {'object_name': 'ArticleImage'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_path': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        }
    }

    complete_apps = ['openstandard']