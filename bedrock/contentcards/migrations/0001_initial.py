# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations, models

import django_extensions.db.fields.json


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContentCard",
            fields=[
                ("id", models.CharField(max_length=100, serialize=False, primary_key=True)),
                ("card_name", models.CharField(max_length=100)),
                ("page_name", models.CharField(max_length=100)),
                ("locale", models.CharField(max_length=10)),
                ("content", models.TextField(blank=True)),
                ("data", django_extensions.db.fields.json.JSONField()),
            ],
            options={
                "ordering": ("id",),
            },
        ),
    ]
