import re
from collections import OrderedDict
from operator import itemgetter
from urllib import urlencode

from django.conf import settings
from product_details import ProductDetails
from lib.l10n_utils.dotlang import _lazy as _


# TODO: port this to django-mozilla-product-details
class _ProductDetails(ProductDetails):
    bouncer_url = 'https://download.mozilla.org/'

    def _matches_query(self, info, query):
        words = re.split(r',|,?\s+', query.strip().lower())
        return all((word in info['name_en'].lower() or
                    word in info['name_native'].lower()) for word in words)


class FirefoxDesktop(_ProductDetails):
    download_base_url_transition = '/firefox/new/?scene=2'

    # Human-readable platform names
    platform_labels = OrderedDict([
        ('win', 'Windows'),
        ('win64', 'Windows 64-bit'),
        ('osx', 'OS X'),
        ('linux', 'Linux'),
        ('linux64', 'Linux 64-bit'),
    ])

    # Human-readable channel names
    channel_labels = {
        'alpha': _('Developer Edition'),
        'beta': _('Firefox Beta'),
        'esr': _('Firefox Extended Support Release'),
        'release': _('Firefox'),
    }

    # Version property names in product-details
    version_map = {
        'alpha': 'FIREFOX_AURORA',
        'beta': 'LATEST_FIREFOX_DEVEL_VERSION',
        'esr': 'FIREFOX_ESR',
        'esr_next': 'FIREFOX_ESR_NEXT',
        'release': 'LATEST_FIREFOX_VERSION',
    }

    def __init__(self, **kwargs):
        super(FirefoxDesktop, self).__init__(**kwargs)

    def platforms(self, channel='release'):
        platforms = self.platform_labels.copy()

        return platforms.items()

    def latest_version(self, channel='release'):
        version = self.version_map.get(channel, 'LATEST_FIREFOX_VERSION')
        try:
            return self.firefox_versions[version]
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
                # Append 64-bit builds
                if 'Windows' in _builds:
                    _builds['Windows 64-bit'] = _builds['Windows']
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
                # Windows 64-bit builds are not available in Firefox 38 ESR
                # TODO: Remove this exception once 38 ESR reaches EOL on 2016-06-07
                if platform == 'win64' and channel == 'esr':
                    continue

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
                         force_funnelcake=False, funnelcake_id=None):
        """
        Get direct download url for the product.
        :param channel: one of self.version_map.keys().
        :param version: a firefox version. one of self.latest_version.
        :param platform: OS. one of self.platform_labels.keys().
        :param locale: e.g. pt-BR. one exception is ja-JP-mac.
        :param force_direct: Force the download URL to be direct.
        :param force_full_installer: Force the installer download to not be
                the stub installer (for aurora).
        :param force_funnelcake: Force the download version for en-US Windows to be
                'latest', which bouncer will translate to the funnelcake build.
        :param funnelcake_id: ID for the the funnelcake build.
        :return: string url
        """
        _version = version
        _locale = 'ja-JP-mac' if platform == 'osx' and locale == 'ja' else locale

        # Aurora has a special download link format
        if channel == 'alpha':
            # Download links are different for localized versions
            if locale == 'en-US':
                # Use the stub installer for 32-bit Windows
                if platform == 'win':
                    product = 'firefox-aurora-stub'
                else:
                    product = 'firefox-aurora-latest-ssl'
            else:
                product = 'firefox-aurora-latest-l10n'

            return '?'.join([self.bouncer_url,
                             urlencode([
                                 ('product', product),
                                 ('os', platform),
                                 # Order matters, lang must be last for bouncer.
                                 ('lang', _locale),
                             ])])

        # stub installer exceptions
        # TODO: NUKE FROM ORBIT!
        stub_langs = settings.STUB_INSTALLER_LOCALES.get(platform, [])
        if (stub_langs and (stub_langs == settings.STUB_INSTALLER_ALL or
                            _locale.lower() in stub_langs) and
                           not force_full_installer and
                           channel in ['beta', 'release']):
            suffix = 'stub'
            if force_funnelcake:
                suffix = 'latest'

            _version = ('beta-' if channel == 'beta' else '') + suffix
        elif not funnelcake_id:
            # Force download via SSL. Stub installers are always downloaded via SSL.
            # Funnelcakes may not be ready for SSL download
            _version += '-SSL'

        # append funnelcake id to version if we have one
        if funnelcake_id:
            _version = '{vers}-f{fc}'.format(vers=_version, fc=funnelcake_id)

        # Check if direct download link has been requested
        # (bypassing the transition page)
        if force_direct:
            # build a direct download link
            return '?'.join([self.bouncer_url,
                             urlencode([
                                 ('product', 'firefox-%s' % _version),
                                 ('os', platform),
                                 # Order matters, lang must be last for bouncer.
                                 ('lang', _locale),
                             ])])
        else:
            # build a link to the transition page

            if funnelcake_id:
                # include funnelcake in scene 2 URL
                return '&f='.join([self.download_base_url_transition,
                                   funnelcake_id])
            else:
                return self.download_base_url_transition


