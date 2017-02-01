# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from collections import OrderedDict
from operator import itemgetter
from urllib import urlencode

from django.conf import settings
from bedrock.base.waffle import switch
from product_details import ProductDetails
from lib.l10n_utils.dotlang import _


# TODO: port this to django-mozilla-product-details
class ThunderbirdDesktop(ProductDetails):
    bouncer_url = settings.BOUNCER_URL

    # Note download-sha1.allizom.org is the production endpoint for SHA-1.
    # It uses this because that's the only SHA-1 certificate
    # we have that's usable. (SHA-1 certs can no longer be issued).
    sha1_bouncer_url = 'https://download-sha1.allizom.org/'

    download_base_url_ftp = 'https://ftp.mozilla.org/pub/mozilla.org/thunderbird/'

    # Human-readable platform names
    platform_labels = OrderedDict([
        ('winsha1', 'Windows (XP/Vista)'),
        ('win', 'Windows'),
        ('osx', 'OS X'),
        ('linux', 'Linux'),
        ('linux64', 'Linux 64-bit'),
    ])

    # Human-readable channel names
    channel_labels = {
        'release': _('Thunderbird'),
        'beta': _('Thunderbird Beta'),
        'alpha': _('Earlybird'),
    }

    # Version property names in product-details
    version_map = {
        'alpha': 'LATEST_THUNDERBIRD_ALPHA_VERSION',
        'beta': 'LATEST_THUNDERBIRD_DEVEL_VERSION',
        'release': 'LATEST_THUNDERBIRD_VERSION',
    }

    # Binary file suffixes on FTP
    file_suffixes = {
        'win': 'win32.installer.exe',
        'osx': 'mac.dmg',
        'linux': 'linux-i686.tar.bz2',
        'linux64': 'linux-x86_64.tar.bz2',
    }

    def platforms(self, channel='release'):
        return self.platform_labels.items()

    def get_bouncer_url(self, platform):
        return self.sha1_bouncer_url if not switch('disable-sha1-downloads') and platform == 'winsha1' else self.bouncer_url

    def latest_version(self, channel='release'):
        if not channel:
            channel = 'release'
        if channel == 'earlybird':
            channel = 'alpha'

        version = self.version_map.get(channel, 'LATEST_THUNDERBIRD_VERSION')
        try:
            return self.thunderbird_versions[version]
        except KeyError:
            return None

    def latest_major_version(self, channel):
        """Return latest major version as an int."""
        lv = self.latest_version(channel)
        if lv is None:
            return 0

        try:
            return int(lv.split('.')[0])
        except ValueError:
            return 0

    def latest_builds(self, locale, channel='release'):
        """Return build info for a locale and channel.

        :param locale: locale string of the build
        :param channel: channel of the build: release, beta, or aurora
        :return: dict or None
        """
        all_builds = (self.thunderbird_primary_builds,
                      self.thunderbird_beta_builds)
        version = self.latest_version(channel)

        # FIXME: Use the Release channel version to retrieve the supported
        # locales until the new Ship It API provides the Beta and Earlybird
        # build info.
        _version = self.latest_version('release')

        for builds in all_builds:
            if locale in builds and _version in builds[locale]:
                _builds = builds[locale][_version]
                # Append 64-bit builds
                if 'Linux' in _builds:
                    _builds['Linux 64-bit'] = _builds['Linux']
                return version, _builds

    def _matches_query(self, info, query):
        words = re.split(r',|,?\s+', query.strip().lower())
        return all((word in info['name_en'].lower() or
                    word in info['name_native'].lower()) for word in words)

    def _get_filtered_builds(self, builds, channel, version=None, query=None):
        """
        Get a list of builds, sorted by english locale name, for a specific
        Thunderbird version.
        :param builds: a build dict from the JSON
        :param channel: one of self.channel_map.keys().
        :param version: a thunderbird version. one of self.latest_versions.
        :param query: a string to match against native or english locale name
        :return: list
        """

        version = version or self.latest_version(channel)
        f_builds = []

        # FIXME: Use the Release channel version to retrieve the supported
        # locales until the new Ship It API provides the Beta and Earlybird
        # build info.
        _version = self.latest_version('release')

        for locale, build in builds.iteritems():
            if locale not in self.languages or not build.get(_version):
                continue

            build_info = {
                'locale': locale,
                'name_en': self.languages[locale]['English'],
                'name_native': self.languages[locale]['native'],
                'platforms': {},
            }

            # only include builds that match a search query
            if query is not None and not self._matches_query(build_info, query):
                continue

            for platform, label in self.platform_labels.iteritems():
                build_info['platforms'][platform] = {
                    'download_url': self.get_download_url(channel, version,
                                                          platform, locale,
                                                          True),
                }

            f_builds.append(build_info)

        return sorted(f_builds, key=itemgetter('name_en'))

    def get_filtered_full_builds(self, channel, version=None, query=None):
        """
        Return filtered builds for the fully translated releases.
        :param channel: one of self.channel_map.keys().
        :param version: a thunderbird version. one of self.latest_version.
        :param query: a string to match against native or english locale name
        :return: list
        """
        return self._get_filtered_builds(self.thunderbird_primary_builds,
                                         channel, version, query)

    def get_download_url(self, channel, version, platform, locale,
                         force_direct=True):
        """
        Get direct download url for the product.
        :param channel: one of self.channel_map.keys().
        :param version: a thunderbird version. one of self.latest_version.
        :param platform: OS. one of self.platform_labels.keys().
        :param locale: e.g. pt-BR. one exception is ja-JP-mac.
        :param force_direct: Force the download URL to be direct.
        :return: string url
        """
        _version = version
        _locale = 'ja-JP-mac' if platform == 'osx' and locale == 'ja' else locale
        _platform = 'win' if platform == 'winsha1' else platform

        # Point the FTP server for Earlybird
        if channel == 'alpha':
            return '%snightly/latest-comm-aurora%s/thunderbird-%s.%s.%s' % (
                self.download_base_url_ftp,
                '' if locale == 'en-US' else '-l10n',
                _version, _locale, self.file_suffixes[_platform])

        # Check if direct download link has been requested
        # (bypassing the transition page)
        if force_direct:
            # build a direct download link
            return '?'.join([self.get_bouncer_url(platform),
                             urlencode([
                                 ('product', 'thunderbird-%s-SSL' % _version),
                                 ('os', _platform),
                                 # Order matters, lang must be last for bouncer.
                                 ('lang', _locale),
                             ])])
        else:
            # build a link to the transition page
            return self.download_base_url_transition


thunderbird_desktop = ThunderbirdDesktop()
