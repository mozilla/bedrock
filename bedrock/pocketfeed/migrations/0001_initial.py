# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PocketArticle",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("pocket_id", models.IntegerField()),
                ("url", models.URLField()),
                ("domain", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("image_src", models.URLField()),
                ("time_shared", models.DateTimeField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-time_shared"],
                "get_latest_by": "time_shared",
            },
        ),
    ]
