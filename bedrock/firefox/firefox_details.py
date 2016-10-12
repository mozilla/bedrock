import re
from collections import OrderedDict
from operator import itemgetter
from urllib import urlencode

from django.conf import settings
from bedrock.base.waffle import switch
from product_details import ProductDetails
from lib.l10n_utils.dotlang import _lazy as _


# TODO: port this to django-mozilla-product-details
class _ProductDetails(ProductDetails):
    bouncer_url = 'https://download.mozilla.org/'

    # Note allizom.org is the production endpoint for SHA-1.
    # It uses this because that's the only SHA-1 certificate
    # we have that's usable. (SHA-1 certs can no longer be issued).
    sha1_bouncer_url = 'https://download-sha1.allizom.org/'

    def _matches_query(self, info, query):
        words = re.split(r',|,?\s+', query.strip().lower())
        return all((word in info['name_en'].lower() or
                    word in info['name_native'].lower()) for word in words)


class FirefoxDesktop(_ProductDetails):
    download_base_url_transition = '/firefox/new/?scene=2'
    nightly_url_base = ('https://archive.mozilla.org/pub/firefox/nightly/'
                        'latest-mozilla-central')

    # Human-readable platform names
    platform_labels = OrderedDict([
        ('winsha1', 'Windows (XP/Vista)'),
        ('win', 'Windows'),
        ('win64', 'Windows 64-bit'),
        ('osx', 'OS X'),
        ('linux', 'Linux'),
        ('linux64', 'Linux 64-bit'),
    ])

    # Firefox Nightly file name suffixes
    platform_file_suffixes = {
        'win': 'win32.installer.exe',
        'win64': 'win64.installer.exe',
        'osx': 'mac.dmg',
        'linux': 'linux-i686.tar.bz2',
        'linux64': 'linux-x86_64.tar.bz2',
    }

    # Human-readable channel names
    channel_labels = {
        'nightly': _('Firefox Nightly'),
        'alpha': _('Developer Edition'),
        'beta': _('Firefox Beta'),
        'esr': _('Firefox Extended Support Release'),
        'release': _('Firefox'),
    }

    # Version property names in product-details
    version_map = {
        'nightly': 'FIREFOX_NIGHTLY',
        'alpha': 'FIREFOX_AURORA',
        'beta': 'LATEST_FIREFOX_DEVEL_VERSION',
        'esr': 'FIREFOX_ESR',
        'esr_next': 'FIREFOX_ESR_NEXT',
        'release': 'LATEST_FIREFOX_VERSION',
    }

    def __init__(self, **kwargs):
        super(FirefoxDesktop, self).__init__(**kwargs)

    def get_bouncer_url(self, platform):
        return self.sha1_bouncer_url if not switch('disable-sha1-downloads') and platform == 'winsha1' else self.bouncer_url

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
        _platform = 'win' if platform == 'winsha1' else platform

        # Aurora has a special download link format
        if channel == 'alpha':
            # Download links are different for localized versions
            if locale == 'en-US':
                # Use the stub installer for 32-bit Windows
                if _platform == 'win':
                    product = 'firefox-aurora-stub'
                else:
                    product = 'firefox-aurora-latest-ssl'
            else:
                product = 'firefox-aurora-latest-l10n'

            return '?'.join([self.get_bouncer_url(platform),
                             urlencode([
                                 ('product', product),
                                 ('os', _platform),
                                 # Order matters, lang must be last for bouncer.
                                 ('lang', _locale),
                             ])])

        # Use direct archive links for Nightly
        if channel == 'nightly':
            _dir = self.nightly_url_base + ('' if locale == 'en-US' else '-l10n')
            _suffix = self.platform_file_suffixes.get(_platform)

            return '{dir}/firefox-{version}.{locale}.{suffix}'.format(
                dir=_dir, version=_version, locale=_locale, suffix=_suffix)

        # stub installer exceptions
        # TODO: NUKE FROM ORBIT!
        stub_langs = settings.STUB_INSTALLER_LOCALES.get(_platform, [])
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
            return '?'.join([self.get_bouncer_url(platform),
                             urlencode([
                                 ('product', 'firefox-%s' % _version),
                                 ('os', _platform),
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
        major_version = int(self.latest_version(channel).split('.', 1)[0])

        # Android Gingerbread (2.3) is no longer supported as of Firefox 48
        if major_version >= 48:
            platforms['android'] = _('ARM devices\n(Android 4.0.3+)')
            platforms['android-x86'] = _('Intel devices\n(Android 4.0.3+ x86 CPU)')
            del platforms['android-api-9']

        # Android Honeycomb (3.x) was supported on Firefox 45 and below
        if major_version <= 45:
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
