# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("security", "0008_alter_mitrecve_reporter_alter_product_name_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="MitreCVE",
        ),
    ]
