# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("security", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="securityadvisory",
            name="impact",
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name="securityadvisory",
            name="reporter",
            field=models.CharField(default="", max_length=100, blank=True),
            preserve_default=False,
        ),
    ]
