# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import re

from django.conf import settings
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from bedrock.base.urlresolvers import reverse
from lib import l10n_utils
from rna.models import Release
from product_details import product_details

from bedrock.firefox.firefox_details import firefox_desktop, firefox_android, firefox_ios
from bedrock.thunderbird.details import thunderbird_desktop
from bedrock.mozorg.decorators import cache_control_expires
from bedrock.mozorg.templatetags.misc import releasenotes_url
from bedrock.firefox.templatetags.helpers import android_builds, ios_builds


SUPPORT_URLS = {
    'Firefox for Android': 'https://support.mozilla.org/products/mobile',
    'Firefox for iOS': 'https://support.mozilla.org/products/ios',
    'Firefox': 'https://support.mozilla.org/products/firefox',
    'Thunderbird': 'https://support.mozilla.org/products/thunderbird/',
}


def release_notes_template(channel, product, version=None):
    prefix = dict((c, c.lower()) for c in Release.CHANNELS)

    if product == 'Firefox' and channel == 'Aurora' and version >= 35:
        return 'firefox/releases/dev-browser-notes.html'

    dir = 'firefox'
    if product == 'Thunderbird':
        dir = 'thunderbird'

    return ('{dir}/releases/{channel}-notes.html'
            .format(dir=dir, channel=prefix.get(channel, 'release')))


def equivalent_release_url(release):
    equivalent_release = (release.equivalent_android_release() or
                          release.equivalent_desktop_release())
    if equivalent_release:
        return releasenotes_url(equivalent_release)


def get_release_or_404(version, product):
    if product == 'Firefox' and (version.endswith('esr') or
                                 len(version.split('.')) == 3):
        product_query = Q(product='Firefox') | Q(
            product='Firefox Extended Support Release')
    else:
        product_query = Q(product=product)
    release = get_object_or_404(Release, product_query, version=version)
    if not release.is_public and not settings.DEV:
        raise Http404
    return release


def get_download_url(release):
    if release.product == 'Thunderbird':
        if release.channel == 'Beta':
            return reverse('thunderbird.channel')
        else:
            return reverse('thunderbird.index')
    elif release.product == 'Firefox for Android':
        return android_builds(release.channel)[0]['download_link']
    elif release.product == 'Firefox for iOS':
        return ios_builds(release.channel)[0]['download_link']
    else:
        if release.channel == 'Aurora':
            return reverse('firefox.channel') + '#developer'
        elif release.channel == 'Beta':
            return reverse('firefox.channel') + '#beta'
        else:
            return reverse('firefox')


def check_url(product, version):
    if product == 'Firefox for Android':
        return settings.FIREFOX_MOBILE_SYSREQ_URL
    elif product == 'Firefox for iOS':
        return reverse('firefox.ios.system_requirements', args=[version])
    else:
        return reverse('firefox.system_requirements', args=[version])


@cache_control_expires(1)
def release_notes(request, version, product='Firefox'):
    if not version:
        raise Http404

    try:
        release = get_release_or_404(version, product)
    except Http404:
        release = get_release_or_404(version + 'beta', product)
        return HttpResponseRedirect(releasenotes_url(release))

    new_features, known_issues = release.notes(public_only=not settings.DEV)

    return l10n_utils.render(
        request, release_notes_template(release.channel, product,
                                        int(release.major_version())), {
            'version': version,
            'download_url': get_download_url(release),
            'support_url': SUPPORT_URLS.get(product, 'https://support.mozilla.org/'),
            'check_url': check_url(product, version),
            'release': release,
            'equivalent_release_url': equivalent_release_url(release),
            'new_features': new_features,
            'known_issues': known_issues})


@cache_control_expires(1)
def system_requirements(request, version, product='Firefox'):
    release = get_release_or_404(version, product)
    dir = 'firefox'
    if product == 'Thunderbird':
        dir = 'thunderbird'
    return l10n_utils.render(
        request, '{dir}/releases/system_requirements.html'.format(dir=dir),
        {'release': release, 'version': version})


def latest_notes(request, product='firefox', platform=None, channel=None):
    if not platform:
        platform = 'desktop'

    if not channel:
        channel = 'release'
    if channel in ['aurora', 'developer']:
        channel = 'alpha'
    if channel == 'organizations':
        channel = 'esr'

    if product == 'thunderbird':
        version = thunderbird_desktop.latest_version(channel)
    elif platform == 'android':
        version = firefox_android.latest_version(channel)
    elif platform == 'ios':
        version = firefox_ios.latest_version(channel)
    else:
        version = firefox_desktop.latest_version(channel)

    if channel == 'beta':
        version = re.sub(r'b\d+$', 'beta', version)
    if channel == 'esr':
        version = re.sub(r'esr$', '', version)

    dir = 'auroranotes' if channel == 'alpha' else 'releasenotes'
    path = [product, version, dir]
    locale = getattr(request, 'locale', None)
    if product == 'firefox' and platform != 'desktop':
        path.insert(1, platform)
    if locale:
        path.insert(0, locale)
    return HttpResponseRedirect('/' + '/'.join(path) + '/')


def latest_sysreq(request, channel, product):
    if product == 'firefox' and channel == 'developer':
        channel = 'alpha'
    if channel == 'organizations':
        channel = 'esr'

    if product == 'thunderbird':
        version = thunderbird_desktop.latest_version(channel)
    elif product == 'mobile':
        version = firefox_android.latest_version(channel)
    elif product == 'ios':
        version = firefox_ios.latest_version(channel)
    else:
        version = firefox_desktop.latest_version(channel)

    if channel == 'beta':
        version = re.sub(r'b\d+$', 'beta', version)
    if channel == 'esr':
        version = re.sub(r'^(\d+).+', r'\1.0', version)

    dir = 'system-requirements'
    path = [product, version, dir]
    locale = getattr(request, 'locale', None)
    if locale:
        path.insert(0, locale)
    return HttpResponseRedirect('/' + '/'.join(path) + '/')


def releases_index(request, product):
    releases = {}
    esr_major_versions = range(
        10, int(firefox_desktop.latest_version().split('.')[0]), 7)

    if product == 'Firefox':
        major_releases = firefox_desktop.firefox_history_major_releases
        minor_releases = firefox_desktop.firefox_history_stability_releases
    elif product == 'Thunderbird':
        major_releases = product_details.thunderbird_history_major_releases
        minor_releases = product_details.thunderbird_history_stability_releases

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
