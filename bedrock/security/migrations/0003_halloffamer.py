# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("security", "0002_auto_20161013_0642"),
    ]

    operations = [
        migrations.CreateModel(
            name="HallOfFamer",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("program", models.CharField(max_length=10, choices=[(b"web", b"Web"), (b"client", b"Client")])),
                ("name", models.CharField(max_length=200)),
                ("date", models.DateField()),
                ("url", models.CharField(max_length=200, blank=True)),
            ],
            options={
                "ordering": ("-date", "id"),
            },
        ),
    ]
