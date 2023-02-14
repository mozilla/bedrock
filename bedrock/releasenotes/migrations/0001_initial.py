# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations, models

import bedrock.releasenotes.models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProductRelease",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("product", models.CharField(max_length=50)),
                ("channel", models.CharField(max_length=50)),
                ("version", models.CharField(max_length=25)),
                ("slug", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("release_date", models.DateField()),
                ("text", bedrock.releasenotes.models.MarkdownField(blank=True)),
                ("is_public", models.BooleanField(default=False)),
                ("bug_list", models.TextField(blank=True)),
                ("bug_search_url", models.CharField(max_length=2000, blank=True)),
                ("system_requirements", bedrock.releasenotes.models.MarkdownField(blank=True)),
                ("created", models.DateTimeField()),
                ("modified", models.DateTimeField()),
                ("notes", bedrock.releasenotes.models.NotesField(blank=True)),
            ],
        ),
    ]
