# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import sys
import uuid

from django.db import migrations

from bedrock.base.config_manager import config


def _should_skip():
    return "pytest" in sys.modules or config("SQLITE_EXPORT_MODE", parser=bool, default="false")


def migrate_showcase_media_and_layout(apps, schema_editor):
    """
    Reshape existing ShowcaseBlock.value to the media chooser and named layout
    system: image/image_alt become a single-entry media stream, and
    settings.two_column_layout becomes settings.layout.

    Old structure:
        {
            "type": "showcase_block",
            "value": {
                "settings": {"two_column_layout": false, ...},
                "image": 123,
                "image_alt": "...",
                ...
            }
        }

    New structure:
        {
            "type": "showcase_block",
            "value": {
                "settings": {"layout": "heading-body-media", ...},
                "media": [{"type": "image", "value": {"image": 123, "image_alt": "..."}, "id": "..."}],
                ...
            }
        }

    This does not touch showcase_gallery_block content — that is handled
    separately by the consolidate_showcase_blocks management command, since
    reading it requires bypassing the ORM once the block type is removed.

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

                    if "image" in value:
                        image = value.pop("image")
                        image_alt = value.pop("image_alt", "")
                        value["media"] = [
                            {
                                "type": "image",
                                "value": {"image": image, "image_alt": image_alt},
                                "id": str(uuid.uuid4()),
                            }
                        ]
                        modified = True

                    settings = value.get("settings", {})
                    if "two_column_layout" in settings:
                        two_column_layout = settings.pop("two_column_layout")
                        settings["layout"] = "heading-and-body-media" if two_column_layout else "heading-body-media"
                        modified = True

            if modified:
                Model.objects.filter(pk=page.pk).update(content=json.dumps(raw))


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("mozorg", "0050_alter_aboutuspage_content_alter_homepage_content"),
    ]

    operations = [
        migrations.RunPython(migrate_showcase_media_and_layout, migrations.RunPython.noop),
    ]
