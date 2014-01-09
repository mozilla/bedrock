# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Note.first_version'
        db.delete_column('rna_note', 'first_version')

        # Deleting field 'Note.first_channel'
        db.delete_column('rna_note', 'first_channel_id')

        # Deleting field 'Note.fixed_in_version'
        db.delete_column('rna_note', 'fixed_in_version')

        # Deleting field 'Note.fixed_in_subversion'
        db.delete_column('rna_note', 'fixed_in_subversion')

        # Deleting field 'Note.product'
        db.delete_column('rna_note', 'product_id')

        # Deleting field 'Note.fixed_in_channel'
        db.delete_column('rna_note', 'fixed_in_channel_id')

        # Deleting field 'Note.tag_id'
        db.delete_column('rna_note', 'tag_id')

        # Renaming column for 'Note.tag_num'.
        db.rename_column('rna_note', 'tag_num', 'tag')

        # Deleting field 'Release.sub_version'
        db.delete_column('rna_release', 'sub_version')

        # Deleting field 'Release.channel_id'
        db.delete_column('rna_release', 'channel_id')

        # Deleting field 'Release.product_num'
        db.delete_column('rna_release', 'product_id')

        # Deleting field 'Release.version_str'
        db.delete_column('rna_release', 'version')

        # Renaming column for 'Release.product_str'.
        db.rename_column('rna_release', 'product_num', 'product')

        # Renaming column for 'Release.version_str'.
        db.rename_column('rna_release', 'version_str', 'version')

        # Renaming column for 'Release.channel_num'.
        db.rename_column('rna_release', 'channel_num', 'channel')


    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        'rna.channel': {
            'Meta': {'object_name': 'Channel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'rna.note': {
            'Meta': {'ordering': "('sort_num',)", 'object_name': 'Note'},
            'bug': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'fixed_in_release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fixed_note_set'", 'null': 'True', 'to': "orm['rna.Release']"}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'releases': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rna.Release']", 'symmetrical': 'False'}),
            'sort_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'rna.product': {
            'Meta': {'object_name': 'Product'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'rna.release': {
            'Meta': {'object_name': 'Release'},
            'channel': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.IntegerField', [], {}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'rna.tag': {
            'Meta': {'ordering': "('sort_num',)", 'object_name': 'Tag'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'sort_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['rna']
