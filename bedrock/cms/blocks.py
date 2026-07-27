# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from copy import deepcopy
from uuid import uuid4

from wagtail import blocks


class UUIDBlock(blocks.CharBlock):
    """
    CharBlock that auto-generates a UUID when left blank.

    Used for analytics tracking IDs. Excluded from translation.
    When copying a page, regenerate_analytics_ids() is called to replace all UUIDs with new ones.
    """

    def clean(self, value):
        return super().clean(value) or str(uuid4())

    def get_translatable_segments(self, value):
        # UUIDs are analytics IDs, not user-facing content — exclude from translation
        return []

    def restore_translated_segments(self, value, segments):
        return value


def _regenerate_uuid_blocks(block, value):
    """Walk a block's prepared value and replace every UUIDBlock (analytics ID)
    with a freshly generated UUID, recursing into structs, streams and lists.

    Operates on the JSON-serialisable form returned by ``get_prep_value`` and
    mutates it in place, returning the (possibly replaced) value."""
    if isinstance(block, UUIDBlock):
        return str(uuid4())
    if isinstance(block, blocks.StructBlock):
        for name, child_block in block.child_blocks.items():
            if name in value:
                value[name] = _regenerate_uuid_blocks(child_block, value[name])
    elif isinstance(block, blocks.StreamBlock):
        for member in value:
            child_block = block.child_blocks.get(member["type"])
            if child_block is not None:
                member["value"] = _regenerate_uuid_blocks(child_block, member["value"])
    elif isinstance(block, blocks.ListBlock):
        for index, member in enumerate(value):
            if isinstance(member, dict) and "value" in member and "type" in member:
                member["value"] = _regenerate_uuid_blocks(block.child_block, member["value"])
            else:
                value[index] = _regenerate_uuid_blocks(block.child_block, member)
    return value


def regenerate_analytics_ids(stream_value):
    """Return a new StreamField value with every analytics-ID UUIDBlock replaced
    by a freshly generated UUID.

    Used when duplicating a page so the copy gets its own unique analytics IDs.
    Translations must NOT call this — a translated page keeps the source page's
    analytics IDs so tracking stays consistent across locales."""
    stream_block = stream_value.stream_block
    # deepcopy so mutating the prepared data never touches the source value —
    # get_prep_value() can share nested references with the live StreamValue.
    prepared = deepcopy(stream_value.get_prep_value())
    _regenerate_uuid_blocks(stream_block, prepared)
    return stream_block.to_python(prepared)
