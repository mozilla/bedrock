# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from bs4 import BeautifulSoup
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel, FieldRowPanel, HelpPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet

from bedrock.cms.models.base import AbstractBedrockCMSPage
from bedrock.cms.models.pages import ArticleDetailPageBase, ArticleIndexPageBase
from bedrock.products.views import vpn_available, vpn_available_mobile_sub_only


class VPNCallToActionSnippet(TranslatableMixin):
    heading = models.CharField(
        max_length=255,
    )

    image = models.ForeignKey(
        "cms.BedrockImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("heading"),
        FieldPanel("image"),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = "VPN Call To Action Snippet"
        verbose_name_plural = "VPN Call To Action Snippets"

    def __str__(self):
        return f"{self.heading} – {self.locale}"


register_snippet(VPNCallToActionSnippet)


class VPNResourceCenterIndexPage(ArticleIndexPageBase):
    call_to_action_middle = models.ForeignKey(
        "products.VPNCallToActionSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    call_to_action_bottom = models.ForeignKey(
        "products.VPNCallToActionSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = ArticleIndexPageBase.content_panels + [
        FieldPanel("call_to_action_middle"),
        FieldPanel("call_to_action_bottom"),
    ]

    subpage_types = ["VPNResourceCenterDetailPage"]

    template = "products/vpn/cms/resource-center/index.html"

    def get_context(self, request, *args, **kwargs):
        ARTICLE_GROUP_SIZE = 6
        context = super().get_context(request, *args, **kwargs)
        vpn_available_in_country = vpn_available(request)
        mobile_sub_only = vpn_available_mobile_sub_only(request)
        article_data = VPNResourceCenterDetailPage.objects.filter(locale=self.locale).live().public().order_by("-first_published_at")

        first_article_group, second_article_group = (
            article_data[:ARTICLE_GROUP_SIZE],
            article_data[ARTICLE_GROUP_SIZE:],
        )

        context["first_article_group"] = first_article_group
        context["ftl_files"] = ["products/vpn/resource-center", "products/vpn/shared"]
        context["second_article_group"] = second_article_group
        context["vpn_available"] = vpn_available_in_country
        context["mobile_sub_only"] = mobile_sub_only
        return context


class VPNResourceCenterDetailPage(ArticleDetailPageBase):
    parent_page_types = ["VPNResourceCenterIndexPage"]

    call_to_action_bottom = models.ForeignKey(
        "products.VPNCallToActionSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = ArticleDetailPageBase.content_panels + [
        FieldPanel("call_to_action_bottom"),
    ]

    template = "products/vpn/cms/resource-center/detail.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        vpn_available_in_country = vpn_available(request)
        context["ftl_files"] = ["products/vpn/resource-center", "products/vpn/shared"]
        context["vpn_available"] = vpn_available_in_country
        return context


@register_snippet
class MonitorCallToActionSnippet(TranslatableMixin):
    split_heading = models.CharField(
        max_length=255,
        blank=False,
    )
    split_subheading = models.CharField(
        max_length=255,
        blank=True,
    )
    split_content = RichTextField(null=True, blank=True, features=settings.WAGTAIL_RICHTEXT_FEATURES_MINIMAL)
    split_button_text = models.CharField(
        verbose_name="Link Text",
        max_length=255,
        blank=False,
    )
    split_button_link = models.URLField(
        verbose_name="Link URL",
        blank=False,
    )
    split_image = models.ForeignKey(
        "cms.BedrockImage",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel(
                    "split_heading",
                    heading="Intro Heading",
                ),
                FieldPanel(
                    "split_subheading",
                    heading="Intro Subheading (optional)",
                ),
                FieldPanel(
                    "split_content",
                    heading="Intro Content (optional)",
                ),
                FieldRowPanel(
                    [
                        FieldPanel("split_button_text", heading="Intro Button text"),
                        FieldPanel("split_button_link", heading="Intro Button link"),
                    ]
                ),
                FieldPanel("split_image", heading="Intro Image"),
            ],
            heading="Intro Block",
        ),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Monitor Call To Action Snippet"
        verbose_name_plural = "Monitor Call To Action Snippets"

    def __str__(self):
        return f"{self.split_heading} - CTA Snippet"


class MonitorArticleIndexPage(AbstractBedrockCMSPage):
    split_heading = models.CharField(
        max_length=255,
        blank=False,
    )
    split_subheading = models.CharField(
        max_length=255,
        blank=True,
    )
    split_content = RichTextField(null=True, blank=True, features=settings.WAGTAIL_RICHTEXT_FEATURES_MINIMAL)
    split_button_text = models.CharField(
        verbose_name="Link Text",
        max_length=255,
        blank=False,
    )
    split_button_link = models.URLField(
        verbose_name="Link URL",
        blank=False,
    )
    split_image = models.ForeignKey(
        "cms.BedrockImage",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    articles_heading = models.CharField(
        max_length=255,
        blank=False,
    )
    articles_subheading = models.CharField(
        max_length=255,
        blank=True,
    )
    call_to_action_bottom = models.ForeignKey(
        "products.MonitorCallToActionSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel(
                    "split_heading",
                    heading="Intro Heading",
                ),
                FieldPanel(
                    "split_subheading",
                    heading="Intro Subheading (optional)",
                ),
                FieldPanel(
                    "split_content",
                    heading="Intro Content (optional)",
                ),
                FieldRowPanel(
                    [
                        FieldPanel("split_button_text", heading="Intro Button text"),
                        FieldPanel("split_button_link", heading="Intro Button link"),
                    ]
                ),
                FieldPanel("split_image", heading="Intro Image"),
            ],
            heading="Intro Split Block",
        ),
        MultiFieldPanel(
            [
                FieldPanel("articles_heading"),
                FieldPanel("articles_subheading"),
            ],
            heading="Article Section Heading",
        ),
        HelpPanel(content="The articles will be linked to here"),
        FieldPanel("call_to_action_bottom"),
    ]

    template = "products/monitor/cms/index.html"

    subpage_types = ["MonitorArticlePage"]  # can only have MonitorArticlePage as children

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["articlepages"] = MonitorArticlePage.objects.live().public().order_by("path")
        return context


class MonitorArticleForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["search_description"].required = True


class MonitorArticlePage(AbstractBedrockCMSPage):
    base_form_class = MonitorArticleForm

    # content panels
    subheading = models.CharField(
        max_length=255,
        blank=True,
    )
    summary = RichTextField(null=True, blank=True, features=settings.WAGTAIL_RICHTEXT_FEATURES_MINIMAL)
    call_to_action_middle = models.ForeignKey(
        "products.MonitorCallToActionSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content = RichTextField(null=True, blank=False, features=settings.WAGTAIL_RICHTEXT_FEATURES_FULL)
    call_to_action_bottom = models.ForeignKey(
        "products.MonitorCallToActionSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("subheading"),
        FieldPanel("summary"),
        FieldPanel("call_to_action_middle"),
        FieldPanel("content"),
        FieldPanel("call_to_action_bottom"),
    ]

    template = "products/monitor/cms/article.html"

    parent_page_types = ["MonitorArticleIndexPage"]  # must be child of MonitorArticleIndexPage

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Parse the HTML content
        soup = BeautifulSoup(self.content, "html.parser")
        # Extract headings and their IDs
        headings = soup.find_all("h2")
        if headings:
            for heading in headings:
                heading["id"] = slugify(heading.text)
            # Add headings to the context
            context["toc"] = headings
        else:
            context["toc"] = []

        return context
