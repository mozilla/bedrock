# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail_link_block.blocks import LinkBlock


class DonateBlockSettings(blocks.StructBlock):
    """Settings for the donate block."""

    background_color = blocks.ChoiceBlock(
        choices=[
            ("pink", "Pink"),
            ("green", "Green"),
            ("orange", "Orange"),
            ("gray", "Gray"),
        ],
        required=False,
        help_text="What color should the background be?",
    )

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text=(
            "Optional: Add an ID to make this section linkable. "
            "Will be converted to URL-safe format (e.g., 'Donate Section' becomes 'donate-section')."
        ),
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "Background: {background_color}"
        form_classname = "compact-form struct-block"


class DonateBlock(blocks.StructBlock):
    """Block for the donate section on the homepage."""

    settings = DonateBlockSettings()

    heading = blocks.CharBlock(
        max_length=255,
    )

    body = blocks.RichTextBlock(
        features=["bold", "link"],
        help_text="Keep this to 2 paragraphs or fewer.",
    )

    image = ImageChooserBlock(
        help_text="Ideal image size is 1400 x 700. Image will be cropped to a 2:1 aspect ratio.",
    )

    image_alt = blocks.CharBlock(
        max_length=255,
        required=False,
        help_text="A concise description of the image for someone who can't see it.",
    )

    cta_text = blocks.CharBlock(
        max_length=50,
        label="Link text",
    )

    cta_link = LinkBlock(
        label="Link destination",
    )

    class Meta:
        template = "mozorg/cms/home/blocks/donate_block.html"
        icon = "heart"
        label = "Donate Section"
        label_format = "{heading}"
