# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table(u'security_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('product', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('product_slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'security', ['Product'])

        # Adding model 'SecurityAdvisory'
        db.create_table(u'security_securityadvisory', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=8, primary_key=True, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('impact', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('reporter', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('announced', self.gf('django.db.models.fields.DateField')(null=True)),
            ('year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('extra_data', self.gf('django.db.models.fields.TextField')(default='{}')),
            ('html', self.gf('django.db.models.fields.TextField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'security', ['SecurityAdvisory'])

        # Adding M2M table for field fixed_in on 'SecurityAdvisory'
        m2m_table_name = db.shorten_name(u'security_securityadvisory_fixed_in')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('securityadvisory', models.ForeignKey(orm[u'security.securityadvisory'], null=False)),
            ('product', models.ForeignKey(orm[u'security.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['securityadvisory_id', 'product_id'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table(u'security_product')

        # Deleting model 'SecurityAdvisory'
        db.delete_table(u'security_securityadvisory')

        # Removing M2M table for field fixed_in on 'SecurityAdvisory'
        db.delete_table(db.shorten_name(u'security_securityadvisory_fixed_in'))


    models = {
        u'security.product': {
            'Meta': {'ordering': "('slug',)", 'object_name': 'Product'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'product_slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'security.securityadvisory': {
            'Meta': {'ordering': "('-year', '-order')", 'object_name': 'SecurityAdvisory'},
            'announced': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'extra_data': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'fixed_in': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'advisories'", 'symmetrical': 'False', 'to': u"orm['security.Product']"}),
            'html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True', 'db_index': 'True'}),
            'impact': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {}),
            'reporter': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['security']