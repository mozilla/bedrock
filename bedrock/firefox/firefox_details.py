import re
from collections import OrderedDict
from operator import itemgetter
from urllib import urlencode

from django.conf import settings
from product_details import ProductDetails


# TODO: port this to django-mozilla-product-details
class FirefoxDesktop(ProductDetails):
    download_base_url_direct = 'https://download.mozilla.org/'
    download_base_url_transition = '/firefox/new/?scene=2#download-fx'

    platform_labels = OrderedDict([
        ('win', 'Windows'),
        ('win64', 'Windows 64-bit'),
        ('osx', 'OS X'),
        ('linux', 'Linux'),
        ('linux64', 'Linux 64-bit'),
    ])
    channel_map = {
        'alpha': 'FIREFOX_AURORA',
        'beta': 'LATEST_FIREFOX_DEVEL_VERSION',
        'esr': 'FIREFOX_ESR',
        'esr_next': 'FIREFOX_ESR_NEXT',
        'release': 'LATEST_FIREFOX_VERSION',
    }

    def __init__(self):
        super(FirefoxDesktop, self).__init__()

    def latest_version(self, channel='release'):
        version = self.channel_map.get(channel, 'LATEST_FIREFOX_VERSION')
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
        for version in ('esr', 'esr_next'):
            version_int = self.latest_major_version(version)
            if version_int:
                versions.append(version_int)

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

    def _matches_query(self, info, query):
        words = re.split(r',|,?\s+', query.strip().lower())
        return all((word in info['name_en'].lower() or
                    word in info['name_native'].lower()) for word in words)

    def _get_filtered_builds(self, builds, channel, version=None, query=None):
        """
        Get a list of builds, sorted by english locale name, for a specific
        Firefox version.
        :param builds: a build dict from the JSON
        :param channel: one of self.channel_map.keys().
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
                # Windows 64-bit builds are currently available only on the
                # Aurora channel
                if platform == 'win64' and channel not in ['alpha']:
                    continue

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
        :param version: a firefox version. one of self.latest_version.
        :param query: a string to match against native or english locale name
        :return: list
        """
        return self._get_filtered_builds(self.firefox_primary_builds,
                                         channel, version, query)

    def get_filtered_test_builds(self, channel, version=None, query=None):
        """
        Return filtered builds for the translated releases in beta.
        :param channel: one of self.channel_map.keys().
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
        :param channel: one of self.channel_map.keys().
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

            return '?'.join([self.download_base_url_direct,
                             urlencode([
                                 ('product', product),
                                 ('os', platform),
                                 # Order matters, lang must be last for bouncer.
                                 ('lang', locale),
                             ])])

        # stub installer exceptions
        # TODO: NUKE FROM ORBIT!
        stub_langs = settings.STUB_INSTALLER_LOCALES.get(platform, [])
        if (stub_langs and (stub_langs == settings.STUB_INSTALLER_ALL or
                            _locale.lower() in stub_langs) and
                           channel in ['beta', 'release']):
            suffix = 'stub'
            if force_funnelcake or force_full_installer:
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
            return '?'.join([self.download_base_url_direct,
                             urlencode([
                                 ('product', 'firefox-%s' % _version),
                                 ('os', platform),
                                 # Order matters, lang must be last for bouncer.
                                 ('lang', _locale),
                             ])])
        else:
            # build a link to the transition page
            return self.download_base_url_transition


class FirefoxAndroid(ProductDetails):
    channel_map = {
        'alpha': 'alpha_version',
        'beta': 'beta_version',
        'release': 'version',
    }
    store_url = settings.GOOGLE_PLAY_FIREFOX_LINK
    aurora_url_base = ('https://ftp.mozilla.org/pub/mozilla.org/mobile/nightly/'
                       'latest-mozilla-aurora-android')
    aurora_urls = {
        'api-9': aurora_url_base + '-api-9/fennec-%s.multi.android-arm.apk',
        'api-11': aurora_url_base + '-api-11/fennec-%s.multi.android-arm.apk',
        'x86': aurora_url_base + '-x86/fennec-%s.multi.android-i386.apk',
    }

    def __init__(self):
        super(FirefoxAndroid, self).__init__()

    def latest_version(self, channel):
        version = self.channel_map.get(channel, 'version')
        return self.mobile_details[version]

    def get_download_url(self, channel, type=None):
        if channel == 'alpha':
            return self.aurora_urls[type] % self.latest_version('alpha')

        if channel == 'beta':
            return self.store_url.replace('org.mozilla.firefox',
                                          'org.mozilla.firefox_beta')

        return self.store_url


firefox_desktop = FirefoxDesktop()
firefox_android = FirefoxAndroid()
