# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import re
from collections import defaultdict
from unittest.mock import patch

from django.conf import settings
from django.http import HttpResponse
from django.test import override_settings
from django.test.client import Client
from django.urls import resolvers

from bedrock.contentful.constants import (
    CONTENT_CLASSIFICATION_VPN,
    CONTENT_TYPE_PAGE_RESOURCE_CENTER,
    VRC_ROOT_PATH,
)
from bedrock.contentful.models import ContentfulEntry
from bedrock.releasenotes.models import ProductRelease
from bedrock.security.models import SecurityAdvisory

SEC_KNOWN_VULNS = [
    "/security/known-vulnerabilities/firefox/",
    "/security/known-vulnerabilities/firefox-esr/",
    "/security/known-vulnerabilities/firefox-for-ios/",
    "/security/known-vulnerabilities/firefox-os/",
    "/security/known-vulnerabilities/mozilla-vpn/",
    "/security/known-vulnerabilities/thunderbird/",
    "/security/known-vulnerabilities/thunderbird-esr/",
    "/security/known-vulnerabilities/seamonkey/",
    "/security/known-vulnerabilities/firefox-3.6/",
    "/security/known-vulnerabilities/firefox-3.5/",
    "/security/known-vulnerabilities/firefox-3.0/",
    "/security/known-vulnerabilities/firefox-2.0/",
    "/security/known-vulnerabilities/firefox-1.5/",
    "/security/known-vulnerabilities/firefox-1.0/",
    "/security/known-vulnerabilities/thunderbird-3.1/",
    "/security/known-vulnerabilities/thunderbird-3.0/",
    "/security/known-vulnerabilities/thunderbird-2.0/",
    "/security/known-vulnerabilities/thunderbird-1.5/",
    "/security/known-vulnerabilities/thunderbird-1.0/",
    "/security/known-vulnerabilities/seamonkey-2.0/",
    "/security/known-vulnerabilities/seamonkey-1.1/",
    "/security/known-vulnerabilities/seamonkey-1.0/",
    "/security/known-vulnerabilities/mozilla-suite/",
]


def get_security_urls():
    urls = {url: ["en-US"] for url in SEC_KNOWN_VULNS}
    for advisory in SecurityAdvisory.objects.all():
        try:
            adv_url = advisory.get_absolute_url()
        except resolvers.NoReverseMatch:
            continue

        # strip "/en-US" off the front
        if adv_url.startswith("/en-US"):
            adv_url = adv_url[6:]

        urls[adv_url] = ["en-US"]

    return urls


def get_release_notes_urls():
    urls = {}
    for release in ProductRelease.objects.exclude(product="Thunderbird"):
        # we redirect all release notes for versions 28.x and below to an archive
        # and Firefox for iOS uses a different version numbering scheme
        if release.product != "Firefox for iOS" and release.major_version_int < 29:
            continue

        try:
            rel_path = release.get_absolute_url()
            req_path = release.get_sysreq_url()
        except resolvers.NoReverseMatch:
            continue

        # strip "/en-US" off the front
        if rel_path.startswith("/en-US"):
            rel_path = rel_path[6:]
        if req_path.startswith("/en-US"):
            req_path = req_path[6:]

        urls[rel_path] = ["en-US"]
        urls[req_path] = ["en-US"]

    return urls


# DEV should always be False for this to avoid some URLs that are only present in DEV=True mode
@override_settings(DEV=False)
def get_static_urls():
    urls = {}
    client = Client()
    excludes = [
        re.compile(r)
        for r in settings.NOINDEX_URLS
        + [
            r".*%\(.*\).*",
            r".*//$",
            r"^media/",
            r"^robots\.txt$",
            # Redirects in en-US. Added via EXTRA_INDEX_URLS
            r"firefox-klar/$",
        ]
    ]

    # start with the ones we know we want
    urls.update(settings.EXTRA_INDEX_URLS)

    # get_resolver is an undocumented but convenient function.
    # Try to retrieve all valid URLs on this site.
    # NOTE: have to use `lists()` here since the standard
    # `items()` only returns the first item in the list for the
    # view since `reverse_dict` is a `MultiValueDict`.
    for key, values in resolvers.get_resolver(None).reverse_dict.lists():
        for value in values:
            path = value[0][0][0]
            # Exclude pages that we don't want be indexed by search engines.
            # Some other URLs are also unnecessary for the sitemap.
            if any(exclude.search(path) for exclude in excludes):
                continue

            path_prefix = path.split("/", 2)[0]
            nonlocale = path_prefix in settings.SUPPORTED_NONLOCALES
            path = f"/{path}"
            if nonlocale:
                locales = []
            else:
                with patch("lib.l10n_utils.django_render") as render:
                    render.return_value = HttpResponse()
                    client.get("/" + settings.LANGUAGE_CODE + path)

                # Exclude urls that did not call render
                if not render.called:
                    continue

                locales = set(render.call_args[0][2]["translations"].keys())

                # zh-CN is a redirect on the homepage
                if path == "/":
                    locales -= {"zh-CN"}

                # Firefox Focus has a different URL in German
                if path == "/privacy/firefox-focus/":
                    locales -= {"de"}

                # just remove any locales not in our prod list
                locales = list(locales.intersection(settings.PROD_LANGUAGES))

            if path not in urls:
                urls[path] = locales

    return urls


def _get_vrc_urls():
    # URLs for individual VRC articles - the listing/landing page is declared
    # separately in bedrock/products/urls.py so we don't need to include it here

    urls = defaultdict(list)

    for entry in ContentfulEntry.objects.filter(
        localisation_complete=True,
        content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
        classification=CONTENT_CLASSIFICATION_VPN,
    ):
        _path = f"{VRC_ROOT_PATH}{entry.slug}/"
        urls[_path].append(entry.locale)  # One slug may support multiple locales

    return urls


def get_contentful_urls():
    urls = {}
    urls.update(_get_vrc_urls())
    return urls


def update_sitemaps():
    urls = get_static_urls()
    urls.update(get_release_notes_urls())
    urls.update(get_security_urls())
    urls.update(get_contentful_urls())
    # Output static files
    output_json(urls)


def output_json(urls):
    output_file = settings.ROOT_PATH.joinpath("root_files", "sitemap.json")

    # Output the data as a JSON file for convenience
    with output_file.open("w") as json_file:
        json.dump(urls, json_file)
