# -*- coding: utf-8 -*-
import django_extensions.db.fields.json
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0004_mitrecve'),
    ]

    operations = [
        migrations.AddField(
            model_name='mitrecve',
            name='mfsa_ids',
            field=django_extensions.db.fields.json.JSONField(default='[]'),
        ),
    ]
