# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.cms.blocks import UUIDBlock


def test_uuid_block_auto_generates_when_blank():
    """clean() returns a UUID when the value is blank (requires required=False)."""
    block = UUIDBlock(required=False)
    result = block.clean("")
    assert result != ""
    assert len(result) == 36  # UUID v4 string length


def test_uuid_block_preserves_existing_value():
    """clean() does not replace a value that is already set."""
    block = UUIDBlock(required=False)
    existing = "existing-uuid-value"
    assert block.clean(existing) == existing


def test_uuid_block_excluded_from_translation():
    """get_translatable_segments() returns empty list so UUIDs are never sent for translation."""
    block = UUIDBlock()
    assert block.get_translatable_segments("any-uuid") == []


def test_uuid_block_restore_translated_segments_is_noop():
    """restore_translated_segments() returns the original value unchanged."""
    block = UUIDBlock()
    value = "some-uuid"
    assert block.restore_translated_segments(value, []) == value
