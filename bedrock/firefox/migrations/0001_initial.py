# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FirefoxOSFeedLink",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("link", models.URLField(max_length=2000)),
                ("title", models.CharField(max_length=2000)),
                ("locale", models.CharField(max_length=10, db_index=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
