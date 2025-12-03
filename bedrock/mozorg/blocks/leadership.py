# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.template.defaultfilters import slugify as django_slugify

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class LeadershipHeadshotBlock(blocks.StructBlock):
    """Block for a leadership bio headshot image and (optional) photos link."""

    image = ImageChooserBlock(
        help_text="A headshot image of the person.",
    )

    image_alt_text = blocks.CharBlock(
        char_max_length=255,
        help_text="Alt text for the headshot image.",
    )

    photos_link = blocks.URLBlock(
        required=False,
        char_max_length=255,
        help_text="External link to a .zip file of photos of the person.",
    )

    class Meta:
        icon = "image"
        label = "Headshot image"


class LeadershipExternalLinkBlock(blocks.StructBlock):
    """Block for a leadership bio external link, such as a website or social media account."""

    url = blocks.URLBlock(
        required=False,
        char_max_length=255,
        help_text="Link to the person's website or social media account.",
    )

    type = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("url mastodon", "Mastodon"),
            ("url twitter", "Twitter"),
            ("url website", "Website"),
        ],
        help_text="Selects a visual icon type for the link.",
    )

    text = blocks.CharBlock(
        required=False,
        char_max_length=255,
        help_text="Text to display for the link.",
    )

    class Meta:
        icon = "link"
        label = "External Link"


class LeadershipBioID(blocks.StructValue):
    """ID Value class for LeadershipBioBlock. Used for page anchor links."""

    @property
    def id(self):
        name = self.get("name")
        return django_slugify(name)


class LeadershipBioBlock(blocks.StructBlock):
    """Block for a leadership bio."""

    name = blocks.CharBlock(
        char_max_length=255,
        placeholder="Enter the person's full name.",
    )

    headshot = LeadershipHeadshotBlock()

    job_title = blocks.CharBlock(
        required=False,
        char_max_length=255,
    )

    biography = blocks.RichTextBlock(
        required=False,
        help_text="A biography limited to a few short paragraphs. Links and formatting are supported.",
        features=settings.WAGTAIL_RICHTEXT_FEATURES_FULL,
    )

    external_links = blocks.ListBlock(
        LeadershipExternalLinkBlock(),
        min_num=0,
        max_num=5,
    )

    class Meta:
        value_class = LeadershipBioID
        template = "mozorg/cms/about/blocks/leadership_block.html"
        icon = "user"
        label = "Leadership Profile"


class LeadershipGroupBlock(blocks.StructBlock):
    """Block for a leadership group."""

    title = blocks.CharBlock(
        char_max_length=255,
        help_text="Leadership group title, e.g. 'Executive Steering Committee' or 'Senior Leadership'.",
        required=False,
    )

    description = blocks.CharBlock(
        char_max_length=1000,
        help_text="A couple of sentences describes what the group is and some helpful context.",
        required=False,
    )

    leaders = blocks.ListBlock(
        LeadershipBioBlock(),
        min_num=1,
    )

    class Meta:
        icon = "group"


class LeadershipSectionID(blocks.StructValue):
    """ID Value class for LeadershipSectionBlock. Used for page anchor links."""

    @property
    def id(self):
        name = self.get("title")
        return django_slugify(name)


class LeadershipSectionBlock(blocks.StructBlock):
    """Block for a leadership section containing a title and one or more leadership groups."""

    title = blocks.CharBlock(
        max_length=255, blank=True, null=True, help_text="Title for the section of the page e.g. 'Mozilla Corporation' or 'Mozilla Foundation."
    )

    description = blocks.CharBlock(
        char_max_length=1000,
        help_text="Description for the leadership section.",
        required=False,
    )

    leadership_group = blocks.ListBlock(
        LeadershipGroupBlock(),
        min_num=1,
    )

    class Meta:
        value_class = LeadershipSectionID
        icon = "group"
