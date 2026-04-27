# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys
from uuid import uuid4

from django.db import migrations

from bedrock.base.config_manager import config


def _should_skip():
    return "pytest" in sys.modules or config("SQLITE_EXPORT_MODE", parser=bool, default="false")


def populate_notification_snippet_analytics_ids(apps, schema_editor):
    if _should_skip():
        return
    NotificationSnippet = apps.get_model("mozorg", "NotificationSnippet")
    for snippet in NotificationSnippet.objects.filter(analytics_id=""):
        snippet.analytics_id = str(uuid4())
        snippet.save(update_fields=["analytics_id"])


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("mozorg", "0029_notificationsnippet_analytics_id"),
    ]

    operations = [
        migrations.RunPython(populate_notification_snippet_analytics_ids, migrations.RunPython.noop),
    ]
