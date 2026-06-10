# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys

from django.db import migrations

from bedrock.base.config_manager import config


def _should_skip():
    return "pytest" in sys.modules or config("SQLITE_EXPORT_MODE", parser=bool, default="false")


def populate_leadership_profile_snippets(apps, schema_editor):
    """
    Traverse all LeadershipPage instances and create one LeadershipProfileSnippet
    per LeadershipBioBlock found.

    Source nesting (via raw_data):
        leadership_sections (StreamField)
        → section (LeadershipSectionBlock)
          → leadership_group (ListBlock of LeadershipGroupBlock)
            → leaders (ListBlock of LeadershipBioBlock)
              → each bio

    Fields copied:
        bio.name                  → snippet.name
        bio.headshot.image (PK)   → snippet.image_id   (PK passthrough — never save the image)
        bio.headshot.photos_link  → snippet.press_photos_link
        bio.biography             → snippet.biography
        bio.external_links        → snippet.external_links (ListBlock items → StreamField blocks)

    Fields intentionally discarded:
        bio.job_title             (no field on snippet)
        bio.headshot.image_alt_text (no field on snippet; BedrockImage deliberately has no alt field)
        section/group title & description (no field on flat snippet)
    """
    if _should_skip():
        return

    LeadershipPage = apps.get_model("mozorg", "LeadershipPage")
    LeadershipProfileSnippet = apps.get_model("mozorg", "LeadershipProfileSnippet")
    BedrockImage = apps.get_model("cms", "BedrockImage")

    for page in LeadershipPage.objects.all():
        if not page.leadership_sections:
            continue

        for section in page.leadership_sections.raw_data:
            # section is {"type": "section", "id": "...", "value": {...}}
            section_value = section.get("value", {})

            for group_item in section_value.get("leadership_group", []):
                # leadership_group is a ListBlock; each item is {"type": "item", "id": "...", "value": {...}}
                group_value = group_item.get("value", {})

                for leader_item in group_value.get("leaders", []):
                    # leaders is a ListBlock; each item is {"type": "item", "id": "...", "value": {...}}
                    bio = leader_item.get("value", {})
                    name = bio.get("name", "")

                    if not name:
                        continue

                    # Idempotent: skip if a snippet for this person+locale already exists.
                    if LeadershipProfileSnippet.objects.filter(
                        name=name,
                        locale_id=page.locale_id,
                    ).exists():
                        continue

                    # headshot is a StructBlock stored as a plain dict (no type/value wrapper)
                    headshot = bio.get("headshot") or {}

                    snippet = LeadershipProfileSnippet(
                        name=name,
                        press_photos_link=headshot.get("photos_link") or "",
                        biography=bio.get("biography") or "",
                        locale_id=page.locale_id,
                    )

                    # Image: PK passthrough only — never fetch-and-save BedrockImage;
                    # its save() queues ~100 renditions and prod has no DB/storage write access.
                    image_pk = headshot.get("image")
                    if image_pk and BedrockImage.objects.filter(pk=image_pk).exists():
                        snippet.image_id = image_pk

                    # external_links: each ListBlock item is {"type": "item", "id": "...", "value": {url, type, text}}.
                    # The snippet's StreamField expects block-type tuples; the inner value shape is
                    # identical (LeadershipExternalLinkBlock is shared between source and target).
                    snippet.external_links = [
                        ("external_link", link_item["value"])
                        for link_item in bio.get("external_links", [])
                        if link_item.get("value")
                    ]

                    snippet.save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("mozorg", "0033_leadershipprofilesnippet"),
    ]

    operations = [
        migrations.RunPython(populate_leadership_profile_snippets, migrations.RunPython.noop),
    ]
