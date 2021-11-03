# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Dict, List

from django.db import models
from django.utils.timezone import now

from django_extensions.db.fields.json import JSONField


class ContentfulEntryManager(models.Manager):
    def get_page_by_id(self, content_id) -> Dict:
        return self.get(contentful_id=content_id).data

    def get_page_by_slug(self, slug, lang, content_type) -> Dict:
        return self.get(
            slug=slug,
            language=lang,
            content_type=content_type,
        ).data

    def get_entries_by_type(self, content_type, lang, order_by="last_modified") -> List[Dict]:
        qs = self.filter(
            content_type=content_type,
            language=lang,
        ).order_by(order_by)
        return [entry.data for entry in qs]

    def get_page(self, content_type, lang) -> Dict:
        return self.get(
            content_type=content_type,
            language=lang,
        ).data

    def get_homepage(self, lang) -> Dict:
        return self.get(
            content_type="connectHomepage",
            language=lang,
        ).data


class ContentfulEntry(models.Model):
    contentful_id = models.CharField(max_length=20, unique=True)
    content_type = models.CharField(max_length=20)
    language = models.CharField(max_length=5)
    last_modified = models.DateTimeField(default=now)
    url_base = models.CharField(max_length=255, blank=True)
    slug = models.CharField(max_length=255, blank=True)
    data_hash = models.CharField(max_length=64)
    data = JSONField()

    objects = ContentfulEntryManager()

    def __str__(self) -> str:
        return f"ContentfulEntry {self.content_type}:{self.contentful_id}"
