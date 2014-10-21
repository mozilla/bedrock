# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.sponsored'
        db.add_column(u'openstandard_article', 'sponsored',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Article.sponsored'
        db.delete_column(u'openstandard_article', 'sponsored')


    models = {
        u'openstandard.article': {
            'Meta': {'object_name': 'Article'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openstandard.ArticleImage']", 'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '2000'}),
            'on_homepage': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'sponsored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        u'openstandard.articleimage': {
            'Meta': {'object_name': 'ArticleImage'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        }
    }

    complete_apps = ['openstandard']