# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from bedrock.anonym.blocks import (
    CallToActionBlock as AnonymCallToActionBlock,
    SectionBlock as AnonymSectionBlock,
    ToggleableItemsBlock as AnonymToggleableItemsBlock,
)
from bedrock.cms.models.base import AbstractBedrockCMSPage
from bedrock.mozorg.blocks.navigation import NavigationLinkBlock
from bedrock.mozorg.models import SubNavigationMixin


class AnonymStaticPage(AbstractBedrockCMSPage):
    """
    Abstract base class for static Anonym pages.
    Subclasses only need to define the template path.
    """

    parent_page_types = ["AnonymIndexPage"]
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Add the parent AnonymIndexPage to context
        context["anonym_index_page"] = self.get_parent().specific
        return context

    class Meta:
        abstract = True


class AnonymNewsPage(AnonymStaticPage):
    """Static news page for Anonym."""

    max_count = 1

    template = "anonym/anonym_news.html"

    class Meta:
        verbose_name = "Anonym News Page"
        # This database table was originally created in the mozorg app, then
        # the Django model was moved to the anonym app. To preserve data, we
        # refer to the original database table here.
        db_table = "mozorg_anonymnewspage"


class AnonymContactPage(AnonymStaticPage):
    """Static contact page for Anonym."""

    max_count = 1

    template = "anonym/anonym_contact.html"

    class Meta:
        verbose_name = "Anonym Contact Page"
        # This database table was originally created in the mozorg app, then
        # the Django model was moved to the anonym app. To preserve data, we
        # refer to the original database table here.
        db_table = "mozorg_anonymcontactpage"


class AnonymIndexPage(SubNavigationMixin, AbstractBedrockCMSPage):
    subpage_types = ["AnonymTopAndBottomPage", "AnonymContentSubPage", "AnonymNewsPage", "AnonymContactPage", "AnonymArticlePage"]
    navigation_field_name = "navigation"

    navigation = StreamField(
        [("link", NavigationLinkBlock())],
        blank=True,
        null=True,
        use_json_field=True,
        help_text="Configure the navigation menu items.",
    )
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
    settings_panels = AbstractBedrockCMSPage.settings_panels + [
        FieldPanel("navigation"),
    ]

    template = "anonym/anonym_index_page.html"

    def get_available_sections(self):
        """Collect all anchor IDs from content blocks."""
        available_sections = []

        for block in self.content:
            # Anchor IDs are nested under settings
            settings = block.value.get("settings", {})
            anchor_id = settings.get("anchor_id") if settings else None
            if anchor_id:
                available_sections.append(anchor_id)

        return available_sections

    class Meta:
        verbose_name = "Anonym Index Page"
        # This database table was originally created in the mozorg app, then
        # the Django model was moved to the anonym app. To preserve data, we
        # refer to the original database table here.
        db_table = "mozorg_anonymindexpage"


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

    template = "anonym/anonym_top_and_bottom_page.html"

    class Meta:
        verbose_name = "Anonym Top And Bottom Page"
        # This database table was originally created in the mozorg app, then
        # the Django model was moved to the anonym app. To preserve data, we
        # refer to the original database table here.
        db_table = "mozorg_anonymtopandbottompage"


class AnonymContentSubPage(AbstractBedrockCMSPage):
    parent_page_types = ["AnonymIndexPage"]
    subpage_types = []

    content = StreamField(
        [
            ("section", AnonymSectionBlock()),
            ("toggle_items", AnonymToggleableItemsBlock()),
            ("call_to_action", AnonymCallToActionBlock()),
        ],
        blank=True,
        null=True,
        collapsed=True,
    )
    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("content"),
    ]

    template = "anonym/anonym_content_sub_page.html"

    class Meta:
        verbose_name = "Anonym Content Subpage"
        # This database table was originally created in the mozorg app, then
        # the Django model was moved to the anonym app. To preserve data, we
        # refer to the original database table here.
        db_table = "mozorg_anonymcontentsubpage"


class AnonymArticlePage(AbstractBedrockCMSPage):
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
    notification = models.ForeignKey(
        "mozorg.NotificationSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("content"),
        FieldPanel("notification"),
    ]

    template = "anonym/anonym_article_page.html"

    class Meta:
        verbose_name = "Anonym Article Page"
        # This database table was originally created in the mozorg app, then
        # the Django model was moved to the anonym app. To preserve data, we
        # refer to the original database table here.
        db_table = "mozorg_anonymarticlepage"
