# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import re
from operator import attrgetter

from django.conf import settings
from django.http import Http404, HttpResponseRedirect

from lib import l10n_utils

from bedrock.base.urlresolvers import reverse
from bedrock.firefox.firefox_details import firefox_desktop
from bedrock.firefox.templatetags.helpers import android_builds, ios_builds
from bedrock.releasenotes.models import get_latest_release_or_404, get_release_or_404, get_releases_or_404

SUPPORT_URLS = {
    'Firefox for Android': 'https://support.mozilla.org/products/mobile',
    'Firefox for iOS': 'https://support.mozilla.org/products/ios',
    'Firefox': 'https://support.mozilla.org/products/firefox',
}


def release_notes_template(channel, product, version=None):
    channel = channel or 'release'
    if product == 'Firefox' and channel == 'Aurora' and version >= 35:
        return 'firefox/releases/dev-browser-notes.html'

    dir = 'firefox'

    return ('{dir}/releases/{channel}-notes.html'
            .format(dir=dir, channel=channel.lower()))


def equivalent_release_url(release):
    equivalent_release = (release.equivalent_android_release() or
                          release.equivalent_desktop_release())
    if equivalent_release:
        return equivalent_release.get_absolute_url()


def get_download_url(release):
    if release.product == 'Firefox for Android':
        return android_builds(release.channel)[0]['download_link']
    elif release.product == 'Firefox for iOS':
        return ios_builds(release.channel)[0]['download_link']
    else:
        if release.channel == 'Aurora':
            return reverse('firefox.channel.desktop') + '#developer'
        elif release.channel == 'Beta':
            return reverse('firefox.channel.desktop') + '#beta'
        else:
            return reverse('firefox')


def show_android_sys_req(version):
    match = re.match(r'\d{1,2}', version)
    if match:
        num_version = int(match.group(0))
        return num_version >= 46

    return False


def check_url(product, version):
    if product == 'Firefox for Android':
        # System requirement pages for Android releases exist from 46.0 and upward.
        if show_android_sys_req(version):
            return reverse('firefox.android.system_requirements', args=[version])
        else:
            return settings.FIREFOX_MOBILE_SYSREQ_URL
    elif product == 'Firefox for iOS':
        return reverse('firefox.ios.system_requirements', args=[version])
    else:
        return reverse('firefox.system_requirements', args=[version])


def release_notes(request, version, product='Firefox'):
    if not version:
        raise Http404

    # Show a "coming soon" page for any unpublished Firefox releases
    include_drafts = product in ['Firefox', 'Firefox for Android']

    try:
        release = get_release_or_404(version, product, include_drafts)
    except Http404:
        release = get_release_or_404(version + 'beta', product, include_drafts)
        return HttpResponseRedirect(release.get_absolute_url())

    return l10n_utils.render(
        request, release_notes_template(release.channel, product,
                                        int(release.major_version)), {
            'version': version,
            'download_url': get_download_url(release),
            'support_url': SUPPORT_URLS.get(product, 'https://support.mozilla.org/'),
            'check_url': check_url(product, version),
            'release': release,
            'equivalent_release_url': equivalent_release_url(release),
        })


def system_requirements(request, version, product='Firefox'):
    release = get_release_or_404(version, product)
    dir = 'firefox'
    return l10n_utils.render(
        request, '{dir}/releases/system_requirements.html'.format(dir=dir),
        {'release': release, 'version': version})


def latest_release(product='firefox', platform=None, channel=None):
    if not platform:
        platform = 'desktop'
    elif platform == 'android':
        product = 'firefox for android'
    elif platform == 'ios':
        product = 'firefox for ios'

    if not channel:
        channel = 'release'
    elif channel in ['developer', 'earlybird']:
        channel = 'beta'
    elif channel == 'organizations':
        channel = 'esr'

    return get_latest_release_or_404(product, channel)


def latest_notes(request, product='firefox', platform=None, channel=None):
    release = latest_release(product, platform, channel)
    return HttpResponseRedirect(release.get_absolute_url())


def latest_sysreq(request, product='firefox', platform=None, channel=None):
    release = latest_release(product, platform, channel)
    return HttpResponseRedirect(release.get_sysreq_url())


def releases_index(request, product):
    releases = {}
    esr_major_versions = range(
        10, int(firefox_desktop.latest_version().split('.')[0]), 7)

    if product == 'Firefox':
        major_releases = firefox_desktop.firefox_history_major_releases
        minor_releases = firefox_desktop.firefox_history_stability_releases

    for release in major_releases:
        major_version = float(re.findall(r'^\d+\.\d+', release)[0])
        # The version numbering scheme of Firefox changes sometimes. The second
        # number has not been used since Firefox 4, then reintroduced with
        # Firefox ESR 24 (Bug 870540). On this index page, 24.1.x should be
        # fallen under 24.0. This pattern is a tricky part.
        converter = '%g' if int(major_version) in esr_major_versions else '%s'
        major_pattern = r'^' + re.escape(converter % round(major_version, 1))
        releases[major_version] = {
            'major': release,
            'minor': sorted(filter(lambda x: re.findall(major_pattern, x),
                                   minor_releases),
                            key=lambda x: map(lambda y: int(y), x.split('.')))
        }

    return l10n_utils.render(
        request, '{product}/releases/index.html'.format(product=product.lower()),
        {'releases': sorted(releases.items(), reverse=True)}
    )


def nightly_feed(request):
    """Serve an Atom feed with the latest changes in Firefox Nightly"""
    notes = {}
    releases = get_releases_or_404('firefox', 'nightly', 5)

    for release in releases:
        link = reverse('firefox.desktop.releasenotes',
                        args=(release.version, 'release'))

        for note in release.notes:
            if note.id in notes:
                continue

            if note.is_public and note.tag:
                note.link = '%s#note-%s' % (link, note.id)
                note.version = release.version
                notes[note.id] = note

    # Sort by date in descending order
    notes = sorted(notes.values(), key=attrgetter('modified'), reverse=True)

    return l10n_utils.render(request, 'firefox/releases/nightly-feed.xml',
                             {'notes': notes},
                             content_type='application/atom+xml')
