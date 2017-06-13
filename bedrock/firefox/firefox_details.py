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
    download_base_url_transition = '/firefox/new/?scene=2'

    # Human-readable platform names
    platform_labels = OrderedDict([
        ('winsha1', 'Windows (XP/Vista)'),
        ('win', 'Windows'),
        ('win64', 'Windows 64-bit'),
        ('osx', 'macOS'),
        ('linux', 'Linux'),
        ('linux64', 'Linux 64-bit'),
    ])

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
                         force_funnelcake=False, funnelcake_id=None,
                         locale_in_transition=False):
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
        :param locale_in_transition: Include the locale in the transition URL
        :return: string url
        """
        _version = version
        _locale = 'ja-JP-mac' if platform == 'osx' and locale == 'ja' else locale
        _platform = 'win' if platform == 'winsha1' else platform
        include_funnelcake_param = False

        # Bug 1345467 - Only allow specifically configured funnelcake builds
        if funnelcake_id:
            fc_platforms = config('FUNNELCAKE_%s_PLATFORMS' % funnelcake_id, default='', cast=Csv())
            fc_locales = config('FUNNELCAKE_%s_LOCALES' % funnelcake_id, default='', cast=Csv())
            include_funnelcake_param = _platform in fc_platforms and _locale in fc_locales

        stub_langs = settings.STUB_INSTALLER_LOCALES.get(channel, {}).get(_platform, [])
        # Nightly and Aurora have a special download link format
        # see bug 1324001
        if channel in ['alpha', 'nightly']:
            prod_name = 'firefox-nightly' if channel == 'nightly' else 'firefox-aurora'
            # Use the stub installer for approved platforms
            if (stub_langs and (stub_langs == settings.STUB_INSTALLER_ALL or _locale.lower() in stub_langs) and
                    not force_full_installer):
                # Download links are different for localized versions
                suffix = 'stub'
            else:
                suffix = 'latest-ssl'
                if locale != 'en-US':
                    suffix = 'latest-l10n-ssl'

            product = '%s-%s' % (prod_name, suffix)

            return '?'.join([self.get_bouncer_url(platform),
                             urlencode([
                                 ('product', product),
                                 ('os', _platform),
                                 # Order matters, lang must be last for bouncer.
                                 ('lang', _locale),
                             ])])

        # stub installer exceptions
        if (stub_langs and (stub_langs == settings.STUB_INSTALLER_ALL or _locale.lower() in stub_langs) and
                not force_full_installer):
            suffix = 'stub'
            if force_funnelcake:
                suffix = 'latest'

            _version = ('beta-' if channel == 'beta' else '') + suffix
        elif not include_funnelcake_param:
            # Force download via SSL. Stub installers are always downloaded via SSL.
            # Funnelcakes may not be ready for SSL download
            _version += '-SSL'

        # append funnelcake id to version if we have one
        if include_funnelcake_param:
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
            transition_url = self.download_base_url_transition
            if funnelcake_id:
                # include funnelcake in scene 2 URL
                transition_url += '&f=%s' % funnelcake_id

            if locale_in_transition:
                transition_url = '/%s%s' % (locale, transition_url)

            return transition_url


class FirefoxAndroid(_ProductDetails):
    # Architecture names defined in bouncer and these human-readable names
    platform_labels = OrderedDict([
        ('api-15', _('ARM devices\n(Android 4.0.3+)')),
        ('x86', _('Intel devices\n(Android 4.0.3+ x86 CPU)')),
    ])

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
        ('api-15', 'android'),
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
        'api-15': archive_url_base + '-api-15/fennec-%s.multi.android-arm.apk',
        'x86': archive_url_base + '-x86/fennec-%s.multi.android-i386.apk',
    }

    def platforms(self, channel='release'):
        # Use an OrderedDict to always put the api-15 build in front
        platforms = OrderedDict()

        # key is a bouncer platform name, value is the human-readable label
        for arch, platform in self.platform_map.iteritems():
            platforms[platform] = self.platform_labels[arch]

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

    def get_download_url(self, channel='release', arch='api-15', locale='multi',
                         force_direct=False):
        """
        Get direct download url for the product.
        :param channel: one of self.version_map.keys() such as nightly, beta.
        :param arch: one of self.platform_map.keys() such as api-15, x86.
        :param locale: e.g. pt-BR.
        :param force_direct: Force the download URL to be direct or bouncer
                instead of Google Play.
        :return: string url
        """
        if force_direct:
            # Use a direct archive link for Nightly
            if channel == 'nightly':
                return self.archive_urls[arch] % (self.archive_repo[channel],
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
