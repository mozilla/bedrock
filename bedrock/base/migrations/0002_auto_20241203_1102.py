# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations

from waffle.models import Switch

# The name of the switch must be unique.
SWITCH_NAME = "M24_HERO_ANIMATION"


def create_switch(apps, schema_editor):
    Switch.objects.get_or_create(
        name=SWITCH_NAME,
        defaults={"active": False},  # Set initial state, True or False.
    )


def remove_switch(apps, schema_editor):
    Switch.objects.filter(name=SWITCH_NAME).delete()


class Migration(migrations.Migration):
    dependencies = [
        (
            "base",
            "0001_initial",
        ),  # Keep whatever the makemigrations command generated here.
    ]

    operations = [
        migrations.RunPython(create_switch, remove_switch),
    ]
