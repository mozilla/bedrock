# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from bedrock.cms.models.pages import ArticleDetailPageBase, ArticleIndexPageBase
from bedrock.products.views import vpn_available


class VPNCallToActionSnippet(models.Model):
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

    def __str__(self):
        return self.heading


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
        context = super().get_context(request)
        vpn_available_in_country = vpn_available(request)
        article_data = VPNResourceCenterDetailPage.objects.live().public()

        first_article_group, second_article_group = (
            article_data[:ARTICLE_GROUP_SIZE],
            article_data[ARTICLE_GROUP_SIZE:],
        )

        context["first_article_group"] = first_article_group
        context["ftl_files"] = ["products/vpn/resource-center", "products/vpn/shared"]
        context["second_article_group"] = second_article_group
        context["vpn_available"] = vpn_available_in_country
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
        context = super().get_context(request)
        vpn_available_in_country = vpn_available(request)
        context["ftl_files"] = ["products/vpn/resource-center", "products/vpn/shared"]
        context["vpn_available"] = vpn_available_in_country
        return context
