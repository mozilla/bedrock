# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.utils.safestring import mark_safe

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail_link_block.blocks import LinkBlock


class DividerBlock(blocks.StaticBlock):
    """A visual divider for grouping fields in the admin.

    Styles for this block are in media/css/cms/wagtail_admin.css
    """

    def get_admin_text(self):
        return mark_safe('<hr class="cms-divider-hr">')

    class Meta:
        admin_text = ""


# Shared color choices for transition blocks (value is the color suffix for CSS classes)
TRANSITION_COLOR_CHOICES = [
    ("light", "White"),
    ("dark", "Dark"),
    ("green", "Green"),
    ("orange", "Orange"),
    ("pink", "Pink"),
    ("gray", "Gray"),
    ("dark-alt", "Dark-Alt"),
]


class TransitionBlock(blocks.StructBlock):
    """A decorative transition element between sections with configurable colors."""

    top_color = blocks.ChoiceBlock(
        choices=TRANSITION_COLOR_CHOICES,
        default="light",
    )

    bottom_color = blocks.ChoiceBlock(
        choices=TRANSITION_COLOR_CHOICES,
        default="dark-alt",
    )

    class Meta:
        template = "mozorg/cms/blocks/transition_block.html"
        icon = "grip"
        label = "Transition"
        label_format = "{top_color} → {bottom_color}"


class SpringboardItemBlock(blocks.StructBlock):
    """Block for a single media springboard row."""

    url = blocks.URLBlock(
        required=True,
        char_max_length=255,
        help_text="Link to the person's website or social media account with UTMs.",
    )

    link_attributes = blocks.CharBlock(
        required=False,
        char_max_length=255,
        help_text='Link attributes limited to data-* (e.g., data-link-text="...",  data-link-position="...")',
    )

    type = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("Article", "Article"),
            ("Podcast", "Podcast"),
            ("Video", "Video"),
        ],
        help_text="Selects a visual icon type for the link.",
    )

    icon = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("article", "Article"),
            ("podcast", "Podcast"),
            ("video", "Video"),
        ],
        help_text="Selects an icon for the row.",
    )

    topic = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("News", "News"),
            ("Products", "Products"),
            ("Artificial Intelligence", "Artificial Intelligence"),
            ("Open Source AI", "Open Source AI"),
            ("Privacy & Security", "Privacy & Security"),
        ],
        help_text="Selects a topic.",
    )

    author = blocks.CharBlock(
        required=False,
        char_max_length=255,
        help_text="Author name(s), website name",
    )

    preview = blocks.CharBlock(
        required=False,
        char_max_length=255,
        help_text="Short preview of the content",
    )

    class Meta:
        icon = "grip"
        label = "Springboard Item"


