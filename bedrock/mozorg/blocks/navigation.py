# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.exceptions import ValidationError

from wagtail import blocks


class NavigationLinkBlock(blocks.StructBlock):
    """A navigation link for sub-navigation menu."""

    link_text = blocks.CharBlock(
        max_length=50,
        help_text="Text to display for this navigation link",
    )

    link_type = blocks.ChoiceBlock(
        choices=[
            ("section", "Link to section on advertising index Page"),
            ("page", "Internal Page"),
            ("external", "External URL"),
        ],
        help_text="Choose the type of link",
    )

    # For section links - editor manually enters the anchor ID
    section_anchor = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text="Enter the Anchor ID from one of the content sections.",
    )

    internal_page = blocks.PageChooserBlock(
        required=False,
        help_text="Choose an internal page to link to",
    )

    external_url = blocks.URLBlock(
        required=False,
        max_length=255,
        help_text="Full URL for external links",
    )

    has_button_appearance = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text="This link should look like a button",
    )

    def clean(self, value):
        errors = {}
        link_type = value.get("link_type")

        # Validate that the appropriate field is filled based on link_type
        if link_type == "section":
            if not value.get("section_anchor"):
                errors["section_anchor"] = ValidationError("Section anchor is required when linking to a section")
        elif link_type == "page":
            if not value.get("internal_page"):
                errors["internal_page"] = ValidationError("Internal page is required when linking to a page")
        elif link_type == "external":
            if not value.get("external_url"):
                errors["external_url"] = ValidationError("External URL is required when linking to an external URL")

        if errors:
            raise blocks.StructBlockValidationError(errors)

        return super().clean(value)

    class Meta:
        icon = "link"
        label = "Navigation Link"
