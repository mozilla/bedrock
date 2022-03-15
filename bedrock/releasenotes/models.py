# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import codecs
import json
import os
from glob import glob
from operator import attrgetter

from django.conf import settings
from django.core.cache import caches
from django.db import models, transaction
from django.http import Http404
from django.utils.dateparse import parse_datetime
from django.utils.functional import cached_property

import bleach
import markdown
from django_extensions.db.fields.json import JSONField
from product_details.version_compare import Version

from bedrock.base.urlresolvers import reverse
from bedrock.releasenotes.utils import memoize

LONG_RN_CACHE_TIMEOUT = 7200  # 2 hours
cache = caches["release-notes"]
markdowner = markdown.Markdown(
    extensions=[
        "markdown.extensions.tables",
        "markdown.extensions.codehilite",
        "markdown.extensions.fenced_code",
        "markdown.extensions.toc",
        "markdown.extensions.nl2br",
    ]
)
# based on bleach.sanitizer.ALLOWED_TAGS
ALLOWED_TAGS = [
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "code",
    "div",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "i",
    "li",
    "ol",
    "p",
    "small",
    "strike",
    "strong",
    "ul",
]
ALLOWED_ATTRS = [
    "alt",
    "class",
    "href",
    "id",
    "title",
]


def process_markdown(value):
    return markdowner.reset().convert(bleach.clean(value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS))


def process_notes(notes):
    notes = [Note(d) for d in notes]
    return [n for n in notes if n.is_public]


def process_is_public(is_public):
    if settings.DEV:
        return True

    return is_public


def process_note_release(rel_data):
    return ProductRelease(**rel_data)


FIELD_PROCESSORS = {
    "created": parse_datetime,
    "modified": parse_datetime,
    "is_public": process_is_public,
    "note": process_markdown,
    "fixed_in_release": process_note_release,
}


class RNModel:
    def __init__(self, data):
        for key, value in data.items():
            if not hasattr(self, key):
                continue
            if key in FIELD_PROCESSORS:
                value = FIELD_PROCESSORS[key](value)
            setattr(self, key, value)


class Note(RNModel):
    id = None
    bug = None
    note = ""
    tag = None
    is_public = True
    fixed_in_release = None
    sort_num = None
    created = None
    modified = None


class MarkdownField(models.TextField):
    """Field that takes Markdown text as input and saves HTML to the database"""

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        value = process_markdown(value)
        setattr(model_instance, self.attname, value)
        return value


class NotesField(JSONField):
    """Field that returns a list of Note objects instead of dicts"""

    def from_db_value(self, value, expression, connection):
        if not value:
            return value

        return process_notes(self.to_python(value))


class ProductReleaseQuerySet(models.QuerySet):
    def product(self, product_name, channel_name=None, version=None):
        if product_name.lower() == "firefox extended support release":
            product_name = "firefox"
            channel_name = "esr"
        q = self.filter(product__iexact=product_name)
        if channel_name:
            q = q.filter(channel__iexact=channel_name)
        if version:
            q = q.filter(version=version)

        return q


class ProductReleaseManager(models.Manager):
    def get_queryset(self, include_drafts=False):
        qs = ProductReleaseQuerySet(self.model, using=self._db)
        if settings.DEV or include_drafts:
            return qs

        return qs.filter(is_public=True)

    def product(self, product_name, channel_name=None, version=None, include_drafts=False):
        return self.get_queryset(include_drafts).product(product_name, channel_name, version)

    def refresh(self):
        release_objs = []
        rn_path = os.path.join(settings.RELEASE_NOTES_PATH, "releases")
        with transaction.atomic(using=self.db):
            self.get_queryset(include_drafts=True).delete()
            releases = glob(os.path.join(rn_path, "*.json"))
            for release_file in releases:
                with codecs.open(release_file, "r", encoding="utf-8") as rel_fh:
                    data = json.load(rel_fh)
                    # doing this to simplify queries for Firefox since it is always
                    # looked up with product=Firefox and relies on the version number
                    # and channel to determine ESR.
                    if data["product"] == "Firefox Extended Support Release":
                        data["product"] = "Firefox"
                        data["channel"] = "ESR"
                    # make all releases public on non-production environments
                    if settings.DEV:
                        data["is_public"] = True
                    release_objs.append(ProductRelease(**data))

            self.bulk_create(release_objs)

        return len(release_objs)


