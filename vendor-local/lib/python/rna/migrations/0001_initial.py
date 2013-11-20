# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Channel'
        db.create_table('rna_channel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('rna', ['Channel'])

        # Adding model 'Product'
        db.create_table('rna_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('rna', ['Product'])

        # Adding model 'Tag'
        db.create_table('rna_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('sort_num', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('rna', ['Tag'])

        # Adding model 'Note'
        db.create_table('rna_note', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(db_index=True, blank=True)),
            ('bug', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('first_version', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('first_channel', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='first_channel_notes', null=True, to=orm['rna.Channel'])),
            ('fixed_in_version', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('fixed_in_channel', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='fixed_in_channel_notes', null=True, to=orm['rna.Channel'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rna.Tag'], null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rna.Product'], null=True, blank=True)),
            ('sort_num', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('fixed_in_subversion', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('rna', ['Note'])


    def backwards(self, orm):
        # Deleting model 'Channel'
        db.delete_table('rna_channel')

        # Deleting model 'Product'
        db.delete_table('rna_product')

        # Deleting model 'Tag'
        db.delete_table('rna_tag')

        # Deleting model 'Note'
        db.delete_table('rna_note')


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