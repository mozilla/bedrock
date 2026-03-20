# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("careers", "0002_position_internal_job_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="position",
            name="updated_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
