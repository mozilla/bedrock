# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations

import django_extensions.db.fields.json


class Migration(migrations.Migration):
    dependencies = [
        ("security", "0004_mitrecve"),
    ]

    operations = [
        migrations.AddField(
            model_name="mitrecve",
            name="mfsa_ids",
            field=django_extensions.db.fields.json.JSONField(default="[]"),
        ),
    ]
