# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock


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


class LeadershipProfileChooserBlock(blocks.StructBlock):
    """Block for placing a LeadershipProfileSnippet with an optional per-placement job title."""

    profile = SnippetChooserBlock("mozorg.LeadershipProfileSnippet")

    job_title = blocks.CharBlock(
        required=False,
        max_length=255,
        help_text="Job title to display for this placement. Leave blank to omit.",
    )

    class Meta:
        icon = "user"
        label = "Leadership Profile"


class LeadershipGroupSnippetBlock(blocks.StructBlock):
    """Block for a leadership group that references LeadershipProfileSnippets."""

    title = blocks.CharBlock(
        char_max_length=255,
        help_text="Leadership group title, e.g. 'Executive Steering Committee' or 'Senior Leadership'.",
        required=False,
    )

    description = blocks.CharBlock(
        char_max_length=1000,
        help_text="A couple of sentences describing what the group is and some helpful context.",
        required=False,
    )

    leaders = blocks.ListBlock(
        LeadershipProfileChooserBlock(),
        min_num=1,
    )

    closing = blocks.RichTextBlock(
        required=False,
        help_text="Optional closing text displayed after the list of leaders.",
        features=settings.WAGTAIL_RICHTEXT_FEATURES_FULL,
    )

    class Meta:
        icon = "group"
        label = "Leadership Group"
