# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys
from uuid import uuid4

from django.core.management import call_command
from django.db import migrations

from bedrock.base.config_manager import config


def _should_skip():
    return "pytest" in sys.modules or config("SQLITE_EXPORT_MODE", parser=bool, default="false")


def populate_news_item_analytics_ids(apps, schema_editor):
    if _should_skip():
        return
    AnonymNewsItemPage = apps.get_model("anonym", "AnonymNewsItemPage")
    for page in AnonymNewsItemPage.objects.filter(analytics_id=""):
        page.analytics_id = str(uuid4())
        page.save(update_fields=["analytics_id"])


def inject_analytics_ids_into_link_blocks(apps, schema_editor):
    if _should_skip():
        return
    call_command("populate_link_block_analytics_ids")


def restructure_case_study_list_blocks(apps, schema_editor):
    if _should_skip():
        return
    call_command("populate_case_study_analytics_ids")


def populate_nav_button_analytics_ids(apps, schema_editor):
    if _should_skip():
        return
    call_command("populate_nav_button_analytics_ids")


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("anonym", "0015_anonymnewsitempage_analytics_id"),
    ]

    operations = [
        migrations.RunPython(populate_news_item_analytics_ids, migrations.RunPython.noop),
        migrations.RunPython(inject_analytics_ids_into_link_blocks, migrations.RunPython.noop),
        migrations.RunPython(restructure_case_study_list_blocks, migrations.RunPython.noop),
        migrations.RunPython(populate_nav_button_analytics_ids, migrations.RunPython.noop),
    ]
