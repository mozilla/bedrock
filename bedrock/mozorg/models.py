# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction

import markdown
from markdown.extensions.toc import TocExtension
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet

from bedrock.cms.models.base import AbstractBedrockCMSPage
from bedrock.mozorg.blocks.advertising import (
    AdvertisingHeroBlock,
    SectionBlock,
    TwoColumnDetailBlock,
)
from bedrock.mozorg.blocks.anonym import (
    CallToActionBlock as AnonymCallToActionBlock,
    SectionBlock as AnonymSectionBlock,
)
from bedrock.mozorg.blocks.leadership import LeadershipSectionBlock
from bedrock.mozorg.blocks.navigation import NavigationLinkBlock


def process_md_file(file_path):
    try:
        # Parse the Markdown file
        with open(str(file_path)) as f:
            input = f.read()

        md = markdown.Markdown(
            extensions=[
                "markdown.extensions.attr_list",
                TocExtension(permalink=True, baselevel=2, toc_depth="2-3", separator=""),
            ],
            output_format="html5",
        )
        content = md.convert(input)
    except OSError:
        content = ""

    return content, md.toc


class WebvisionDocsManager(models.Manager):
    def refresh(self):
        doc_objs = []
        errors = 0
        docs_path = settings.WEBVISION_DOCS_PATH
        with transaction.atomic(using=self.db):
            self.all().delete()
            doc_files = docs_path.glob("input/*.md")
            for f in doc_files:
                name = f.stem
                content, toc = process_md_file(f)
                if not content:
                    errors += 1
                    continue

                doc_objs.append(WebvisionDoc(name=name, content={"content": content, "toc": toc}))
            self.bulk_create(doc_objs)

        return len(doc_objs), errors


class WebvisionDoc(models.Model):
    name = models.CharField(max_length=100)
    content = models.JSONField()

    objects = WebvisionDocsManager()

    def __str__(self):
        return self.name


@register_snippet
class ContactBannerSnippet(TranslatableMixin):
    heading = models.CharField(
        max_length=255,
        blank=False,
    )
    image = models.ForeignKey(
        "cms.BedrockImage",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    button_text = models.CharField(
        verbose_name="Link Text",
        max_length=255,
        blank=False,
    )
    button_link = models.URLField(
        verbose_name="Link URL",
        blank=False,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel(
                    "heading",
                    heading="Heading",
                ),
                FieldPanel("image", heading="Image"),
                FieldRowPanel(
                    [
                        FieldPanel("button_text", heading="Button text"),
                        FieldPanel("button_link", heading="Button link"),
                    ]
                ),
            ],
            heading="Contact Banner Block",
        ),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Contact Banner Snippet"
        verbose_name_plural = "Contact Banner Snippets"

    def __str__(self):
        return f"{self.heading} - Contact Banner Snippet"


@register_snippet
class NotificationSnippet(models.Model):
    notification_text = models.CharField(
        max_length=255,
        blank=False,
    )
    linkedin_link = models.URLField(
        max_length=255,
        blank=True,
    )
    tiktok_link = models.URLField(
        max_length=255,
        blank=True,
    )
    spotify_link = models.URLField(
        max_length=255,
        blank=True,
    )
    bluesky_link = models.URLField(
        max_length=255,
        blank=True,
    )
    instagram_link = models.URLField(
        max_length=255,
        blank=True,
    )
    youtube_link = models.URLField(
        max_length=255,
        blank=True,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel(
                    "notification_text",
                    heading="Notification Text",
                ),
                FieldPanel("linkedin_link", heading="Linkedin Link"),
                FieldPanel("tiktok_link", heading="Tiktok Link"),
                FieldPanel("spotify_link", heading="Spotify Link"),
                FieldPanel("bluesky_link", heading="Bluesky Link"),
                FieldPanel("instagram_link", heading="Instagram Link"),
                FieldPanel("youtube_link", heading="Youtube Link"),
            ],
            heading="Notifications Block",
        ),
    ]

    def __str__(self):
        return f"{self.notification_text} - Notification Snippet"


class LeadershipPage(AbstractBedrockCMSPage):
    max_count = 1  # Ensure there's only one instance of this page
    subpage_types = []  # This page type cannot have any children

    leadership_sections = StreamField(
        [("section", LeadershipSectionBlock())],
        blank=True,
        null=True,
        collapsed=True,
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("leadership_sections"),
    ]

    template = "mozorg/cms/about/leadership.html"


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

    template = "mozorg/cms/advertising/advertising_index_page.html"

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

    template = "mozorg/cms/advertising/two_column_subpage.html"


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

    template = "mozorg/cms/advertising/content_subpage.html"


class AnonymIndexPage(AbstractBedrockCMSPage):
    subpage_types = ["AnonymTopAndBottomPage", "AnonymContentSubPage"]

    content = StreamField(
        [
            ("section", AnonymSectionBlock()),
            ("call_to_action", AnonymCallToActionBlock()),
        ],
        blank=True,
        null=True,
        collapsed=True,
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("content"),
    ]

    template = "mozorg/cms/anonym/anonym_index_page.html"


class AnonymTopAndBottomPage(AbstractBedrockCMSPage):
    parent_page_types = ["AnonymIndexPage"]
    subpage_types = []

    top_content = StreamField(
        [
            ("section", AnonymSectionBlock()),
            ("call_to_action", AnonymCallToActionBlock()),
        ],
        blank=True,
        null=True,
        collapsed=True,
    )
    bottom_content = StreamField(
        [
            ("section", AnonymSectionBlock()),
            ("call_to_action", AnonymCallToActionBlock()),
        ],
        blank=True,
        null=True,
        collapsed=True,
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("top_content"),
        FieldPanel("bottom_content"),
    ]

    template = "mozorg/cms/anonym/anonym_top_and_bottom_page.html"


class AnonymContentSubPage(AbstractBedrockCMSPage):
    parent_page_types = ["AnonymIndexPage"]
    subpage_types = []

    content = StreamField(
        [
            ("section", AnonymSectionBlock()),
            ("call_to_action", AnonymCallToActionBlock()),
        ],
        blank=True,
        null=True,
        collapsed=True,
    )
    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("content"),
    ]

    template = "mozorg/cms/anonym/anonym_content_sub_page.html"