class ProductRelease(models.Model):
    CHANNELS = ("Nightly", "Aurora", "Beta", "Release", "ESR")
    PRODUCTS = ("Firefox", "Firefox for Android", "Firefox Extended Support Release", "Firefox OS", "Thunderbird", "Firefox for iOS")

    product = models.CharField(max_length=50)
    channel = models.CharField(max_length=50)
    version = models.CharField(max_length=25)
    slug = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    text = MarkdownField(blank=True)
    is_public = models.BooleanField(default=False)
    bug_list = models.TextField(blank=True)
    bug_search_url = models.CharField(max_length=2000, blank=True)
    system_requirements = MarkdownField(blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    notes = NotesField(blank=True)

    objects = ProductReleaseManager()

    class Meta:
        ordering = ["-release_date"]

    def __str__(self):
        return self.title

    @cached_property
    def major_version(self):
        return str(self.version_obj.major)

    @cached_property
    def major_version_int(self):
        return self.version_obj.major or 0

    @cached_property
    def version_obj(self):
        return Version(self.version)

    @property
    def is_latest(self):
        return self == get_latest_release(self.product, self.channel)

    def get_absolute_url(self):
        if self.product == "Firefox for Android":
            urlname = "firefox.android.releasenotes"
        elif self.product == "Firefox for iOS":
            urlname = "firefox.ios.releasenotes"
        else:
            urlname = "firefox.desktop.releasenotes"

        prefix = "aurora" if self.channel == "Aurora" else "release"
        return reverse(urlname, args=[self.version, prefix])

    def get_sysreq_url(self):
        if self.product == "Firefox for Android":
            urlname = "firefox.android.system_requirements"
        elif self.product == "Firefox for iOS":
            urlname = "firefox.ios.system_requirements"
        else:
            urlname = "firefox.system_requirements"

        return reverse(urlname, args=[self.version])

    def get_bug_search_url(self):
        if self.bug_search_url:
            return self.bug_search_url
        return (
            "https://bugzilla.mozilla.org/buglist.cgi?"
            "j_top=OR&f1=target_milestone&o3=equals&v3=Firefox%20{version}&"
            "o1=equals&resolution=FIXED&o2=anyexact&query_format=advanced&"
            "f3=target_milestone&f2=cf_status_firefox{version}&"
            "bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&"
            "v1=mozilla{version}&v2=fixed%2Cverified&limit=0"
        ).format(version=self.major_version)

    def equivalent_release_for_product(self, product):
        """
        Returns the release for a specified product with the same
        channel and major version with the highest minor version,
        or None if no such releases exist
        """
        releases = ProductRelease.objects.product(product, self.channel).filter(version__startswith=f"{self.major_version}.")
        if releases:
            return sorted(releases, reverse=True, key=attrgetter("version_obj"))[0]

        return None

    def equivalent_android_release(self):
        if self.product == "Firefox":
            return self.equivalent_release_for_product("Firefox for Android")

    def equivalent_desktop_release(self):
        if self.product == "Firefox for Android":
            return self.equivalent_release_for_product("Firefox")


@memoize(LONG_RN_CACHE_TIMEOUT)
def get_release(product, version, channel=None, include_drafts=False):
    channels = [channel] if channel else ProductRelease.CHANNELS
    if product.lower() == "firefox extended support release":
        channels = ["esr"]
    for channel in channels:
        try:
            return ProductRelease.objects.product(product, channel, version, include_drafts).get()
        except ProductRelease.DoesNotExist:
            continue

    return None


def get_release_or_404(version, product, include_drafts=False):
    release = get_release(product, version, None, include_drafts)
    if release is None:
        raise Http404

    return release


@memoize(LONG_RN_CACHE_TIMEOUT)
def get_releases(product, channel, num_results=10):
    return ProductRelease.objects.product(product, channel)[:num_results]


def get_releases_or_404(product, channel, num_results=10):
    releases = get_releases(product, channel, num_results)
    if releases:
        return releases

    raise Http404


@memoize(LONG_RN_CACHE_TIMEOUT)
def get_latest_release(product, channel="release"):
    try:
        release = ProductRelease.objects.product(product, channel)[0]
    except IndexError:
        release = None

    return release


def get_latest_release_or_404(product, channel):
    release = get_latest_release(product, channel)
    if release:
        return release

    raise Http404
