# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations


def update_waffle(apps, schema_editor):
    Switch = apps.get_model("waffle", "Switch")

    # Update the switch if it exists, or create it if it doesn't
    Switch.objects.update_or_create(name="M24_WEBSITE_REFRESH", defaults={"active": True})


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0001_initial"),  # <- gets set by the above command
    ]

    operations = [
        migrations.RunPython(update_waffle),
    ]
