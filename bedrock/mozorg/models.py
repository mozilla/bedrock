# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.db import models, transaction

import markdown
from markdown.extensions.toc import TocExtension
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet

from bedrock.cms.models.base import AbstractBedrockCMSPage
from bedrock.mozorg.blocks.advertising import AdvertisingHeroBlock, FeatureListBlock, FigureWithStatisticBlock, SectionHeaderBlock
from bedrock.mozorg.blocks.leadership import LeadershipSectionBlock


def process_md_file(file_path):
    try:
        # Parse the Markdown file
        with open(str(file_path)) as f:
            input = f.read()

        md = markdown.Markdown(
            extensions=["markdown.extensions.attr_list", TocExtension(permalink=True, baselevel=2, toc_depth="2-3", separator="")],
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
    subpage_types = ["AdvertisingPrinciplesPage"]

    content = StreamField(
        [
            ("advertising_hero_block", AdvertisingHeroBlock()),
            ("section_header_block", SectionHeaderBlock()),
            ("figure_with_statistic_block", FigureWithStatisticBlock()),
            ("feature_list_block", FeatureListBlock()),
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
    notification_text = RichTextField(
        blank=True,
        features=["bold", "italic", "superscript", "subscript", "strikethrough", "code", "link"],
    )

    content_panels = AbstractBedrockCMSPage.content_panels + [
        FieldPanel("content"),
        FieldPanel("contact_banner"),
        FieldPanel("notification_text"),
    ]

    template = "mozorg/cms/advertising/advertising_index_page.html"


class AdvertisingPrinciplesPage(AbstractBedrockCMSPage):
    subpage_types = []  # This page type cannot have any children

    template = "mozorg/cms/advertising/advertising_principles_page.html"
