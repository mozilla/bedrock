# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.exceptions import ValidationError
from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from bedrock.advertising.blocks import (
    AdvertisingHeroBlock,
    SectionBlock,
    TwoColumnDetailBlock,
)
from bedrock.cms.models.base import AbstractBedrockCMSPage
from bedrock.mozorg.blocks.navigation import NavigationLinkBlock


class AdvertisingIndexPage(AbstractBedrockCMSPage):
    subpage_types = ["AdvertisingTwoColumnSubpage", "ContentSubpage"]

    sub_navigation = StreamField(
        [("link", NavigationLinkBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        help_text="Configure the sub-navigation menu items. Leave empty to use the default navigation.",
    )
    hero = StreamField(
        [("advertising_hero_block", AdvertisingHeroBlock())],
        blank=True,
        null=True,
        max_num=1,
        collapsed=True,
        use_json_field=True,
    )
    sections = StreamField(
        [
            ("section", SectionBlock()),
        ],
        blank=True,
        null=True,
        collapsed=True,
    )
    contact_banner = models.ForeignKey(
        "mozorg.ContactBannerSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    notification = models.ForeignKey(
        "mozorg.NotificationSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("hero"),
        FieldPanel("sections"),
        FieldPanel("contact_banner"),
        FieldPanel("notification"),
    ]
    settings_panels = AbstractBedrockCMSPage.settings_panels + [
        FieldPanel("sub_navigation"),
    ]

    template = "advertising/advertising_index_page.html"

    def clean(self):
        """
        Validate that:
        1. Anchor IDs in content blocks are unique
        2. Sub-navigation links reference valid sections
        """
        super().clean()

        # Get available section anchors and check for duplicates
        available_sections = []
        for block in self.hero:
            anchor_id = block.value.get("anchor_id")
            if anchor_id:
                available_sections.append(anchor_id)
        for block in self.sections:
            # SectionBlock has anchor_id nested under settings
            settings = block.value.get("settings", {})
            anchor_id = settings.get("anchor_id") if settings else None

            if anchor_id:
                available_sections.append(anchor_id)

            # Also, check for an anchor id in the section's header.
            header_anchor_id = block.value.get("header").get("anchor_id")
            if header_anchor_id:
                available_sections.append(header_anchor_id)

            # Also, check for anchor ids in each block of the sections' content.
            for section_block in block.value.get("content"):
                section_block_anchor_id = section_block.value.get("anchor_id")
                if section_block_anchor_id:
                    available_sections.append(section_block_anchor_id)

        # Check for duplicate anchor IDs
        if len(available_sections) != len(set(available_sections)):
            # Find duplicates
            seen = set()
            duplicates = set()
            for anchor_id in available_sections:
                if anchor_id in seen:
                    duplicates.add(anchor_id)
                seen.add(anchor_id)

            raise ValidationError(f"Duplicate anchor ID(s) found: {', '.join(sorted(duplicates))}. Each anchor ID must be unique.")

        # Validate navigation links reference valid sections
        if self.sub_navigation:
            available_sections_set = set(available_sections)
            invalid_anchors = []
            for nav_item in self.sub_navigation:
                link = nav_item.value.get("link", {})
                if link.get("link_to") == "anchor":
                    anchor = link.get("anchor", "")
                    if anchor and anchor not in available_sections_set:
                        invalid_anchors.append(anchor)

            if invalid_anchors:
                available_text = ", ".join(available_sections) if available_sections else "None"
                invalid_text = ", ".join(invalid_anchors)
                raise ValidationError(f"Navigation links reference unknown section(s): '{invalid_text}'. Available sections: {available_text}")

    class Meta:
        verbose_name = "Advertising Index Page"
        db_table = "mozorg_advertisingindexpage"  # CRITICAL: Keep old table name!


class AdvertisingTwoColumnSubpage(AbstractBedrockCMSPage):
    parent_page_types = ["AdvertisingIndexPage"]
    subpage_types = []  # This page type cannot have any children

    content = StreamField(
        [
            ("two_column_block", TwoColumnDetailBlock()),
        ],
        blank=True,
        null=True,
        collapsed=True,
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("content"),
    ]

    template = "advertising/two_column_subpage.html"

    class Meta:
        verbose_name = "Advertising Two Column Subpage"
        db_table = "mozorg_advertisingtwocolumnsubpage"  # CRITICAL: Keep old table name!


class ContentSubpage(AbstractBedrockCMSPage):
    parent_page_types = ["AdvertisingIndexPage"]
    subpage_types = []  # This page type cannot have any children

    sections = StreamField(
        [
            ("section", SectionBlock()),
        ],
        blank=True,
        null=True,
        collapsed=True,
    )

    contact_banner = models.ForeignKey(
        "mozorg.ContactBannerSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    notification = models.ForeignKey(
        "mozorg.NotificationSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("sections"),
        FieldPanel("contact_banner"),
        FieldPanel("notification"),
    ]

    template = "advertising/content_subpage.html"

    class Meta:
        verbose_name = "Content Subpage"
        db_table = "mozorg_contentsubpage"  # CRITICAL: Keep old table name!
