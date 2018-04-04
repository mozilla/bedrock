# coding=utf-8

import re
from collections import OrderedDict
from operator import itemgetter
from urllib import urlencode

from django.conf import settings

from decouple import Csv, config
from product_details import ProductDetails

from bedrock.base.waffle import switch
from lib.l10n_utils.dotlang import _lazy as _


# TODO: port this to django-mozilla-product-details
class _ProductDetails(ProductDetails):
    bouncer_url = settings.BOUNCER_URL

    # Note download-sha1.allizom.org is the production endpoint for SHA-1.
    # It uses this because that's the only SHA-1 certificate
    # we have that's usable. (SHA-1 certs can no longer be issued).
    sha1_bouncer_url = 'https://download-sha1.allizom.org/'

    def _matches_query(self, info, query):
        words = re.split(r',|,?\s+', query.strip().lower())
        return all((word in info['name_en'].lower() or
                    word in info['name_native'].lower()) for word in words)


class FirefoxDesktop(_ProductDetails):
    download_base_url_transition = '/firefox/download/thanks/'

    # Human-readable platform names
    platform_labels = OrderedDict([
        ('winsha1', 'Windows (XP/Vista)'),
        ('win64', 'Windows 64-bit'),
        ('win', 'Windows 32-bit'),
        ('osx', 'macOS'),
        ('linux64', 'Linux 64-bit'),
        ('linux', 'Linux 32-bit'),
    ])

    # Recommended/modern vs traditional/legacy platforms
    platform_classification = OrderedDict([
        ('recommended', ('win64', 'osx', 'linux64')),
        ('traditional', ('win', 'winsha1', 'linux')),
    ])

    # Human-readable channel names
    channel_labels = {
        'nightly': _('Firefox Nightly'),
        'alpha': _('Developer Edition'),
        'devedition': _('Developer Edition'),
        'beta': _('Firefox Beta'),
        'esr': _('Firefox Extended Support Release'),
        'release': _('Firefox'),
    }

    # Version property names in product-details
    version_map = {
        'nightly': 'FIREFOX_NIGHTLY',
        'alpha': 'FIREFOX_DEVEDITION',
        'devedition': 'FIREFOX_DEVEDITION',
        'beta': 'LATEST_FIREFOX_DEVEL_VERSION',
        'esr': 'FIREFOX_ESR',
        'esr_next': 'FIREFOX_ESR_NEXT',
        'release': 'LATEST_FIREFOX_VERSION',
    }

    def __init__(self, **kwargs):
        super(FirefoxDesktop, self).__init__(**kwargs)

    def get_bouncer_url(self, platform):
        return self.sha1_bouncer_url if not switch('disable-sha1-downloads') and platform == 'winsha1' else self.bouncer_url

    def platforms(self, channel='release', classified=False):
        """
        Get the desktop platform dictionary containing slugs and corresponding
        labels. If the classified option is True, it will be ordered by the
        classification where recommended platforms go first, otherwise a simple
        copy of platform_labels will be returned.
        """
        if classified:
            platforms = OrderedDict()
            for k, v in self.platform_classification.iteritems():
                for platform in v:
                    platforms[platform] = self.platform_labels[platform]
        else:
            platforms = self.platform_labels.copy()

        return platforms.items()

    def latest_version(self, channel='release'):
        version = self.version_map.get(channel, 'LATEST_FIREFOX_VERSION')
        try:
            return self.firefox_versions[version]
        except KeyError:
            if channel in ['alpha', 'devedition']:
                # beta as a fall-back until all product-details data is updated
                return self.latest_version('beta')

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

    @property
    def esr_major_versions(self):
        versions = []
        for channel in ('esr', 'esr_next'):
            version_int = self.latest_major_version(channel)
            if version_int:
                versions.append(version_int)

        return versions

    @property
    def esr_minor_versions(self):
        versions = []
        for channel in ('esr', 'esr_next'):
            version = self.latest_version(channel)
            version_int = self.latest_major_version(channel)
            if version and version_int:
                versions.append(str(version).replace('esr', ''))

        return versions

    def latest_builds(self, locale, channel='release'):
        """Return build info for a locale and channel.

        :param locale: locale string of the build
        :param channel: channel of the build: release, beta, or aurora
        :return: dict or None
        """
        all_builds = (self.firefox_primary_builds,
                      self.firefox_beta_builds)
        version = self.latest_version(channel)

        for builds in all_builds:
            if locale in builds and version in builds[locale]:
                _builds = builds[locale][version]
                # Append 64-bit builds and Sha-1
                if 'Windows' in _builds:
                    _builds['Windows 64-bit'] = _builds['Windows']
                    _builds['Windows (XP/Vista)'] = _builds['Windows']
                if 'Linux' in _builds:
                    _builds['Linux 64-bit'] = _builds['Linux']
                return version, _builds

    def _get_filtered_builds(self, builds, channel, version=None, query=None):
        """
        Get a list of builds, sorted by english locale name, for a specific
        Firefox version.
        :param builds: a build dict from the JSON
        :param channel: one of self.version_map.keys().
        :param version: a firefox version. one of self.latest_versions.
        :param query: a string to match against native or english locale name
        :return: list
        """
        version = version or self.latest_version(channel)

        f_builds = []
        for locale, build in builds.iteritems():
            if locale not in self.languages or not build.get(version):
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
                                                          True, True),
                }

            f_builds.append(build_info)

        return sorted(f_builds, key=itemgetter('name_en'))

    def get_filtered_full_builds(self, channel, version=None, query=None):
        """
        Return filtered builds for the fully translated releases.
        :param channel: one of self.version_map.keys().
        :param version: a firefox version. one of self.latest_version.
        :param query: a string to match against native or english locale name
        :return: list
        """
        return self._get_filtered_builds(self.firefox_primary_builds,
                                         channel, version, query)

    def get_filtered_test_builds(self, channel, version=None, query=None):
        """
        Return filtered builds for the translated releases in beta.
        :param channel: one of self.version_map.keys().
        :param version: a firefox version. one of self.latest_version.
        :param query: a string to match against native or english locale name
        :return: list
        """
        return self._get_filtered_builds(self.firefox_beta_builds,
                                         channel, version, query)

    def get_download_url(self, channel, version, platform, locale,
                         force_direct=False, force_full_installer=False,
                         force_funnelcake=False, funnelcake_id=None,
                         locale_in_transition=False):
        """
        Get direct download url for the product.
        :param channel: one of self.version_map.keys().
        :param version: a firefox version. one of self.latest_version.
        :param platform: OS. one of self.platform_labels.keys().
        :param locale: e.g. pt-BR. one exception is ja-JP-mac.
        :param force_direct: Force the download URL to be direct.
                always True for non-release URLs.
        :param force_full_installer: Force the installer download to not be
                the stub installer (for aurora).
        :param force_funnelcake: Force the download version for en-US Windows to be
                'latest', which bouncer will translate to the funnelcake build.
        :param funnelcake_id: ID for the the funnelcake build.
        :param locale_in_transition: Include the locale in the transition URL
        :return: string url
        """
        _version = version
        _locale = 'ja-JP-mac' if platform == 'osx' and locale == 'ja' else locale
        _platform = 'win' if platform == 'winsha1' else platform
        channel = 'devedition' if channel == 'alpha' else channel
        force_direct = True if channel != 'release' else force_direct
        stub_platforms = ['win', 'win64']
        esr_channels = ['esr', 'esr_next']
        include_funnelcake_param = False

        # Bug 1345467 - Only allow specifically configured funnelcake builds
        if funnelcake_id:
            fc_platforms = config('FUNNELCAKE_%s_PLATFORMS' % funnelcake_id, default='', cast=Csv())
            fc_locales = config('FUNNELCAKE_%s_LOCALES' % funnelcake_id, default='', cast=Csv())
            include_funnelcake_param = _platform in fc_platforms and _locale in fc_locales

        # Check if direct download link has been requested
        # if not just use transition URL
        if not force_direct:
            # build a link to the transition page
            transition_url = self.download_base_url_transition
            if funnelcake_id:
                # include funnelcake in scene 2 URL
                transition_url += '?f=%s' % funnelcake_id

            if locale_in_transition:
                transition_url = '/%s%s' % (locale, transition_url)

            return transition_url

        # otherwise build a full download URL
        prod_name = 'firefox' if channel == 'release' else 'firefox-%s' % channel
        suffix = 'latest-ssl'
        if channel in esr_channels:
            # nothing special about ESR other than there is no stub.
            # included in this contitional to avoid the following elif.
            if channel == 'esr_next':
                # no firefox-esr-next-latest-ssl alias just yet
                # could come in future in bug 1408868
                prod_name = 'firefox'
                suffix = '%s-SSL' % _version
        elif _platform in stub_platforms and not force_full_installer:
            # Use the stub installer for approved platforms
            # append funnelcake id to version if we have one
            if include_funnelcake_param:
                suffix = 'stub-f%s' % funnelcake_id
            else:
                suffix = 'stub'
        elif channel == 'nightly' and locale != 'en-US':
            # Nightly uses a different product name for localized builds,
            # and is the only one ಠ_ಠ
            suffix = 'latest-l10n-ssl'

        product = '%s-%s' % (prod_name, suffix)

        return '?'.join([self.get_bouncer_url(platform),
                        urlencode([
                            ('product', product),
                            ('os', _platform),
                            # Order matters, lang must be last for bouncer.
                            ('lang', _locale),
                        ])])


