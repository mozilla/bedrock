# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import django.utils.timezone
from django.db import migrations, models

import django_extensions.db.fields
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(unique=True, max_length=50)),
                ("slug", models.CharField(max_length=50, db_index=True)),
                ("product", models.CharField(max_length=50)),
                ("product_slug", models.SlugField()),
            ],
            options={
                "ordering": ("slug",),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="SecurityAdvisory",
            fields=[
                ("id", models.CharField(max_length=8, serialize=False, primary_key=True, db_index=True)),
                ("title", models.CharField(max_length=200)),
                ("impact", models.CharField(max_length=100)),
                ("reporter", models.CharField(max_length=100, null=True)),
                ("announced", models.DateField(null=True)),
                ("year", models.SmallIntegerField()),
                ("order", models.SmallIntegerField()),
                ("extra_data", django_extensions.db.fields.json.JSONField()),
                ("html", models.TextField()),
                (
                    "last_modified",
                    django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True),
                ),
                ("fixed_in", models.ManyToManyField(related_name="advisories", to="security.Product")),
            ],
            options={
                "ordering": ("-year", "-order"),
                "get_latest_by": "last_modified",
            },
            bases=(models.Model,),
        ),
    ]
