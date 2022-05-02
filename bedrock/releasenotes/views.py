# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re
from copy import copy
from operator import attrgetter

from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.urls import NoReverseMatch
from django.views.decorators.http import require_safe

from bedrock.base.urlresolvers import reverse
from bedrock.firefox.firefox_details import firefox_desktop
from bedrock.firefox.templatetags.helpers import android_builds, ios_builds
from bedrock.releasenotes.models import (
    get_latest_release_or_404,
    get_release_or_404,
    get_releases_or_404,
)
from lib import l10n_utils

SUPPORT_URLS = {
    "Firefox for Android": "https://support.mozilla.org/products/mobile",
    "Firefox for iOS": "https://support.mozilla.org/products/ios",
    "Firefox": "https://support.mozilla.org/products/firefox",
}


def release_notes_template(channel, product, version=None):
    channel = channel or "release"
    version = version or 0

    if product == "Firefox" and channel == "Aurora" and version >= 35:
        return "firefox/releases/dev-browser-notes.html"

    dir = "firefox"

    return f"{dir}/releases/{channel.lower()}-notes.html"


def equivalent_release_url(release):
    equivalent_release = release.equivalent_android_release() or release.equivalent_desktop_release()
    if equivalent_release:
        return equivalent_release.get_absolute_url()


def get_download_url(release):
    if release.product == "Firefox for Android":
        return android_builds(release.channel)[0]["download_link"]
    elif release.product == "Firefox for iOS":
        return ios_builds(release.channel)[0]["download_link"]
    else:
        if release.channel == "Aurora":
            return reverse("firefox.channel.desktop") + "#developer"
        elif release.channel == "Beta":
            return reverse("firefox.channel.desktop") + "#beta"
        else:
            return reverse("firefox")


def show_android_sys_req(version):
    if version:
        match = re.match(r"\d{1,3}", version)
        if match:
            num_version = int(match.group(0))
            return num_version >= 46

    return False


def check_url(product, version):
    if product == "Firefox for Android":
        # System requirement pages for Android releases exist from 46.0 and upward.
        if show_android_sys_req(version):
            return reverse("firefox.android.system_requirements", args=[version])
        else:
            return settings.FIREFOX_MOBILE_SYSREQ_URL
    elif product == "Firefox for iOS":
        return reverse("firefox.ios.system_requirements", args=[version])
    else:
        return reverse("firefox.system_requirements", args=[version])


@require_safe
def release_notes(request, version, product="Firefox"):

    if not version:
        raise Http404

    # Show a "coming soon" page for any unpublished Firefox releases
    include_drafts = product in ["Firefox", "Firefox for Android"]

    try:
        release = get_release_or_404(version, product, include_drafts)
    except Http404:
        release = get_release_or_404(version + "beta", product, include_drafts)
        return HttpResponseRedirect(release.get_absolute_url())

    # add MDN link to all non-iOS releases. bug 1553566
    # avoid adding duplicate notes
    release_notes = copy(release.notes)
    if release.product != "Firefox for iOS":
        release_notes.insert(
            0,
            {
                "id": "mdn",
                "is_public": True,
                "tag": "Developer",
                "sort_num": 1,
                "note": f'<a class="mdn-icon" rel="external" '
                f'href="https://developer.mozilla.org/docs/Mozilla/Firefox/Releases/'
                f'{ release.major_version }">Developer Information</a>',
            },
        )

    return l10n_utils.render(
        request,
        release_notes_template(release.channel, product, int(release.major_version)),
        {
            "version": version,
            "download_url": get_download_url(release),
            "support_url": SUPPORT_URLS.get(product, "https://support.mozilla.org/"),
            "check_url": check_url(product, version),
            "release": release,
            "release_notes": release_notes,
            "equivalent_release_url": equivalent_release_url(release),
        },
    )


@require_safe
def system_requirements(request, version, product="Firefox"):
    release = get_release_or_404(version, product)
    dir = "firefox"
    return l10n_utils.render(request, f"{dir}/releases/system_requirements.html", {"release": release, "version": version})


def latest_release(product="firefox", platform=None, channel=None):
    if not platform:
        platform = "desktop"
    elif platform == "android":
        product = "firefox for android"
    elif platform == "ios":
        product = "firefox for ios"

    if not channel:
        channel = "release"
    elif channel in ["developer", "earlybird"]:
        channel = "beta"
    elif channel == "organizations":
        channel = "esr"

    return get_latest_release_or_404(product, channel)


@require_safe
def latest_notes(request, product="firefox", platform=None, channel=None):
    release = latest_release(product, platform, channel)
    return HttpResponseRedirect(release.get_absolute_url())


@require_safe
def latest_sysreq(request, product="firefox", platform=None, channel=None):
    release = latest_release(product, platform, channel)
    return HttpResponseRedirect(release.get_sysreq_url())


@require_safe
def releases_index(request, product):
    releases = {}
    major_releases = []

    if product == "Firefox":
        major_releases = firefox_desktop.firefox_history_major_releases
        minor_releases = firefox_desktop.firefox_history_stability_releases

    for release in major_releases:
        major_version = float(re.findall(r"^\d+\.\d+", release)[0])
        # The version numbering scheme of Firefox changes sometimes. The second
        # number has not been used since Firefox 4, then reintroduced with
        # Firefox ESR 24 (Bug 870540). On this index page, 24.1.x should be
        # fallen under 24.0. This pattern is a tricky part.
        # The outlier is 33.1 which is in major_releases for some reason.
        major_pattern = r"^" + re.escape(
            f"{major_version:.0f}." if major_version > 4 and release not in ["33.0", "33.1"] else f"{major_version:.1f}."
        )
        releases[major_version] = {
            "major": release,
            "minor": sorted(
                [x for x in minor_releases if re.findall(major_pattern, x) if x not in major_releases], key=lambda x: [int(y) for y in x.split(".")]
            ),
        }

    return l10n_utils.render(request, f"{product.lower()}/releases/index.html", {"releases": sorted(releases.items(), reverse=True)})


@require_safe
def nightly_feed(request):
    """Serve an Atom feed with the latest changes in Firefox Nightly"""
    notes = {}
    releases = get_releases_or_404("firefox", "nightly", 5)

    for release in releases:
        try:
            link = reverse("firefox.desktop.releasenotes", args=(release.version, "release"))
        except NoReverseMatch:
            continue

        for note in release.notes:
            if note.id in notes:
                continue

            if note.is_public and note.tag:
                note.link = f"{link}#note-{note.id}"
                note.version = release.version
                notes[note.id] = note

    # Sort by date in descending order
    notes = sorted(notes.values(), key=attrgetter("modified"), reverse=True)

    return l10n_utils.render(request, "firefox/releases/nightly-feed.xml", {"notes": notes}, content_type="application/atom+xml")
