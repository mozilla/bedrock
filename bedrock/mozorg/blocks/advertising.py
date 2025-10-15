# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from wagtail import blocks


class AdvertisingHeroBlock(blocks.StructBlock):
    """Advertising page hero block."""

    heading_text = blocks.CharBlock(char_max_length=255)
    primary_cta_text = blocks.CharBlock(char_max_length=255)
    primary_cta_link = blocks.URLBlock(
        char_max_length=255,
        help_text="Link URL for the primary CTA.",
    )
    supporting_text = blocks.TextBlock()
    secondary_cta_text = blocks.CharBlock(char_max_length=255)
    secondary_cta_link = blocks.URLBlock(
        char_max_length=255,
        help_text="Link URL for the secondary CTA.",
    )

    class Meta:
        label = "Hero"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/advertising_hero_block.html"
        form_classname = "compact-form struct-block"
