# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from django.conf import settings
from django.db import models, transaction

SITEMAPS_DATA = settings.SITEMAPS_PATH.joinpath("data")
NO_LOCALE = "__"  # special value for no locale


def load_sitemaps_data():
    with SITEMAPS_DATA.joinpath("etags.json").open() as fh:
        etags = json.load(fh)

    with SITEMAPS_DATA.joinpath("sitemap.json").open() as fh:
        sitemap = json.load(fh)

    return sitemap, etags


def get_sitemap_objs():
    objs = []
    sitemap, etags = load_sitemaps_data()
    for url, locales in sitemap.items():
        if not locales:
            locales = [NO_LOCALE]

        for locale in locales:
            if locale == NO_LOCALE:
                full_url = f"{settings.CANONICAL_URL}{url}"
            else:
                full_url = f"{settings.CANONICAL_URL}/{locale}{url}"

            kwargs = {"path": url, "locale": locale}
            etag = etags.get(full_url)
            if etag:
                kwargs["lastmod"] = etag["date"]
            objs.append(SitemapURL(**kwargs))

    return objs


class SitemapURLManager(models.Manager):
    def refresh(self):
        with transaction.atomic(using=self.db):
            self.all().delete()
            self.bulk_create(get_sitemap_objs())

    def all_for_locale(self, locale):
        return self.filter(locale=locale).order_by("path")

    def all_locales(self):
        return self.values_list("locale", flat=True).distinct().order_by("locale")


class SitemapURL(models.Model):
    path = models.CharField(max_length=200)
    locale = models.CharField(max_length=5)
    lastmod = models.CharField(max_length=40, blank=True)

    objects = SitemapURLManager()

    def __str__(self):
        if self.has_locale:
            return f"/{self.locale}{self.path}"
        else:
            return self.path

    def get_absolute_url(self):
        return f"{settings.CANONICAL_URL}{self}"

    @property
    def has_locale(self):
        return self.locale != NO_LOCALE
