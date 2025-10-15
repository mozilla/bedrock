# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


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


class SectionHeaderBlock(blocks.StructBlock):
    """Section header block."""

    superheading_text = blocks.CharBlock(char_max_length=255, required=False)
    heading_text = blocks.CharBlock(char_max_length=255)
    subheading_text = blocks.CharBlock(char_max_length=255, required=False)
    image = ImageChooserBlock(required=False)
    image_alt_text = blocks.CharBlock(char_max_length=255, required=False)

    class Meta:
        icon = "title"
        label = "Section Heading"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/section_heading_block.html"
        form_classname = "compact-form struct-block"
