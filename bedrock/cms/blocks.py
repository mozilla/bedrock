# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from uuid import uuid4

from wagtail import blocks


class UUIDBlock(blocks.CharBlock):
    """
    CharBlock that auto-generates a UUID when left blank.

    Used for analytics tracking IDs. Excluded from translation.
    """

    def clean(self, value):
        return super().clean(value) or str(uuid4())

    def get_translatable_segments(self, value):
        # UUIDs are analytics IDs, not user-facing content — exclude from translation
        return []

    def restore_translated_segments(self, value, segments):
        return value