class SpringboardBlockSettings(blocks.StructBlock):
    """Settings for the media springboard block."""

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable (e.g., 'media', 'support').",
    )

    background_color = blocks.ChoiceBlock(
        choices=[
            ("", "White"),
            ("m24-t-dark", "Dark"),
            ("m24-t-green", "Green"),
            ("m24-t-orange", "Orange"),
            ("m24-t-pink", "Pink"),
            ("m24-t-gray", "Gray"),
        ],
        required=False,
        help_text="What color should the background be?",
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "ID: {anchor_id} - Background: {background_color}"
        form_classname = "compact-form struct-block"


class SpringboardBlock(blocks.StructBlock):
    """Block for the media springboard section on the homepage."""

    settings = SpringboardBlockSettings()

    text_divider = DividerBlock(label="Text")

    heading = blocks.CharBlock(
        required=False,
        max_length=255,
        help_text="Use sentence case.",
    )

    column_one = blocks.CharBlock(
        max_length=255,
        label="Title for column one",
        help_text="Column name, e.g.: Type",
    )

    column_two = blocks.CharBlock(
        max_length=255,
        label="Title for column two",
        help_text="Column name, e.g.: Author(s)",
    )

    column_three = blocks.CharBlock(
        max_length=255,
        label="Title for column three",
        help_text="Column name, e.g.: Topic",
    )

    column_four = blocks.CharBlock(
        max_length=255,
        label="Title for column four",
        help_text="Column name, e.g.: Intro",
    )

    springboard_items = blocks.ListBlock(
        SpringboardItemBlock(),
        min_num=1,
    )

    class Meta:
        template = "mozorg/cms/blocks/springboard_block.html"
        icon = "grip"
        label = "Springboard Section"
        label_format = "{heading}"


class DonateBlockSettings(blocks.StructBlock):
    """Settings for the donate block."""

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable (e.g., 'donate', 'support').",
    )

    background_color = blocks.ChoiceBlock(
        choices=[
            ("", "White"),
            ("m24-t-dark", "Dark"),
            ("m24-t-green", "Green"),
            ("m24-t-orange", "Orange"),
            ("m24-t-pink", "Pink"),
            ("m24-t-gray", "Gray"),
        ],
        required=False,
        help_text="What color should the background be?",
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "ID: {anchor_id} - Background: {background_color}"
        form_classname = "compact-form struct-block"


class DonateBlock(blocks.StructBlock):
    """Block for the donate section on the homepage."""

    settings = DonateBlockSettings()

    text_divider = DividerBlock(label="Text")

    heading = blocks.CharBlock(
        max_length=255,
        help_text="Use sentence case.",
    )

    body = blocks.RichTextBlock(
        features=["bold", "link"],
        help_text="Keep this to 2 paragraphs or fewer.",
    )

    image_divider = DividerBlock(label="Image")

    image = ImageChooserBlock(
        help_text="Ideal image size is 1400 x 700. Image will be cropped to a 2:1 aspect ratio.",
    )

    image_alt = blocks.CharBlock(
        max_length=255,
        required=False,
        help_text=(
            "A concise description of the image for someone who can't see it. "
            "See <a href='https://mozmeao.github.io/platform-docs/cms/alt-text/' target='_blank'>alt text guidelines</a> for tips."
        ),
    )

    cta_divider = DividerBlock(label="Call-to-action")

    cta_text = blocks.CharBlock(
        max_length=50,
        label="Link text",
        help_text="Use sentence case (e.g., 'Donate', 'Read more').",
    )

    cta_link = LinkBlock(
        label="Link destination",
    )

    class Meta:
        template = "mozorg/cms/blocks/donate_block.html"
        icon = "grip"
        label = "Donate Section"
        label_format = "{heading}"


class ShowcaseBlockSettings(blocks.StructBlock):
    """Settings for the showcase block."""

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable (e.g., 'showcase', 'support').",
    )

    background_color = blocks.ChoiceBlock(
        choices=[
            ("", "White"),
            ("m24-t-dark", "Dark"),
            ("m24-t-green", "Green"),
            ("m24-t-orange", "Orange"),
            ("m24-t-pink", "Pink"),
            ("m24-t-gray", "Gray"),
        ],
        required=False,
        help_text="What color should the background be?",
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "ID: {anchor_id} - Background: {background_color}"
        form_classname = "compact-form struct-block"


class ShowcaseBlock(blocks.StructBlock):
    """Block for the showcase section on the homepage."""

    settings = ShowcaseBlockSettings()

    text_divider = DividerBlock(label="Text")

    heading = blocks.CharBlock(
        max_length=255,
        help_text="Section heading. Use sentence case.",
    )

    body = blocks.RichTextBlock(
        features=["bold", "link"],
        help_text="Keep this to 2 paragraphs or fewer.",
    )

    image_divider = DividerBlock(label="Image")

    image = ImageChooserBlock(
        help_text="Ideal image size is 1376 * 515.",
    )

    image_alt = blocks.CharBlock(
        max_length=255,
        required=False,
        help_text=(
            "A concise description of the image for someone who can't see it. "
            "See <a href='https://mozmeao.github.io/platform-docs/cms/alt-text/' target='_blank'>alt text guidelines</a> for tips."
        ),
    )

    sub_heading = blocks.CharBlock(
        required=False,
        max_length=255,
        help_text="Section sub heading heading. Use sentence case.",
    )

    two_column_layout = blocks.BooleanBlock(
        required=False,
        default=False,
        label="Make it two column layout",
        inline_form=True,
        help_text="Make the title and body content into a two-column layout.",
    )

    cta_divider = DividerBlock(label="Call-to-action")

    cta_text = blocks.CharBlock(
        required=False,
        max_length=50,
        label="Link text",
        help_text="Use sentence case (e.g., 'Read the report', 'Read more').",
    )

    cta_link = LinkBlock(
        label="Link destination",
    )

    class Meta:
        template = "mozorg/cms/blocks/showcase_block.html"
        icon = "grip"
        label = "Showcase Section"
        label_format = "{heading}"


class GalleryBlockSettings(blocks.StructBlock):
    """Settings for the gallery block."""

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable (e.g., 'news', 'gallery').",
    )

    background_color = blocks.ChoiceBlock(
        choices=[
            ("", "White"),
            ("m24-t-dark", "Dark"),
            ("m24-t-green", "Green"),
            ("m24-t-orange", "Orange"),
            ("m24-t-pink", "Pink"),
            ("m24-t-gray", "Gray"),
        ],
        required=False,
        help_text="What color should the background be?",
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "ID: {anchor_id} - Background: {background_color}"
        form_classname = "compact-form struct-block"


class GalleryTileBlock(blocks.StructBlock):
    """A single tile in the gallery grid."""

    width = blocks.ChoiceBlock(
        choices=[
            ("fifth", "Fifth (20%)"),
            ("quarter", "Quarter (25%)"),
            ("third", "Third (33%)"),
            ("half", "Half (50%)"),
            ("three-quarters", "Three-quarters (75%)"),
        ],
        default="half",
        help_text="Width of the tile in the gallery grid at desktop sizes.",
    )

    link_divider = DividerBlock(label="Link")

    cta_link = LinkBlock(
        label="Link destination",
    )

    image_divider = DividerBlock(label="Image")

    image = ImageChooserBlock(
        help_text=(
            "Upload a 2:1 aspect ratio image at 1400×700px - this is displayed on mobile browsers. "
            "Wagtail will crop it for displaying at your chosen aspect ratios for desktop."
        ),
    )

    image_ratio = blocks.ChoiceBlock(
        choices=[
            ("2:1", "2:1 Wide landscape"),
            ("1:1", "1:1 Square"),
            ("5:4", "5:4 Landscape"),
            ("4:5", "4:5 Portrait"),
            ("2:3", "2:3 Tall portrait"),
        ],
        default="2:1",
        help_text="Aspect ratio for the image on desktop. The image will be cropped to fit.",
    )

    image_alt = blocks.CharBlock(
        max_length=255,
        required=False,
        help_text=(
            "A concise description of the image for someone who can't see it. "
            "See <a href='https://mozmeao.github.io/platform-docs/cms/alt-text/' target='_blank'>alt text guidelines</a> for tips."
        ),
    )

    text_divider = DividerBlock(label="Text")

    tag = blocks.ChoiceBlock(
        choices=[
            ("", "None"),
            ("community", "Community"),
            ("event", "Event"),
            ("impact", "Impact"),
            ("partnership", "Partnership"),
            ("policy", "Policy"),
            ("product", "Product"),
            ("program", "Program"),
            ("project", "Project"),
            ("research", "Research"),
        ],
        required=False,
        default="",
    )

    heading = blocks.CharBlock(
        max_length=255,
        help_text="Use sentence case.",
    )

    body = blocks.TextBlock(
        required=False,
        help_text="Short blurb about what you're linking to.",
    )

    cta_text = blocks.CharBlock(
        max_length=100,
        required=False,
        label="Call to action text (optional)",
        help_text="Use sentence case (e.g., 'Read more', 'Watch now').",
    )

    class Meta:
        icon = "image"
        label = "Gallery Tile"
        label_format = "{heading} ({width})"


class ShowcaseGalleryImageBlock(blocks.StructBlock):
    """A single image with alt text for the gallery."""

    image = ImageChooserBlock()

    image_alt = blocks.CharBlock(
        max_length=255,
        required=False,
        help_text=(
            "A concise description of the image for someone who can't see it. "
            "See <a href='https://mozmeao.github.io/platform-docs/cms/alt-text/' target='_blank'>alt text guidelines</a> for tips."
        ),
    )

    class Meta:
        icon = "image"
        label = "Showcase Gallery Image"
        label_format = "{image}"


class GalleryBlock(blocks.StructBlock):
    """Block for a gallery section with multiple tiles."""

    settings = GalleryBlockSettings()

    heading = blocks.CharBlock(
        max_length=255,
        required=False,
    )

    intro = blocks.RichTextBlock(
        features=["bold", "link"],
        required=False,
    )

    tiles = blocks.ListBlock(
        GalleryTileBlock(),
        min_num=1,
        help_text="Add gallery tiles. For best results, ensure tile widths add up to 100% per row.",
    )

    class Meta:
        template = "mozorg/cms/blocks/gallery_block.html"
        icon = "grip"
        label = "Gallery Section"
        label_format = "{heading}"


class ShowcaseGalleryBlockSettings(blocks.StructBlock):
    """Settings for the showcase gallery block."""

    anchor_id = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Optional: Add an ID to make this section linkable (e.g., 'news', 'gallery').",
    )

    background_color = blocks.ChoiceBlock(
        choices=[
            ("", "White"),
            ("m24-t-dark", "Dark"),
            ("m24-t-green", "Green"),
            ("m24-t-orange", "Orange"),
            ("m24-t-pink", "Pink"),
            ("m24-t-gray", "Gray"),
        ],
        required=False,
        help_text="What color should the background be?",
    )

    class Meta:
        icon = "cog"
        collapsed = True
        label = "Settings"
        label_format = "ID: {anchor_id} - Background: {background_color}"
        form_classname = "compact-form struct-block"


class ShowcaseGalleryBlock(blocks.StructBlock):
    """A showcase block with a gallery as media."""

    settings = ShowcaseGalleryBlockSettings()

    text_divider = DividerBlock(label="Text")

    heading = blocks.CharBlock(
        required=False,
        max_length=255,
        help_text="Use sentence case.",
    )

    image_divider = DividerBlock(label="Image")

    tiles = blocks.ListBlock(
        ShowcaseGalleryImageBlock(),
        min_num=1,
        help_text="Add gallery tiles. For best results, ensure tile widths add up to 100% per row.",
    )

    body = blocks.CharBlock(
        max_length=1000,
        label="Content for section body",
        help_text="Use sentence case.",
    )

    cta_text = blocks.CharBlock(
        required=False,
        max_length=50,
        label="Link text",
        help_text="Use sentence case (e.g., 'Read the report', 'Read more').",
    )

    cta_link = LinkBlock(
        label="Link destination",
    )

    class Meta:
        template = "mozorg/cms/blocks/showcase_gallery_block.html"
        icon = "grip"
        label = "Showcase Gallery section"
        label_format = "{heading}"
