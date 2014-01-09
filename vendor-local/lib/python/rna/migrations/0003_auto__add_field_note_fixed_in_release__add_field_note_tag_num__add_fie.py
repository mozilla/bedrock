# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Note.fixed_in_release'
        db.add_column('rna_note', 'fixed_in_release',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fixed_note_set', null=True, to=orm['rna.Release']),
                      keep_default=False)

        # Adding field 'Note.tag_num'
        db.add_column('rna_note', 'tag_num',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding M2M table for field releases on 'Note'
        m2m_table_name = db.shorten_name('rna_note_releases')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('note', models.ForeignKey(orm['rna.note'], null=False)),
            ('release', models.ForeignKey(orm['rna.release'], null=False))
        ))
        db.create_unique(m2m_table_name, ['note_id', 'release_id'])

        # Adding field 'Release.product_num'
        db.add_column('rna_release', 'product_num',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Release.channel_num'
        db.add_column('rna_release', 'channel_num',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Release.version_str'
        db.add_column('rna_release', 'version_str',
                      self.gf('django.db.models.fields.CharField')(default='1.0', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Note.fixed_in_release'
        db.delete_column('rna_note', 'fixed_in_release_id')

        # Deleting field 'Note.tag_num'
        db.delete_column('rna_note', 'tag_num')

        # Removing M2M table for field releases on 'Note'
        db.delete_table(db.shorten_name('rna_note_releases'))

        # Deleting field 'Release.product_num'
        db.delete_column('rna_release', 'product_num')

        # Deleting field 'Release.channel_num'
        db.delete_column('rna_release', 'channel_num')

        # Deleting field 'Release.version_str'
        db.delete_column('rna_release', 'version_str')


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
            'first_channel': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'first_channel_notes'", 'null': 'True', 'to': "orm['rna.Channel']"}),
            'first_version': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fixed_in_channel': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'fixed_in_channel_notes'", 'null': 'True', 'to': "orm['rna.Channel']"}),
            'fixed_in_release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fixed_note_set'", 'null': 'True', 'to': "orm['rna.Release']"}),
            'fixed_in_subversion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fixed_in_version': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rna.Product']", 'null': 'True', 'blank': 'True'}),
            'releases': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rna.Release']", 'symmetrical': 'False'}),
            'sort_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rna.Tag']", 'null': 'True', 'blank': 'True'}),
            'tag_num': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
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
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rna.Channel']"}),
            'channel_num': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rna.Product']"}),
            'product_num': ('django.db.models.fields.IntegerField', [], {}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'sub_version': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {}),
            'version_str': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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