# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pocketfeed", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pocketarticle",
            name="image_src",
            field=models.URLField(null=True),
        ),
    ]
