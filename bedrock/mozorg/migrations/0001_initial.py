# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import django.utils.timezone
from django.db import migrations, models

import django_extensions.db.fields
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContributorActivity",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("date", models.DateField()),
                ("source_name", models.CharField(max_length=100)),
                ("team_name", models.CharField(max_length=100)),
                ("total", models.IntegerField()),
                ("new", models.IntegerField()),
            ],
            options={
                "ordering": ["-date"],
                "get_latest_by": "date",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="TwitterCache",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("account", models.CharField(unique=True, max_length=100, db_index=True)),
                ("tweets", picklefield.fields.PickledObjectField(default=list, editable=False)),
                ("updated", django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name="contributoractivity",
            unique_together={("date", "source_name", "team_name")},
        ),
    ]
