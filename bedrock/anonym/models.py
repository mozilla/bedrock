# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet

from bedrock.anonym.blocks import (
    CallToActionBlock as AnonymCallToActionBlock,
    CheckboxGroupFieldBlock,
    CompetitorComparisonTableBlock as AnonymCompetitorComparisonTableBlock,
    EmailFieldBlock,
    PhoneFieldBlock,
    SectionBlock as AnonymSectionBlock,
    SelectFieldBlock,
    StatItemBlock,
    TextFieldBlock,
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


class AnonymNewsItemPage(AbstractBedrockCMSPage):
    """News item page for Anonym."""

    parent_page_types = ["AnonymNewsPage"]
    subpage_types = []

    description = models.TextField(
        blank=True,
        help_text="Description of the news item",
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Category (e.g., 'Press', 'Blog')",
    )
    logo = models.ForeignKey(
        "cms.BedrockImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Logo (e.g., publication logo like WSJ, NYT)",
    )
    image = models.ForeignKey(
        "cms.BedrockImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image for the news item",
    )
    link = models.URLField(
        blank=True,
        help_text=("External link for this news item. If set, this (Wagtail) page will .not be accessible to users."),
    )
    stats = StreamField(
        [
            ("stat", StatItemBlock()),
        ],
        blank=True,
        null=True,
        use_json_field=True,
        max_num=3,
        help_text="Statistics that will display if this news item is shown on the homepage",
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
        FieldPanel("description"),
        FieldPanel("category"),
        FieldPanel("logo"),
        FieldPanel("image"),
        FieldPanel("link"),
        FieldPanel("stats"),
        FieldPanel("content"),
    ]

    template = "anonym/anonym_news_item_page.html"

    @property
    def exclude_from_sitemap(self):
        """Exclude from sitemap if this is an external link."""
        return bool(self.link)

    class Meta:
        verbose_name = "Anonym News Item Page"
        verbose_name_plural = "Anonym News Item Pages"


class AnonymNewsPage(AnonymStaticPage):
    """Static news page for Anonym."""

    max_count = 1
    subpage_types = ["AnonymNewsItemPage"]
    template = "anonym/anonym_news.html"

    class Meta:
        verbose_name = "Anonym News Page"
        # This database table was originally created in the mozorg app, then
        # the Django model was moved to the anonym app. To preserve data, we
        # refer to the original database table here.
        db_table = "mozorg_anonymnewspage"


class AnonymCaseStudyPage(AnonymStaticPage):
    """Static case study page for Anonym."""

    max_count = 1
    subpage_types = ["AnonymCaseStudyItemPage"]
    template = "anonym/anonym_case_study.html"

    class Meta:
        verbose_name = "Anonym Case Study Page"
        verbose_name_plural = "Anonym Case Study Pages"


class AnonymContactPage(AbstractBedrockCMSPage):
    """Contact page for Anonym."""

    parent_page_types = ["AnonymIndexPage"]
    subpage_types = []
    max_count = 1
    template = "anonym/anonym_contact.html"

    subheading = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional subheading for the contact page",
    )

    form_fields = StreamField(
        [
            ("text_field", TextFieldBlock()),
            ("email_field", EmailFieldBlock()),
            ("phone_field", PhoneFieldBlock()),
            ("select_field", SelectFieldBlock()),
            ("checkbox_group_field", CheckboxGroupFieldBlock()),
        ],
        blank=True,
        null=True,
        use_json_field=True,
        help_text="Define the form fields that will appear on the contact page.",
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("subheading"),
        FieldPanel("form_fields"),
    ]

    class Meta:
        verbose_name = "Anonym Contact Page"
        # This database table was originally created in the mozorg app, then
        # the Django model was moved to the anonym app. To preserve data, we
        # refer to the original database table here.
        db_table = "mozorg_anonymcontactpage"


class AnonymIndexPage(SubNavigationMixin, AbstractBedrockCMSPage):
    subpage_types = ["AnonymTopAndBottomPage", "AnonymContentSubPage", "AnonymNewsPage", "AnonymContactPage", "AnonymCaseStudyPage"]
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
            ("competitor_table", AnonymCompetitorComparisonTableBlock()),
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


class AnonymCaseStudyItemPage(AbstractBedrockCMSPage):
    parent_page_types = ["AnonymCaseStudyPage"]
    subpage_types = []

    logo = models.ForeignKey(
        "cms.BedrockImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Logo or image for the case study (displays in card view)",
    )
    client = models.CharField(
        max_length=255,
        blank=True,
        help_text="Client name (displays as heading in card view)",
    )
    description = models.TextField(
        blank=True,
        help_text="Brief description of the case study (displays in card view)",
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
    notification = models.ForeignKey(
        "mozorg.NotificationSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("logo"),
        FieldPanel("client"),
        FieldPanel("description"),
        FieldPanel("content"),
        FieldPanel("notification"),
    ]

    template = "anonym/anonym_case_study_item_page.html"

    class Meta:
        verbose_name = "Anonym Case Study Item Page"
        # This database table was originally created in the mozorg app, then
        # the Django model was moved to the anonym app. To preserve data, we
        # refer to the original database table here.
        db_table = "mozorg_anonymarticlepage"


@register_snippet
class Person(TranslatableMixin):
    image = models.ForeignKey(
        "cms.BedrockImage",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    name = models.CharField(
        max_length=255,
        blank=False,
    )
    position = models.CharField(
        max_length=255,
        blank=False,
    )
    description = RichTextField(
        blank=True,
    )
    learn_more_link = models.URLField(
        verbose_name="Learn More Link",
        blank=True,
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("image", heading="Image"),
                FieldPanel("name", heading="Name"),
                FieldPanel("position", heading="Position"),
                FieldPanel("description", heading="Description"),
                FieldPanel("learn_more_link", heading="Learn More Link"),
            ],
            heading="Person",
        ),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Person"
        verbose_name_plural = "People"
        # This database table was originally created in the mozorg app, then
        # the Django model was moved to the anonym app. To preserve data, we
        # refer to the original database table here.
        db_table = "mozorg_person"

    def __str__(self):
        return f"{self.name} - {self.position}"
