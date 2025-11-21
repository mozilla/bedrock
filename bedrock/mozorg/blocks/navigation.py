# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.exceptions import ValidationError

from wagtail import blocks
from wagtail.blocks import StructValue
from wagtail_link_block.blocks import LinkBlock


class NavigationLinkValue(StructValue):
    """Custom StructValue for NavigationLinkBlock with URL resolution."""

    def get_resolved_url(self, anchor_page_url=""):
        """Return the resolved URL for this navigation link."""
        link = self.get("link")
        if link.get("link_to") == "anchor":
            return f"{anchor_page_url}{link.get_url()}"
        elif link:
            return link.get_url()
        return None


class NavigationLinkBlock(blocks.StructBlock):
    """A navigation link for sub-navigation menu."""

    link_text = blocks.CharBlock(
        max_length=50,
        help_text="Text to display for this navigation link",
    )

    link = LinkBlock()

    has_button_appearance = blocks.BooleanBlock(
        required=False,
        default=False,
        help_text="This link should look like a button",
    )

    def clean(self, value):
        errors = {}
        link = value.get("link", {})

        # Validate that the appropriate field is filled based on link_type
        if link.get("link_to") == "anchor":
            if not link.get("anchor"):
                errors["link"] = ValidationError("Section anchor is required when linking to a section")

        if errors:
            raise blocks.StructBlockValidationError(errors)

        return super().clean(value)

    class Meta:
        icon = "link"
        label = "Navigation Link"
        value_class = NavigationLinkValue
