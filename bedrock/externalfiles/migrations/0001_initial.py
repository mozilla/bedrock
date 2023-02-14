# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExternalFile",
            fields=[
                ("name", models.CharField(max_length=50, serialize=False, primary_key=True)),
                ("content", models.TextField()),
                ("last_modified", models.DateTimeField(auto_now=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
