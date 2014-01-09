# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('rna_tag')

        # Deleting model 'Channel'
        db.delete_table('rna_channel')

        # Deleting model 'Product'
        db.delete_table('rna_product')


    def backwards(self, orm):
        # Adding model 'Tag'
        db.create_table('rna_tag', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, db_index=True)),
            ('sort_num', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('rna', ['Tag'])

        # Adding model 'Channel'
        db.create_table('rna_channel', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('rna', ['Channel'])

        # Adding model 'Product'
        db.create_table('rna_product', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('rna', ['Product'])


    models = {
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
        }
    }

    complete_apps = ['rna']