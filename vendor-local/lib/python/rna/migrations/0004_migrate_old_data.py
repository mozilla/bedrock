# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        PRODUCTS = {
            'FIREFOX': 0,
            'FENNEC': 1,
            'ESR': 2,
        }

        CHANNELS = {
            'NIGHTLY': 0,
            'AURORA': 1,
            'BETA': 2,
            'RELEASE': 3,
        }

        TAGS = {
            'NEW': 0,
            'CHANGED': 1,
            'HTML5': 2,
            'FIXED': 3,
            'DEVELOPER': 4,
        }

        # Hard-coded product IDs. Sadface.
        DB_PRODUCTS = {
            1: PRODUCTS['FIREFOX'],
            2: PRODUCTS['FENNEC'],
            3: PRODUCTS['ESR'],
        }

        for release in orm.Release.objects.all():
            release.version_str = '{0}.0.{1}'.format(release.version, release.sub_version)

            if release.channel.name == 'ESR':
                release.product_num = PRODUCTS['ESR']
                release.channel_num = CHANNELS['RELEASE']
            else:
                release.product_num = DB_PRODUCTS[release.product.id]
                release.channel_num = CHANNELS[release.channel.name.upper()]
            release.save()

        for note in orm.Note.objects.all():
            if note.tag:
                note.tag_num = TAGS[note.tag.text.upper()]

            # Migrate to fixed_in_release
            if note.fixed_in_version:
                version = '{0}.0.{1}'.format(note.fixed_in_version, note.fixed_in_subversion or 0)
                filters = {'version_str': version}

                if note.fixed_in_channel:
                    if note.fixed_in_channel.name.upper() == 'ESR':
                        filters['product_num'] = PRODUCTS['ESR']
                        filters['channel_num'] = CHANNELS['RELEASE']
                    else:
                        filters['channel_num'] = CHANNELS[note.fixed_in_channel.name.upper()]

                        if note.product:
                            filters['product_num'] = DB_PRODUCTS[note.product.id]

                try:
                    note.fixed_in_release = orm.Release.objects.get(**filters)
                except (orm.Release.DoesNotExist, orm.Release.MultipleObjectsReturned):
                    note.fixed_in_release = None

            note.save()

    def backwards(self, orm):
        """No going backwards, as this migration is going to be deleted someday anyway."""


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
    symmetrical = True