class FirefoxAndroid(_ProductDetails):
    # Human-readable architecture names
    platform_labels = OrderedDict([
        ('arm', _('ARM devices\n(Android %s+)')),
        ('x86', _('Intel devices\n(Android %s+ x86 CPU)')),
    ])

    # Recommended/modern vs traditional/legacy platforms
    # Unused but required to match FirefoxDesktop
    platform_classification = None

    # Human-readable channel names
    channel_labels = {
        'nightly': _('Firefox Nightly'),
        'beta': _('Firefox Beta'),
        'release': _('Firefox'),
    }

    # Version property names in product-details
    version_map = {
        'nightly': 'nightly_version',
        'beta': 'beta_version',
        'release': 'version',
    }

    # Build property names in product-details
    build_map = {
        'beta': 'beta_builds',
        'release': 'builds',
    }

    # Platform names defined in bouncer
    platform_map = OrderedDict([
        ('arm', 'android'),
        ('x86', 'android-x86'),
    ])

    # Product names defined in bouncer
    product_map = {
        'beta': 'fennec-beta-latest',
        'release': 'fennec-latest',
    }

    store_url = settings.GOOGLE_PLAY_FIREFOX_LINK
    # Product IDs defined on Google Play
    # Nightly reuses the Aurora ID to migrate the user base
    store_product_ids = {
        'nightly': 'org.mozilla.fennec_aurora',
        'beta': 'org.mozilla.firefox_beta',
        'release': 'org.mozilla.firefox',
    }

    archive_url_base = ('https://archive.mozilla.org/pub/mobile/nightly/'
                        'latest-mozilla-%s-android')
    archive_repo = {
        'nightly': 'central',
    }
    archive_urls = {
        'arm': archive_url_base + '-%s/fennec-%s.multi.android-arm.apk',
        'x86': archive_url_base + '-%s/fennec-%s.multi.android-i386.apk',
    }

    def platforms(self, channel='release', classified=False):
        """
        Get the Android platform dictionary containing slugs and corresponding
        labels. The classified option is unused but required to match the
        FirefoxDesktop implementation.
        """
        # Use an OrderedDict to always put the ARM build in front
        platforms = OrderedDict()

        # Supported Android version has been changed with Firefox 56
        version_int = self.latest_major_version(channel)
        min_version = '4.0.3' if version_int < 56 else '4.1'

        # key is a bouncer platform name, value is the human-readable label
        for arch, platform in self.platform_map.iteritems():
            platforms[platform] = self.platform_labels[arch] % min_version

        return platforms.items()

    def latest_version(self, channel):
        version = self.version_map.get(channel, 'version')
        return self.mobile_details[version]

    def latest_major_version(self, channel):
        """Return latest major version as an int."""
        lv = self.latest_version(channel)
        if lv is None:
            return 0

        try:
            return int(lv.split('.')[0])
        except ValueError:
            return 0

    def _get_filtered_builds(self, builds, channel, version=None, query=None):
        """
        Get a list of builds, sorted by english locale name, for a specific
        Firefox version.
        :param builds: a build dict from the JSON
        :param channel: one of self.version_map.keys().
        :param version: a firefox version. one of self.latest_versions.
        :param query: a string to match against native or english locale name
        :return: list
        """
        locales = [build['locale']['code'] for build in builds]
        f_builds = []

        # For now, only list the multi-locale builds because the single-locale
        # builds are fragile (Bug 1301650)
        locales = ['multi']

        for locale in locales:
            if locale == 'multi':
                name_en = _('Multi-locale')
                name_native = ''
            elif locale in self.languages:
                name_en = self.languages[locale]['English']
                name_native = self.languages[locale]['native']
            else:
                continue

            build_info = {
                'locale': locale,
                'name_en': name_en,
                'name_native': name_native,
                'platforms': {},
            }

            # only include builds that match a search query
            if query is not None and not self._matches_query(build_info, query):
                continue

            for arch, platform in self.platform_map.iteritems():
                # x86 builds are not localized yet
                if arch == 'x86' and locale not in ['multi', 'en-US']:
                    continue

                # Use a direct link instead of Google Play for the /all/ page
                url = self.get_download_url(channel, arch, locale, True)
                build_info['platforms'][platform] = {'download_url': url}

            f_builds.append(build_info)

        return f_builds

    def get_filtered_full_builds(self, channel, version=None, query=None):
        """
        Return filtered builds for the fully translated releases.
        :param channel: one of self.version_map.keys().
        :param version: a firefox version. one of self.latest_version.
        :param query: a string to match against native or english locale name
        :return: list
        """
        builds = self.mobile_details[self.build_map.get(channel, 'builds')]

        return self._get_filtered_builds(builds, channel, version, query)

    def get_filtered_test_builds(self, channel, version=None, query=None):
        # We don't have pre-release builds yet
        return []

    def get_download_url(self, channel='release', arch='arm', locale='multi',
                         force_direct=False):
        """
        Get direct download url for the product.
        :param channel: one of self.version_map.keys() such as nightly, beta.
        :param arch: one of self.platform_map.keys() either arm or x86.
        :param locale: e.g. pt-BR.
        :param force_direct: Force the download URL to be direct or bouncer
                instead of Google Play.
        :return: string url
        """
        if force_direct:
            # Use a direct archive link for Nightly
            if channel == 'nightly':
                if arch == 'x86':
                    api_version = 'x86'
                elif self.latest_major_version(channel) < 56:
                    api_version = 'api-15'
                else:
                    api_version = 'api-16'

                return self.archive_urls[arch] % (self.archive_repo[channel],
                                                  api_version,
                                                  self.latest_version(channel))

            # Use a bouncer link for Beta/Release
            return '?'.join([self.bouncer_url, urlencode([
                ('product', self.product_map.get(channel, 'fennec-latest')),
                ('os', self.platform_map[arch]),
                # Order matters, lang must be last for bouncer.
                ('lang', locale),
            ])])

        if channel != 'release':
            product_id = self.store_product_ids.get(channel, 'org.mozilla.firefox')
            return self.store_url.replace(self.store_product_ids['release'], product_id)

        return self.store_url


class FirefoxIOS(_ProductDetails):
    # Version property names in product-details
    version_map = {
        'beta': 'ios_beta_version',
        'release': 'ios_version',
    }
    store_url = settings.APPLE_APPSTORE_FIREFOX_LINK

    def latest_version(self, channel):
        version = self.version_map.get(channel, 'ios_version')
        return self.mobile_details[version]

    def get_download_url(self, channel='release', locale='en-US'):
        countries = settings.APPLE_APPSTORE_COUNTRY_MAP

        if locale in countries:
            return self.store_url.format(country=countries[locale])

        return self.store_url.replace('/{country}/', '/')


firefox_desktop = FirefoxDesktop()
firefox_android = FirefoxAndroid()
firefox_ios = FirefoxIOS()
