# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0004_mitrecve'),
    ]

    operations = [
        migrations.AddField(
            model_name='mitrecve',
            name='mfsa_ids',
            field=django_extensions.db.fields.json.JSONField(default=b'[]'),
        ),
    ]
