# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("firefox", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FirefoxOSFeedLink",
        ),
    ]
