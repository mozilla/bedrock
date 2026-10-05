# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import sys
import uuid

from django.db import migrations

from bedrock.base.config_manager import config

OLD_FIELD = "sub_heading"
NEW_FIELD = "cta_label"
OLD_FIELD_PATH = f"content.showcase_block.{OLD_FIELD}"
NEW_FIELD_PATH = f"content.showcase_block.{NEW_FIELD}"

# Must match wagtail_localize.models.TranslationContext._get_path_id
PATH_ID_NAMESPACE = uuid.UUID("fcab004a-2b50-11ea-978f-2e728ce88125")


def _should_skip():
    return "pytest" in sys.modules or config("SQLITE_EXPORT_MODE", parser=bool, default="false")


def _rename_path(path):
    prefix, _, last = path.rpartition(".")
    return f"{prefix}.{NEW_FIELD}" if last == OLD_FIELD else path


def migrate_translation_contexts(apps):
    """
    Migration 0047 renamed ShowcaseBlock.sub_heading to cta_label in page content, but
    wagtail-localize's TranslationContexts still pointed at the old field. The translation
    editor resolves each context's field_path against the current block definition, so the
    stale contexts raise KeyError: 'sub_heading' when editing a translation.

    Rename the contexts in place so existing StringSegments and StringTranslations stay linked.
    If a source was already re-synced and a cta_label context exists, move any translations it
    lacks across, then delete the stale one.
    """
    TranslationContext = apps.get_model("wagtail_localize", "TranslationContext")
    StringTranslation = apps.get_model("wagtail_localize", "StringTranslation")

    for context in TranslationContext.objects.filter(field_path=OLD_FIELD_PATH):
        new_path = _rename_path(context.path)
        new_path_id = uuid.uuid5(PATH_ID_NAMESPACE, new_path)

        existing = TranslationContext.objects.filter(object_id=context.object_id, path_id=new_path_id).first()
        if existing is None:
            context.path = new_path
            context.path_id = new_path_id
            context.field_path = NEW_FIELD_PATH
            context.save(update_fields=["path", "path_id", "field_path"])
            continue

        for translation in StringTranslation.objects.filter(context=context):
            already_translated = StringTranslation.objects.filter(
                context=existing,
                locale_id=translation.locale_id,
                translation_of_id=translation.translation_of_id,
            ).exists()
            if not already_translated:
                translation.context = existing
                translation.save(update_fields=["context"])
        context.delete()


def migrate_translation_sources(apps):
    TranslationSource = apps.get_model("wagtail_localize", "TranslationSource")
    ContentType = apps.get_model("contenttypes", "ContentType")

    content_types = ContentType.objects.filter(app_label="mozorg", model__in=["homepage", "aboutuspage"])
    for source in TranslationSource.objects.filter(specific_content_type__in=content_types):
        data = json.loads(source.content_json)
        stream = data.get("content")
        if not stream:
            continue
        stream_is_str = isinstance(stream, str)
        if stream_is_str:
            stream = json.loads(stream)

        modified = False
        for block in stream:
            value = block.get("value")
            if block.get("type") == "showcase_block" and isinstance(value, dict) and OLD_FIELD in value:
                value[NEW_FIELD] = value.pop(OLD_FIELD)
                modified = True

        if modified:
            data["content"] = json.dumps(stream) if stream_is_str else stream
            source.content_json = json.dumps(data)
            source.save(update_fields=["content_json"])


def migrate_showcase_cta_label_translation_data(apps, schema_editor):
    if _should_skip():
        return
    migrate_translation_contexts(apps)
    migrate_translation_sources(apps)


class Migration(migrations.Migration):
    dependencies = [
        ("mozorg", "0048_alter_aboutuspage_content_alter_homepage_content"),
        ("wagtail_localize", "0016_rename_page_revision_translationlog_revision"),
    ]

    operations = [
        migrations.RunPython(migrate_showcase_cta_label_translation_data, migrations.RunPython.noop),
    ]
