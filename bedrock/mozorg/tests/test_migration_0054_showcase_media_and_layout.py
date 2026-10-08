# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Tests for the pure transform helpers in migration 0054. The migration's
top-level entry point is inert under pytest (see _should_skip), so these
exercise _migrate_showcase_block_value / _migrate_raw_blocks directly.
"""

import importlib.util
from pathlib import Path

from django.apps import apps

import pytest

from bedrock.cms.tests.conftest import minimal_site  # noqa: F401
from bedrock.mozorg import models
from bedrock.mozorg.tests import factories

MIGRATION_PATH = Path(__file__).resolve().parent.parent / "migrations" / "0054_migrate_showcase_media_and_layout.py"

spec = importlib.util.spec_from_file_location("migration_0054", MIGRATION_PATH)
migration_0054 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration_0054)


def test_migrates_two_column_layout_true():
    value = {"settings": {"two_column_layout": True}, "image": 1, "image_alt": "alt text"}
    modified = migration_0054._migrate_showcase_block_value(value)

    assert modified is True
    assert value["settings"] == {"layout": "heading-and-body-media"}


def test_migrates_two_column_layout_false():
    value = {"settings": {"two_column_layout": False}, "image": 1, "image_alt": ""}
    migration_0054._migrate_showcase_block_value(value)

    assert value["settings"] == {"layout": "heading-body-media"}


def test_migrates_image_to_ultrawide_media():
    value = {"settings": {"two_column_layout": False}, "image": 42, "image_alt": "a hero image"}
    migration_0054._migrate_showcase_block_value(value)

    assert "image" not in value
    assert "image_alt" not in value
    media_item = value["media"][0]
    assert media_item["type"] == "ultrawide_image"
    assert media_item["value"] == {"image": {"image": 42, "image_alt": "a hero image"}}
    assert media_item["id"]


def test_missing_image_alt_defaults_to_empty_string():
    value = {"settings": {"two_column_layout": False}, "image": 42}
    migration_0054._migrate_showcase_block_value(value)

    assert value["media"][0]["value"]["image"]["image_alt"] == ""


def test_already_migrated_value_is_left_unmodified():
    value = {
        "settings": {"layout": "heading-body-media"},
        "media": [{"type": "ultrawide_image", "value": {"image": {"image": 1, "image_alt": ""}}, "id": "abc"}],
    }
    original = dict(value)

    modified = migration_0054._migrate_showcase_block_value(value)

    assert modified is False
    assert value == original


def test_migration_is_idempotent():
    value = {"settings": {"two_column_layout": True}, "image": 1, "image_alt": ""}

    first_run = migration_0054._migrate_showcase_block_value(value)
    snapshot = dict(value)
    second_run = migration_0054._migrate_showcase_block_value(value)

    assert first_run is True
    assert second_run is False
    assert value == snapshot


def test_migrate_raw_blocks_only_touches_showcase_block():
    raw = [
        {"type": "transition_block", "value": {"top_color": "light", "bottom_color": "dark"}, "id": "t1"},
        {
            "type": "showcase_gallery_block",
            "value": {"settings": {}, "heading": "Careers", "body": "x", "tiles": [{"image": 1, "image_alt": ""}], "cta_text": "", "cta_link": {}},
            "id": "g1",
        },
        {
            "type": "showcase_block",
            "value": {"settings": {"two_column_layout": True}, "image": 1, "image_alt": ""},
            "id": "s1",
        },
    ]
    original_transition = dict(raw[0])
    original_gallery = dict(raw[1])

    modified = migration_0054._migrate_raw_blocks(raw)

    assert modified is True
    assert raw[0] == original_transition
    assert raw[1] == original_gallery
    assert raw[2]["value"]["settings"] == {"layout": "heading-and-body-media"}
    assert raw[2]["value"]["media"][0]["type"] == "ultrawide_image"


def test_migrate_raw_blocks_reports_unmodified_when_nothing_to_do():
    raw = [
        {"type": "transition_block", "value": {"top_color": "light", "bottom_color": "dark"}, "id": "t1"},
        {
            "type": "showcase_gallery_block",
            "value": {"settings": {}, "heading": "Careers", "body": "x", "tiles": [{"image": 1, "image_alt": ""}], "cta_text": "", "cta_link": {}},
            "id": "g1",
        },
    ]

    assert migration_0054._migrate_raw_blocks(raw) is False


@pytest.mark.django_db
def test_migration_reshapes_freeform_page_showcase_blocks(minimal_site, monkeypatch):  # noqa: F811
    page = factories.FreeformPageFactory(parent=minimal_site.root_page)
    old_raw = [
        {"type": "transition_block", "value": {"top_color": "light", "bottom_color": "dark"}, "id": "t1"},
        {
            "type": "showcase_block",
            "value": {"settings": {"two_column_layout": True}, "heading": "Showcase", "image": 1, "image_alt": "alt"},
            "id": "s1",
        },
    ]
    models.FreeformPage.objects.filter(pk=page.pk).update(content=old_raw)

    monkeypatch.setattr(migration_0054, "_should_skip", lambda: False)
    migration_0054.migrate_showcase_media_and_layout(apps, None)

    raw = list(models.FreeformPage.objects.get(pk=page.pk).content.raw_data)
    assert raw[0] == old_raw[0]
    showcase = raw[1]["value"]
    assert "image" not in showcase
    assert showcase["settings"] == {"layout": "heading-and-body-media"}
    assert showcase["media"][0]["type"] == "ultrawide_image"
    assert showcase["media"][0]["value"] == {"image": {"image": 1, "image_alt": "alt"}}
