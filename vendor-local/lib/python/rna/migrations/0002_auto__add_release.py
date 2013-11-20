# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Release'
        db.create_table('rna_release', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rna.Product'])),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rna.Channel'])),
            ('version', self.gf('django.db.models.fields.IntegerField')()),
            ('sub_version', self.gf('django.db.models.fields.IntegerField')()),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('rna', ['Release'])


    def backwards(self, orm):
        # Deleting model 'Release'
        db.delete_table('rna_release')


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
            'fixed_in_subversion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fixed_in_version': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rna.Product']", 'null': 'True', 'blank': 'True'}),
            'sort_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rna.Tag']", 'null': 'True', 'blank': 'True'})
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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rna.Product']"}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'sub_version': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {})
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