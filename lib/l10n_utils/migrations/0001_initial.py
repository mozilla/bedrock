# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LangFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('locale', models.CharField(max_length=8, db_index=True)),
                ('translations', django_extensions.db.fields.json.JSONField()),
                ('tags', django_extensions.db.fields.json.JSONField(default=b'[]')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='langfile',
            unique_together=set([('name', 'locale')]),
        ),
    ]
