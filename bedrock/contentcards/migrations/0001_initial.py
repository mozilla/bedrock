# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContentCard',
            fields=[
                ('id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('card_name', models.CharField(max_length=100)),
                ('page_name', models.CharField(max_length=100)),
                ('locale', models.CharField(max_length=10)),
                ('content', models.TextField(blank=True)),
                ('data', django_extensions.db.fields.json.JSONField()),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
