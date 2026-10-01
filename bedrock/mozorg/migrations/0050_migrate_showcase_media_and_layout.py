# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys
import uuid

from django.db import migrations

from bedrock.base.config_manager import config


def _should_skip():
    return "pytest" in sys.modules or config("SQLITE_EXPORT_MODE", parser=bool, default="false")


def _migrate_showcase_block_value(value):
    """Reshape a single showcase_block's value in place, from the original
    image/image_alt/two_column_layout shape to the media chooser and named
    layout shape. Returns True if the value was modified.

    Old structure:
        {
            "settings": {"two_column_layout": false, ...},
            "image": 123,
            "image_alt": "...",
            ...
        }

    New structure:
        {
            "settings": {"layout": "heading-body-media", ...},
            "media": [
                {
                    "type": "ultrawide_image",
                    "value": {"image": {"image": 123, "image_alt": "..."}},
                    "id": "...",
                }
            ],
            ...
        }

    Idempotent: a value already in the new shape has neither "image" nor
    "two_column_layout", so it passes through unmodified.
    """
    modified = False

    if "image" in value:
        image = value.pop("image")
        image_alt = value.pop("image_alt", "")
        value["media"] = [
            {
                "type": "ultrawide_image",
                "value": {"image": {"image": image, "image_alt": image_alt}},
                "id": str(uuid.uuid4()),
            }
        ]
        modified = True

    settings = value.get("settings", {})
    if "two_column_layout" in settings:
        two_column_layout = settings.pop("two_column_layout")
        settings["layout"] = "heading-and-body-media" if two_column_layout else "heading-body-media"
        modified = True

    return modified


def _migrate_raw_blocks(raw):
    """Apply _migrate_showcase_block_value to every showcase_block in a list
    of raw (undeserialized) top-level block dicts. Returns True if anything
    was modified.

    This does not touch showcase_gallery_block content — that block is being
    migrated to showcase_block by hand, page by page, ahead of its removal.
    """
    modified = False

    for block in raw:
        if block.get("type") == "showcase_block":
            if _migrate_showcase_block_value(block.get("value", {})):
                modified = True

    return modified


def migrate_showcase_media_and_layout(apps, schema_editor):
    """
    Reshape existing ShowcaseBlock.value to the media chooser and named layout
    system. See _migrate_showcase_block_value for the shape change.

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
            if _migrate_raw_blocks(raw):
                Model.objects.filter(pk=page.pk).update(content=raw)


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("mozorg", "0049_alter_aboutuspage_content_alter_homepage_content"),
    ]

    operations = [
        migrations.RunPython(migrate_showcase_media_and_layout, migrations.RunPython.noop),
    ]
