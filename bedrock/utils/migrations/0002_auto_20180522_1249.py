# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("utils", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="gitrepostate",
            name="latest_ref_timestamp",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="gitrepostate",
            name="repo_name",
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name="gitrepostate",
            name="repo_url",
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
