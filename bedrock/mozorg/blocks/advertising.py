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


SOCIAL_MEDIA_ICON_CHOICES = [
    ("linkedin", "LinkedIn"),
    ("tiktok", "TikTok"),
    ("spotify", "Spotify"),
    ("twitter", "Twitter"),
    ("bluesky", "BlueSky"),
    ("instagram", "Instagram"),
    ("youtube", "YouTube"),
]


class AdvertisingHeroBlock(blocks.StructBlock):
    """Advertising page hero block."""

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable from navigation (e.g., 'hero', 'overview')",
    )
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

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable from navigation (e.g., 'solutions', 'why-mozilla')",
    )
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
    colors_should_match_header = blocks.BooleanBlock(
        default=False,
        required=False,
        label="Should the section colors match the colors of the header?",
        inline_form=True,
    )

    class Meta:
        icon = "title"
        label = "Section Heading"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/section_heading_block.html"
        form_classname = "compact-form struct-block"


class FigureWithStatisticBlock(blocks.StructBlock):
    """Figure with a statistic block."""

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable from navigation",
    )
    image = ImageChooserBlock(required=False)
    image_caption = blocks.RichTextBlock(char_max_length=255, required=False)
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
    colors_should_match_header = blocks.BooleanBlock(
        default=False,
        required=False,
        label="Should the section colors match the colors of the header?",
        inline_form=True,
    )

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

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable from navigation",
    )
    feature_list_items = blocks.ListBlock(FeatureListItemBlock(), min_num=1)

    class Meta:
        icon = "list-ul"
        label = "Feature List"
        label_format = "Feature List"
        template = "mozorg/cms/advertising/blocks/feature_list_block.html"
        form_classname = "compact-form struct-block"


class ListItemBlock(blocks.StructBlock):
    """Feature list item block."""

    heading_text = blocks.CharBlock(char_max_length=255)
    supporting_text = blocks.RichTextBlock(
        features=["bold", "italic", "link"],
    )

    class Meta:
        label = "List Item"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/list_item_block.html"
        form_classname = "compact-form struct-block"


class ListBlock(blocks.StructBlock):
    """A block containing a list of items."""

    list_items = blocks.ListBlock(ListItemBlock())

    class Meta:
        icon = "list-ul"
        label = "List"
        label_format = "List"
        template = "mozorg/cms/advertising/blocks/list_block.html"
        form_classname = "compact-form struct-block"


class StatisticBlock(blocks.StructBlock):
    """Statistic block."""

    statistic_value = blocks.CharBlock(char_max_length=255)
    statistic_label = blocks.CharBlock(char_max_length=255)

    class Meta:
        icon = "decimal"
        label = "Statistic Block"
        label_format = "{statistic_value} {statistic_label}"
        template = "mozorg/cms/advertising/blocks/statistic_block.html"
        form_classname = "compact-form struct-block"


class StatisticCalloutBlock(blocks.StructBlock):
    """Block for statistics with a callout."""

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable from navigation",
    )
    heading_text = blocks.CharBlock(char_max_length=255)
    statistics = blocks.ListBlock(StatisticBlock(), min_num=1)
    colors_should_match_header = blocks.BooleanBlock(
        default=False,
        required=False,
        label="Should the section colors match the colors of the header?",
        inline_form=True,
    )

    class Meta:
        icon = "decimal"
        label = "Statistic Callout Block"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/statistic_callout_block.html"
        form_classname = "compact-form struct-block"


class TwoColumnDetailBlock(blocks.StructBlock):
    """Feature list item block."""

    heading_text = blocks.CharBlock(char_max_length=255)
    subheading = blocks.TextBlock()
    second_column = blocks.StreamBlock(
        [
            ("list", ListBlock()),
        ],
        required=False,
    )

    class Meta:
        label = "Two Column Detail"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/two_column_detail_block.html"
        form_classname = "compact-form struct-block"


class LinkWithIcon(blocks.StructBlock):
    """Link with an icon."""

    icon = blocks.ChoiceBlock(required=False, choices=SOCIAL_MEDIA_ICON_CHOICES, inline_form=True)
    link = LinkBlock()

    class Meta:
        icon = "link"
        label = "Link With Icon"
        label_format = "Link With Icon"
        template = "mozorg/cms/advertising/blocks/link_with_icon_block.html"
        form_classname = "compact-form struct-block"


class NotificationBlock(blocks.StructBlock):
    notification_text = blocks.RichTextBlock(
        char_max_length=255,
        features=["bold", "italic", "superscript", "subscript", "strikethrough", "code", "link"],
    )
    links = blocks.StreamBlock(
        [
            ("link_with_icon", LinkWithIcon()),
        ],
        required=False,
    )

    class Meta:
        template = "mozorg/cms/advertising/blocks/notification_block.html"
