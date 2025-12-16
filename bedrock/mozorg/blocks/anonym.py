# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail_link_block.blocks import LinkBlock
from wagtail_thumbnail_choice_block import ThumbnailChoiceBlock

HEADING_TEXT_FEATURES = [
    "bold",
    "italic",
    "link",
    "superscript",
    "subscript",
    "strikethrough",
]


class FigureBlockSettings(blocks.StructBlock):
    make_full_width = blocks.BooleanBlock(
        required=False,
        default=False,
        label="Make Full Width",
        inline_form=True,
        help_text="The Default width is constrained to the layout grid with a max-width, centered on the page.",
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "Full width: {make_full_width}"
        form_classname = "compact-form struct-block"


class FigureBlock(blocks.StructBlock):
    settings = FigureBlockSettings()
    image = ImageChooserBlock()

    class Meta:
        template = "mozorg/cms/anonym/blocks/figure.html"
        label = "Section"
        label_format = "{heading}"


class CTABlock(blocks.StructBlock):
    label = blocks.CharBlock(label="Link Text")
    link = LinkBlock()

    class Meta:
        label = "Link"
        label_format = "Link - {label}"


class SectionBlockSettings(blocks.StructBlock):
    theme = ThumbnailChoiceBlock(
        choices=(
            ("index", "Index"),
            ("top_glow", "Top Glow"),
        ),
        thumbnails={
            "index": "/media/img/icons/index.svg",
            "top_glow": "/media/img/icons/top_glow.svg",
        },
        inline_form=True,
        required=False,
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "Theme: {theme}"
        form_classname = "compact-form struct-block"


class SectionBlock(blocks.StructBlock):
    settings = SectionBlockSettings()
    superheading_text = blocks.RichTextBlock(features=HEADING_TEXT_FEATURES, required=False)
    heading_text = blocks.RichTextBlock(
        features=HEADING_TEXT_FEATURES,
        help_text="Use Bold to make parts of this text black.",
    )
    subheading_text = blocks.RichTextBlock(features=HEADING_TEXT_FEATURES, required=False)

    content = blocks.StreamBlock(
        [
            ("figure_block", FigureBlock()),
        ]
    )
    action = blocks.ListBlock(CTABlock(), min_num=0, max_num=1, default=[])

    class Meta:
        template = "mozorg/cms/anonym/blocks/section.html"
        label = "Section"
        label_format = "{heading}"
