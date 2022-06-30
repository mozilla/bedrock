# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import re
from pathlib import Path

from django.conf import settings
from django.db import models, transaction

from django_extensions.db.fields.json import JSONField
from markupsafe import Markup

from bedrock.base.urlresolvers import reverse

URL_RE = re.compile(r"^https?://", re.I)


def get_page_content_cards(page_name, locale):
    return ContentCard.objects.get_page_cards(page_name, locale)


def get_data_from_file_path(file_path):
    card_name, locale = file_path.stem.split(".")
    page_name = file_path.parts[-2]
    page_id = f"{page_name}-{locale}-{card_name}"
    return {
        "locale": locale,
        "card_name": card_name,
        "page_name": page_name,
        "page_id": page_id,
    }


class ContentCardManager(models.Manager):
    def get_card(self, page_name, name, locale="en-US"):
        card_id = f"{page_name}-{locale}-{name}"
        return self.get(id=card_id)

    def get_page_cards(self, page_name, locale="en-US"):
        cards = self.filter(page_name=page_name, locale=locale)
        return {c.card_name: c.card_data for c in cards}

    def refresh(self):
        card_objs = []
        cc_path = Path(settings.CONTENT_CARDS_PATH, "content")
        with transaction.atomic(using=self.db):
            self.all().delete()
            cc_files = cc_path.glob("*/*.json")
            for ccf in cc_files:
                path_data = get_data_from_file_path(ccf)
                with ccf.open(encoding="utf-8") as ccfo:
                    data = json.load(ccfo)

                card_objs.append(
                    ContentCard(
                        id=path_data["page_id"],
                        card_name=path_data["card_name"],
                        page_name=path_data["page_name"],
                        locale=path_data["locale"],
                        content=data.pop("html_content", ""),
                        data=data,
                    )
                )
            self.bulk_create(card_objs)

        return len(card_objs)


class ContentCard(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    card_name = models.CharField(max_length=100)
    page_name = models.CharField(max_length=100)
    locale = models.CharField(max_length=10)
    content = models.TextField(blank=True)
    data = JSONField()

    objects = ContentCardManager()

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.card_name} ({self.locale})"

    @property
    def html(self):
        return Markup(self.content)

    @property
    def card_data(self):
        """Return a dict appropriate for calling the card() macro"""
        data = {}
        data.update(self.data)
        if "image" in data:
            data["image_url"] = f"{settings.CONTENT_CARDS_URL}contentcards/img/{data['image']}"
            del data["image"]

        if "highres_image" in data:
            data["highres_image_url"] = f"{settings.CONTENT_CARDS_URL}contentcards/img/{data['highres_image']}"
            del data["highres_image"]

        if "ga_title" not in data:
            data["ga_title"] = data["title"]

        if "media_icon" in data:
            data["media_icon"] = f"mzp-has-{data['media_icon']}"

        if "aspect_ratio" in data:
            data["aspect_ratio"] = f"mzp-has-aspect-{data['aspect_ratio']}"

        if "size" in data:
            data["class"] = f"mzp-c-card-{data['size']}"
            del data["size"]

        if "link_url" in data and not URL_RE.match(data["link_url"]):
            data["link_url"] = reverse(data["link_url"])

        return data
