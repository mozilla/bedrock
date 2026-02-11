# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.shortcuts import redirect
from django.template.loader import render_to_string

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet

from bedrock.anonym.blocks import (
    ArticleBlockquoteBlock,
    ArticleFigureBlock,
    ArticleIntroTextBlock,
    ArticleRichTextBlock,
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


class AbstractStatCardPage(AbstractBedrockCMSPage):
    """Abstract base for pages that can appear in the StatCardListBlock.

    Provides the fields needed by the stat card display: company_name,
    logo, link, and stats.  Title is inherited from Wagtail Page.
    """

    company_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Company or client name",
    )
    logo = models.ForeignKey(
        "cms.BedrockImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Logo image",
    )
    link = models.URLField(
        blank=True,
        help_text="External link",
    )
    stats = StreamField(
        [
            ("stat", StatItemBlock()),
        ],
        blank=True,
        null=True,
        use_json_field=True,
        max_num=3,
        help_text="Statistics to display",
    )

    stat_card_panels = [
        FieldPanel("company_name"),
        FieldPanel("logo"),
        FieldPanel("link"),
        FieldPanel("stats"),
    ]

    class Meta:
        abstract = True


class AnonymNewsItemPage(AbstractStatCardPage):
    """News item page for Anonym."""

    parent_page_types = ["AnonymNewsPage"]
    subpage_types = []

    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this news item at the top of the news page",
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Category (e.g., 'Press', 'Blog')",
    )
    image = models.ForeignKey(
        "cms.BedrockImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image for the news item",
    )
    description = models.TextField(
        blank=True,
        help_text="Description of the news item",
    )
    content = StreamField(
        [
            ("intro_text", ArticleIntroTextBlock()),
            ("rich_text", ArticleRichTextBlock()),
            ("blockquote", ArticleBlockquoteBlock()),
            ("figure", ArticleFigureBlock()),
            ("call_to_action", AnonymCallToActionBlock()),
        ],
        blank=True,
        null=True,
        collapsed=True,
    )

    content_panels = (
        AbstractBedrockCMSPage.content_panels
        + [
            FieldPanel("is_featured"),
        ]
        + AbstractStatCardPage.stat_card_panels
        + [
            FieldPanel("first_published_at"),
            FieldPanel("category"),
            FieldPanel("image"),
            FieldPanel("description"),
            FieldPanel("content"),
        ]
    )

    # Since the concept of a AnonymNewsItemPage is similar to an
    # AnonymCaseStudyItemPage, use the AnonymCaseStudyItemPage template.
    template = "anonym/anonym_case_study_item_page.html"

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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        news_items = AnonymNewsItemPage.objects.child_of(self).live().order_by("-first_published_at")
        featured_item = news_items.filter(is_featured=True).first()
        if featured_item:
            grid_items = news_items.exclude(pk=featured_item.pk)
        else:
            grid_items = news_items
        context["featured_item"] = featured_item
        context["nonfeatured_items"] = grid_items
        return context

    class Meta:
        verbose_name = "Anonym News Page"


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

    to_email_address = models.EmailField(
        help_text="Email address where form submissions will be sent.",
    )

    redirect_to = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.PROTECT,
        related_name="+",
        help_text="Page to redirect to after a successful form submission (e.g. a thank-you page).",
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("subheading"),
        FieldPanel("form_fields"),
    ]

    settings_panels = AbstractBedrockCMSPage.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel("to_email_address"),
                FieldPanel("redirect_to"),
            ],
            heading="Form Submission Settings",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        form_errors = getattr(request, "form_errors", None)
        if form_errors:
            context["form_errors"] = form_errors
        return context

    def serve(self, request, *args, **kwargs):
        if request.method == "POST":
            form_errors = self.validate_form_data(request.POST)
            if form_errors:
                request.form_errors = form_errors
                return super().serve(request, *args, **kwargs)

            self.send_form_email(request)
            return redirect(self.redirect_to.url)

        return super().serve(request, *args, **kwargs)

    def validate_form_data(self, post_data):
        """Validate submitted form data against the field configuration.

        Returns a list of error messages. An empty list means the data is valid.
        """
        # If the honeypot field has data, then form validation fails.
        if post_data.get("office_fax", ""):
            return ["Form submission failed."]

        errors = []
        has_any_data = False

        for field in self.form_fields:
            block_type = field.block_type
            value = field.value
            identifier = value["settings"]["internal_identifier"]
            label = value["label"]
            is_required = value.get("required", False)

            if block_type == "checkbox_group_field":
                submitted = post_data.getlist(identifier)
            else:
                submitted = post_data.get(identifier, "").strip()

            if submitted:
                has_any_data = True

            if is_required and not submitted:
                errors.append(f"{label} is required.")

        if not has_any_data:
            errors.append("Please fill in at least one field.")

        return errors

    def send_form_email(self, request):
        """Collect form data and send it as an email."""
        fields = []
        for field in self.form_fields:
            block_type = field.block_type
            value = field.value
            identifier = value["settings"]["internal_identifier"]
            label = value["label"]

            if block_type == "checkbox_group_field":
                submitted = ", ".join(request.POST.getlist(identifier))
            else:
                submitted = request.POST.get(identifier, "")

            fields.append({"label": label, "value": submitted})

        msg = render_to_string("anonym/emails/contact-form.txt", {"fields": fields})
        subject = f"Contact form submission: {self.title}"
        email = EmailMessage(subject, msg, settings.DEFAULT_FROM_EMAIL, [self.to_email_address])
        email.send()

    class Meta:
        verbose_name = "Anonym Contact Page"


class AnonymIndexPage(SubNavigationMixin, AbstractBedrockCMSPage):
    subpage_types = [
        "AnonymContentSubPage",
        "AnonymNewsPage",
        "AnonymContactPage",
        "AnonymCaseStudyPage",
    ]
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


class AnonymContentSubPage(AbstractBedrockCMSPage):
    parent_page_types = ["AnonymIndexPage"]
    subpage_types = []

    content = StreamField(
        [
            ("section", AnonymSectionBlock()),
            ("competitor_table", AnonymCompetitorComparisonTableBlock()),
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


class AnonymCaseStudyItemPage(AbstractStatCardPage):
    parent_page_types = ["AnonymCaseStudyPage"]
    subpage_types = []

    description = models.TextField(
        blank=True,
        help_text="Brief description of the case study (displays in card view)",
    )

    content = StreamField(
        [
            ("intro_text", ArticleIntroTextBlock()),
            ("rich_text", ArticleRichTextBlock()),
            ("blockquote", ArticleBlockquoteBlock()),
            ("figure", ArticleFigureBlock()),
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

    content_panels = (
        AbstractBedrockCMSPage.content_panels
        + AbstractStatCardPage.stat_card_panels
        + [
            FieldPanel("description"),
            FieldPanel("content"),
            FieldPanel("notification"),
        ]
    )

    template = "anonym/anonym_case_study_item_page.html"

    class Meta:
        verbose_name = "Anonym Case Study Item Page"


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

    def __str__(self):
        return f"{self.name} - {self.position}"
