# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import migrations

# This migration originally backfilled analytics IDs on Anonym pages, partly via
# management commands that have since been removed along with the Anonym pages.
# It is kept as a no-op so the migration graph stays intact until the anonym app
# is removed entirely.


class Migration(migrations.Migration):
    dependencies = [
        ("anonym", "0015_anonymnewsitempage_analytics_id"),
    ]

    operations = []
