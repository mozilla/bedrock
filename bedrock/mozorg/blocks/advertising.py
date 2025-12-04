# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.exceptions import ValidationError

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
    superheading_text = blocks.CharBlock(char_max_length=255, required=False)
    heading_text = blocks.CharBlock(char_max_length=255, required=False)
    subheading_text = blocks.CharBlock(char_max_length=255, required=False)
    image = ImageChooserBlock(required=False)

    def clean(self, value):
        errors = {}

        superheading = value.get("superheading_text", "").strip()
        heading = value.get("heading_text", "").strip()
        subheading = value.get("subheading_text", "").strip()

        if not superheading and not heading and not subheading:
            errors["heading_text"] = ValidationError("You must provide either superheading, or heading, or subheading.")

        if errors:
            raise blocks.StructBlockValidationError(errors)

        return super().clean(value)

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
        label="Position the image to the right of the statistic",
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

    heading_text = blocks.TextBlock()
    supporting_text = blocks.RichTextBlock(features=["bold", "italic", "link"])

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

    statistic_superlabel = blocks.CharBlock(char_max_length=255, required=False)
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

    class Meta:
        icon = "decimal"
        label = "Statistic Callout Block"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/statistic_callout_block.html"
        form_classname = "compact-form struct-block"


class FigureBlock(blocks.StructBlock):
    """Figure block."""

    image = ImageChooserBlock(required=False)
    image_caption_heading = blocks.TextBlock(char_max_length=255, required=False)
    image_caption_text = blocks.TextBlock(char_max_length=255, required=False)

    class Meta:
        label = "Feature Item"
        label_format = "{image_caption}"
        form_classname = "compact-form struct-block"


class FeatureItemWithModalBlock(blocks.StructBlock):
    """Block for a feature item with a modal."""

    heading_text = blocks.CharBlock(char_max_length=255)
    figures = blocks.ListBlock(FigureBlock(), min_num=1)
    cta_text = blocks.CharBlock(char_max_length=255, required=False)
    cta_link = LinkBlock(label="CTA Link", required=False)

    class Meta:
        label = "Feature Item"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/feature_item_with_modal_block.html"
        form_classname = "compact-form struct-block"


class FeatureListWithModalsBlock(blocks.StructBlock):
    """A block for a list of features, each with a modal."""

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable from navigation",
    )
    heading_text = blocks.CharBlock(char_max_length=255)
    supporting_text = blocks.TextBlock()
    feature_list_items = blocks.ListBlock(FeatureItemWithModalBlock(), min_num=1)

    class Meta:
        icon = "list-ul"
        label = "Feature List With Modals Block"
        label_format = "{heading_text}"
        template = "mozorg/cms/advertising/blocks/feature_list_with_modals_block.html"
        form_classname = "compact-form struct-block"


class RowTextAndLinkBlock(blocks.StructBlock):
    """Block for text and a link."""

    text = blocks.CharBlock(char_max_length=255, required=False)
    link_text = blocks.CharBlock(char_max_length=255)
    link = LinkBlock(label="Link")

    class Meta:
        icon = "doc-full"
        label = "Text and Link Block"
        label_format = "{text}"
        template = "mozorg/cms/advertising/blocks/row_text_and_link_block.html"
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


class SectionSettings(blocks.StructBlock):
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
    display_on_dark_background = blocks.BooleanBlock(
        default=False,
        required=False,
        label="Should the section have a dark background?",
        inline_form=True,
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "ID: {anchor_id} - Divider: {has_top_divider} - Dark background: {display_on_dark_background}"
        form_classname = "compact-form struct-block"


class SectionBlock(blocks.StructBlock):
    settings = SectionSettings()

    header = SectionHeaderBlock()
    content = blocks.StreamBlock(
        [
            ("section_header_block", SectionHeaderBlock()),
            ("figure_with_statistic_block", FigureWithStatisticBlock()),
            ("statistic_callout_block", StatisticCalloutBlock()),
            ("features_with_modals", FeatureListWithModalsBlock()),
            ("feature_list_block", FeatureListBlock()),
        ]
    )
    call_to_action = blocks.ListBlock(RowTextAndLinkBlock(), min_num=0, max_num=1, default=[], label="Call to Action")

    class Meta:
        template = "mozorg/cms/advertising/blocks/section.html"
        label = "Section"
        label_format = "{header}"
