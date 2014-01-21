# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Note.tag'
        db.alter_column('rna_note', 'tag', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Release.product'
        db.alter_column('rna_release', 'product', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Release.channel'
        db.alter_column('rna_release', 'channel', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):

        # Changing field 'Note.tag'
        db.alter_column('rna_note', 'tag', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Release.product'
        db.alter_column('rna_release', 'product', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Release.channel'
        db.alter_column('rna_release', 'channel', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'rna.note': {
            'Meta': {'ordering': "('sort_num',)", 'object_name': 'Note'},
            'bug': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'fixed_in_release': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fixed_note_set'", 'null': 'True', 'to': "orm['rna.Release']"}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_known_issue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'releases': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rna.Release']", 'symmetrical': 'False', 'blank': 'True'}),
            'sort_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'rna.release': {
            'Meta': {'ordering': "('product', '-version', 'channel')", 'object_name': 'Release'},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['rna']