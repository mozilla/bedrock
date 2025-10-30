# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail_link_block.blocks import LinkBlock

CAPTION_TEXT_FEATURES = [
    "bold",
    "italic",
    "link",
    "superscript",
    "subscript",
    "strikethrough",
    "link",
]


class AdvertisingHeroBlock(blocks.StructBlock):
    """Advertising page hero block."""

    heading_text = blocks.CharBlock(char_max_length=255)
    primary_cta_text = blocks.CharBlock(char_max_length=255)
    primary_cta_link = LinkBlock(label="Primary CTA Link")
    supporting_text = blocks.TextBlock()
    secondary_cta_text = blocks.CharBlock(char_max_length=255)
    secondary_cta_link = LinkBlock(label="Secondary CTA Link")

    class Meta:
        label = "Hero"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/advertising_hero_block.html"
        form_classname = "compact-form struct-block"


class SectionHeaderBlock(blocks.StructBlock):
    """Section header block."""

    has_top_divider = blocks.BooleanBlock(
        default=False,
        required=False,
        label="Should the section have a divider line on top?",
        inline_form=True,
    )
    superheading_text = blocks.CharBlock(char_max_length=255, required=False)
    heading_text = blocks.CharBlock(char_max_length=255)
    subheading_text = blocks.CharBlock(char_max_length=255, required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "title"
        label = "Section Heading"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/section_heading_block.html"
        form_classname = "compact-form struct-block"


class FigureWithStatisticBlock(blocks.StructBlock):
    """Figure with a statistic block."""

    image = ImageChooserBlock(required=False)
    image_caption = blocks.RichTextBlock(char_max_length=255)
    statistic_value = blocks.CharBlock(char_max_length=255)
    statistic_label = blocks.CharBlock(char_max_length=255)
    align_image_on_right = blocks.BooleanBlock(
        default=False,
        required=False,
        label="Should the image be to the right of the statistic?",
        inline_form=True,
    )
    cta_text = blocks.CharBlock(char_max_length=255, required=False)
    cta_link = LinkBlock(label="Link", required=False)

    class Meta:
        icon = "decimal"
        label = "Figure With Statistic"
        label_format = "{statistic_value} {statistic_label}"
        template = "mozorg/cms/advertising/blocks/figure_with_statistic_block.html"
        form_classname = "compact-form struct-block"


class FeatureListItemBlock(blocks.StructBlock):
    """Feature list item block."""

    heading_text = blocks.CharBlock(char_max_length=255)
    supporting_text = blocks.TextBlock()

    class Meta:
        label = "Feature Item"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/feature_list_item_block.html"
        form_classname = "compact-form struct-block"


class FeatureListBlock(blocks.StructBlock):
    """Feature list block."""

    feature_list_items = blocks.ListBlock(FeatureListItemBlock(), min_num=1)

    class Meta:
        icon = "list-ul"
        label = "Feature List"
        label_format = "Feature List"
        template = "mozorg/cms/advertising/blocks/feature_list_block.html"
        form_classname = "compact-form struct-block"


class NotificationBlock(blocks.StructBlock):
    notification_text = blocks.RichTextBlock(
        char_max_length=255,
        features=["bold", "italic", "superscript", "subscript", "strikethrough", "code", "link"],
    )
    link = LinkBlock()

    class Meta:
        template = "mozorg/cms/advertising/blocks/notification_block.html"
