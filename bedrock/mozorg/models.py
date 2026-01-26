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
from bedrock.mozorg.blocks.common import DonateBlock, GalleryBlock, TransitionBlock
from bedrock.mozorg.blocks.leadership import LeadershipSectionBlock
from bedrock.mozorg.blocks.navigation import NavigationLinkBlock

BASE_UTM_PARAMETERS = {
    "utm_source": "www.mozilla.org",
    "utm_medium": "referral",
}


class SubNavigationMixin:
    """
    Mixin for pages with navigation that validates anchor IDs.

    Pages using this mixin should:
    1. Have a navigation StreamField (defaults to 'sub_navigation', configurable via navigation_field_name)
    2. Implement get_available_sections() to return a list of all anchor IDs
    """

    navigation_field_name = "sub_navigation"

    def get_available_sections(self):
        """
        Return a list of all anchor IDs available in the page's content.
        Subclasses should override this method to collect anchor IDs from their specific content fields.
        """
        raise NotImplementedError("Subclasses must implement get_available_sections()")

    def clean(self):
        """
        Validate that:
        1. Anchor IDs in content blocks are unique
        2. Navigation links reference valid sections
        """
        super().clean()

        # Get available section anchors
        available_sections = self.get_available_sections()

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
        navigation_field = getattr(self, self.navigation_field_name, None)
        if navigation_field:
            available_sections_set = set(available_sections)
            invalid_anchors = []
            for nav_item in navigation_field:
                link = nav_item.value.get("link", {})
                if link.get("link_to") == "anchor":
                    anchor = link.get("anchor", "")
                    if anchor and anchor not in available_sections_set:
                        invalid_anchors.append(anchor)

            if invalid_anchors:
                available_text = ", ".join(available_sections) if available_sections else "None"
                invalid_text = ", ".join(invalid_anchors)
                raise ValidationError(f"Navigation links reference unknown section(s): '{invalid_text}'. Available sections: {available_text}")


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


class AdvertisingIndexPage(SubNavigationMixin, AbstractBedrockCMSPage):
    subpage_types = ["AdvertisingTwoColumnSubpage", "ContentSubpage"]
    navigation_field_name = "sub_navigation"

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

    def get_available_sections(self):
        """Collect all anchor IDs from hero and sections."""
        available_sections = []

        # Check hero blocks
        for block in self.hero:
            anchor_id = block.value.get("anchor_id")
            if anchor_id:
                available_sections.append(anchor_id)

        # Check section blocks
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

        return available_sections


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


class HomePage(AbstractBedrockCMSPage):
    """CMS-managed homepage for mozilla.org."""

    max_count = 1  # Ensure there's only one instance of this page
    subpage_types = []  # This page type cannot have any children
    ftl_files = ["mozorg/home-m24"]

    content = StreamField(
        [
            ("donate_block", DonateBlock()),
            ("gallery_block", GalleryBlock()),
            ("transition_block", TransitionBlock()),
        ],
        blank=True,
        null=True,
        use_json_field=True,
        help_text="Add content blocks for the homepage. Blocks will render in the order shown.",
    )

    content_panels = [
        FieldPanel("title", help_text="Help identify this page for other editors."),
        FieldPanel("content"),
    ]

    template = "mozorg/cms/home/home.html"

    def get_utm_parameters(self):
        return {
            **BASE_UTM_PARAMETERS,
            "utm_campaign": self.slug or "homepage",
        }

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["utm_parameters"] = self.get_utm_parameters()
        return context
