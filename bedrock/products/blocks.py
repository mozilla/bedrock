# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models

import wagtail.blocks as blocks
from wagtail.images.blocks import ImageChooserBlock


class SplitBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255, null=True, blank=False)

    content = blocks.RichTextBlock(blank=True, features=["bold", "italic", "link", "ul", "ol"])

    button_text = blocks.CharBlock(verbose_name="Button Text", max_length=255, null=True, blank=False)

    button_link = blocks.URLBlock(verbose_name="Button URL", null=True, blank=False)

    image = ImageChooserBlock()

    class Meta:
        template = "products/monitor/cms/blocks/split.html"
        icon = "image"
        label = "Split Block"

    def __str__(self):
        return f"{self.heading} - Split Block"