class FirefoxAndroid(_ProductDetails):
    # Architecture names defined in bouncer and these human-readable names
    platform_labels = OrderedDict([
        ('android', _('Modern devices\n(Android 4.0+)')),
        ('android-api-9', _('Legacy devices\n(Android 2.3)')),
        ('android-x86', _('Intel devices\n(Android 4.0+ x86 CPU)')),
    ])

    # Human-readable channel names
    channel_labels = {
        'alpha': _('Firefox Aurora'),
        'beta': _('Firefox Beta'),
        'release': _('Firefox'),
    }

    # Version property names in product-details
    version_map = {
        'alpha': 'alpha_version',
        'beta': 'beta_version',
        'release': 'version',
    }

    # Build property names in product-details
    build_map = {
        'alpha': 'alpha_builds',
        'beta': 'beta_builds',
        'release': 'builds',
    }

    # Product names defined in bouncer
    product_map = {
        'beta': 'fennec-beta-latest',
        'release': 'fennec-latest',
    }

    store_url = settings.GOOGLE_PLAY_FIREFOX_LINK
    aurora_url_base = ('https://archive.mozilla.org/pub/mobile/nightly/'
                       'latest-mozilla-aurora-android')
    aurora_urls = {
        'api-9': aurora_url_base + '-api-9/fennec-%s.multi.android-arm.apk',
        'api-15': aurora_url_base + '-api-15/fennec-%s.multi.android-arm.apk',
        'x86': aurora_url_base + '-x86/fennec-%s.multi.android-i386.apk',
    }

    def platforms(self, channel='release'):
        platforms = self.platform_labels.copy()

        # Android Honeycomb (3.x) was supported on Firefox 45 and below
        if int(self.latest_version(channel).split('.', 1)[0]) < 46:
            platforms['android'] = _('Modern devices\n(Android 3.0+)')

        return platforms.items()

    def latest_version(self, channel):
        version = self.version_map.get(channel, 'version')
        return self.mobile_details[version]

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
        product = self.product_map.get(channel, 'fennec-latest')
        locales = [build['locale']['code'] for build in builds]
        f_builds = []

        # Prepend multi-locale build
        locales.sort()
        locales.insert(0, 'multi')

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

            for arch, label in self.platform_labels.iteritems():
                # x86 builds are not localized yet
                if arch == 'android-x86' and locale not in ['multi', 'en-US']:
                    continue

                params = urlencode([
                    ('product', product),
                    ('os', arch),
                    # Order matters, lang must be last for bouncer.
                    ('lang', locale),
                ])

                build_info['platforms'][arch] = {
                    'download_url': '?'.join([self.bouncer_url, params])
                }

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

    def get_download_url(self, channel, type=None):
        if channel == 'alpha':
            return self.aurora_urls[type] % self.latest_version('alpha')

        if channel == 'beta':
            return self.store_url.replace('org.mozilla.firefox',
                                          'org.mozilla.firefox_beta')

        return self.store_url


class FirefoxIOS(_ProductDetails):
    version_map = {
        'release': 'version',
    }
    store_url = settings.APPLE_APPSTORE_FIREFOX_LINK

    def latest_version(self, channel):
        # temporary solution until iOS builds are in ProductDetails
        return settings.FIREFOX_IOS_RELEASE_VERSION

    def get_download_url(self, channel='release', locale='en-US'):
        countries = settings.APPLE_APPSTORE_COUNTRY_MAP

        if locale in countries:
            return self.store_url.format(country=countries[locale])

        return self.store_url.replace('/{country}/', '/')


firefox_desktop = FirefoxDesktop()
firefox_android = FirefoxAndroid()
firefox_ios = FirefoxIOS()
