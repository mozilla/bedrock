# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import sys

from django.db import migrations

from bedrock.base.config_manager import config


def _should_skip():
    return "pytest" in sys.modules or config("SQLITE_EXPORT_MODE", parser=bool, default="false")


def migrate_showcase_label(apps, schema_editor):
    """
    Rename ShowcaseBlock.value.sub_heading to ShowcaseBlock.value.label, matching
    the field rename on the block definition.

    Old structure:
        {
            "type": "showcase_block",
            "value": {
                "sub_heading": "...",
                ...
            }
        }

    New structure:
        {
            "type": "showcase_block",
            "value": {
                "label": "...",
                ...
            }
        }

    Affects: AboutUsPage.content and HomePage.content
    """
    if _should_skip():
        return

    AboutUsPage = apps.get_model("mozorg", "AboutUsPage")
    HomePage = apps.get_model("mozorg", "HomePage")

    for Model in [AboutUsPage, HomePage]:
        for page in Model.objects.all():
            if not page.content:
                continue

            raw = list(page.content.raw_data)
            modified = False

            for block in raw:
                if block.get("type") == "showcase_block":
                    value = block.get("value", {})
                    if "sub_heading" in value:
                        value["label"] = value.pop("sub_heading")
                        modified = True

            if modified:
                Model.objects.filter(pk=page.pk).update(content=json.dumps(raw))


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("mozorg", "0046_alter_aboutuspage_content_alter_homepage_content"),
    ]

    operations = [
        migrations.RunPython(migrate_showcase_label, migrations.RunPython.noop),
    ]
