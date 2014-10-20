# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.on_homepage'
        db.add_column(u'openstandard_article', 'on_homepage',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True),
                      keep_default=False)


        # Changing field 'Article.link'
        db.alter_column(u'openstandard_article', 'link', self.gf('django.db.models.fields.URLField')(max_length=2000))
        # Adding index on 'Article', fields ['link']
        db.create_index(u'openstandard_article', ['link'])


    def backwards(self, orm):
        # Removing index on 'Article', fields ['link']
        db.delete_index(u'openstandard_article', ['link'])

        # Deleting field 'Article.on_homepage'
        db.delete_column(u'openstandard_article', 'on_homepage')


        # Changing field 'Article.link'
        db.alter_column(u'openstandard_article', 'link', self.gf('django.db.models.fields.CharField')(max_length=2000))

    models = {
        u'openstandard.article': {
            'Meta': {'object_name': 'Article'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['openstandard.ArticleImage']", 'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'db_index': 'True'}),
            'on_homepage': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
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