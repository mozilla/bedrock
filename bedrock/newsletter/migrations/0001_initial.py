# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations, models

import django_extensions.db.fields.json


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Newsletter",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("slug", models.SlugField(help_text=b"The ID for the newsletter that will be used by clients", unique=True)),
                ("data", django_extensions.db.fields.json.JSONField()),
            ],
        ),
    ]
