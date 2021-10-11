# -*- coding: utf-8 -*-
import django_extensions.db.fields.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(help_text=b'The ID for the newsletter that will be used by clients', unique=True)),
                ('data', django_extensions.db.fields.json.JSONField()),
            ],
        ),
    ]
