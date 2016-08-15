# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
from urlparse import parse_qsl, urlparse

from django.conf import settings
from django.core.cache import caches
from django.test.utils import override_settings

from mock import patch, Mock
from nose.tools import eq_, ok_

from bedrock.firefox.firefox_details import FirefoxDesktop, FirefoxAndroid, FirefoxIOS
from bedrock.mozorg.tests import TestCase


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
PROD_DETAILS_DIR = os.path.join(TEST_DATA_DIR, 'product_details_json')


firefox_desktop = FirefoxDesktop(json_dir=PROD_DETAILS_DIR)
firefox_android = FirefoxAndroid(json_dir=PROD_DETAILS_DIR)
firefox_ios = FirefoxIOS(json_dir=PROD_DETAILS_DIR)


GOOD_PLATS = {'Windows': {}, 'OS X': {}, 'Linux': {}}
GOOD_BUILDS = {
    'en-US': {
        '25.0': GOOD_PLATS,  # current release
        '26.0b2': GOOD_PLATS,
        '27.0a1': GOOD_PLATS,
    },
    'de': {
        '25.0': GOOD_PLATS,
    },
    'fr': {
        '24.0': GOOD_PLATS,  # prev release
    }
}
GOOD_VERSIONS = {
    'LATEST_FIREFOX_VERSION': '25.0',
    'LATEST_FIREFOX_DEVEL_VERSION': '26.0b2',
    'FIREFOX_AURORA': '27.0a1',
    'FIREFOX_ESR': '24.1.0esr',
}


@patch.object(firefox_desktop, 'firefox_primary_builds', GOOD_BUILDS)
@patch.object(firefox_desktop, 'firefox_beta_builds', {})
@patch.object(firefox_desktop, 'firefox_versions', GOOD_VERSIONS)
class TestLatestBuilds(TestCase):
    def test_latest_builds(self):
        """Should return platforms if localized build does exist."""
        result = firefox_desktop.latest_builds('de', 'release')
        self.assertEqual(result[0], '25.0')
        self.assertIs(result[1], GOOD_PLATS)

    def test_latest_builds_is_none_if_no_build(self):
        """Should return None if the localized build for the channel doesn't exist."""
        result = firefox_desktop.latest_builds('fr', 'release')
        self.assertIsNone(result)

    def test_latest_builds_channels(self):
        """Should work with all channels."""
        result = firefox_desktop.latest_builds('en-US', 'beta')
        self.assertEqual(result[0], '26.0b2')
        self.assertIs(result[1], GOOD_PLATS)

        result = firefox_desktop.latest_builds('en-US', 'alpha')
        self.assertEqual(result[0], '27.0a1')
        self.assertIs(result[1], GOOD_PLATS)


class TestFirefoxDesktop(TestCase):
    pd_cache = caches['product-details']

    def setUp(self):
        self.pd_cache.clear()

    def test_get_download_url(self):
        url = firefox_desktop.get_download_url('release', '17.0.1', 'osx', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-17.0.1-SSL'),
                              ('os', 'osx'),
                              ('lang', 'pt-BR')])
        # Windows 64-bit
        url = firefox_desktop.get_download_url('release', '38.0', 'win64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-38.0-SSL'),
                              ('os', 'win64'),
                              ('lang', 'en-US')])
        # Linux 64-bit
        url = firefox_desktop.get_download_url('release', '17.0.1', 'linux64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-17.0.1-SSL'),
                              ('os', 'linux64'),
                              ('lang', 'en-US')])

    def test_get_download_url_aurora(self):
        """
        The Aurora version should give us a bouncer url. For Windows, a stub url
        should be returned.
        """
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'win', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-aurora-stub'),
                              ('os', 'win'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'win64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-aurora-latest-ssl'),
                              ('os', 'win64'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'osx', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-aurora-latest-ssl'),
                              ('os', 'osx'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'linux', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-aurora-latest-ssl'),
                              ('os', 'linux'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'linux64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-aurora-latest-ssl'),
                              ('os', 'linux64'),
                              ('lang', 'en-US')])

    def test_get_download_url_aurora_l10n(self):
        """Aurora non en-US should have a slightly different product name."""
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'win', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-aurora-latest-l10n'),
                              ('os', 'win'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'win64', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-aurora-latest-l10n'),
                              ('os', 'win64'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'osx', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-aurora-latest-l10n'),
                              ('os', 'osx'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'linux', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-aurora-latest-l10n'),
                              ('os', 'linux'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'linux64', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-aurora-latest-l10n'),
                              ('os', 'linux64'),
                              ('lang', 'pt-BR')])

    def test_get_download_url_scene2_funnelcake(self):
        scene2 = firefox_desktop.download_base_url_transition
        url = firefox_desktop.get_download_url('release', '45.0', 'win', 'en-US')
        self.assertEqual(url, scene2)
        url = firefox_desktop.get_download_url('release', '45.0', 'win', 'en-US', funnelcake_id='64')
        self.assertEqual(url, scene2 + '&f=64')

    @override_settings(STUB_INSTALLER_LOCALES={'win': settings.STUB_INSTALLER_ALL})
    def get_download_url_ssl(self):
        """
        SSL-enabled links should always be used except Windows stub installers.
        """

        # SSL-enabled links won't be used for Windows builds (but SSL download
        # is enabled by default for stub installers)
        url = firefox_desktop.get_download_url('release', '27.0', 'win', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-27.0'),
                              ('os', 'win'),
                              ('lang', 'pt-BR')])

        # SSL-enabled links will be used for OS X builds
        url = firefox_desktop.get_download_url('release', '27.0', 'osx', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-27.0-SSL'),
                              ('os', 'osx'),
                              ('lang', 'pt-BR')])

        # SSL-enabled links will be used for Linux builds
        url = firefox_desktop.get_download_url('release', '27.0', 'linux', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-27.0-SSL'),
                              ('os', 'linux'),
                              ('lang', 'pt-BR')])

    def test_filter_builds_by_locale_name(self):
        # search english
        builds = firefox_desktop.get_filtered_full_builds('release', None,
                                                          'ujara')
        eq_(len(builds), 1)
        eq_(builds[0]['name_en'], 'Gujarati')

        # search native
        builds = firefox_desktop.get_filtered_full_builds('release', None,
                                                          u'જરા')
        eq_(len(builds), 1)
        eq_(builds[0]['name_en'], 'Gujarati')

        # with a space
        builds = firefox_desktop.get_filtered_full_builds('release', None,
                                                          'british english')
        eq_(len(builds), 1)
        eq_(builds[0]['name_en'], 'English (British)')

        # with a comma
        builds = firefox_desktop.get_filtered_full_builds('release', None,
                                                          u'French, Français')
        eq_(len(builds), 1)
        eq_(builds[0]['name_en'], 'French')

    def test_windows64_build(self):
        # Aurora
        builds = firefox_desktop.get_filtered_full_builds('alpha')
        url = builds[0]['platforms']['win64']['download_url']
        eq_(parse_qsl(urlparse(url).query)[1], ('os', 'win64'))

        # Beta
        builds = firefox_desktop.get_filtered_full_builds('beta')
        url = builds[0]['platforms']['win64']['download_url']
        eq_(parse_qsl(urlparse(url).query)[1], ('os', 'win64'))

        # Release
        builds = firefox_desktop.get_filtered_full_builds('release')
        url = builds[0]['platforms']['win64']['download_url']
        eq_(parse_qsl(urlparse(url).query)[1], ('os', 'win64'))

        # ESR
        builds = firefox_desktop.get_filtered_full_builds('esr')
        url = builds[0]['platforms']['win64']['download_url']
        eq_(parse_qsl(urlparse(url).query)[1], ('os', 'win64'))

    def test_linux64_build(self):
        builds = firefox_desktop.get_filtered_full_builds('release')
        url = builds[0]['platforms']['linux64']['download_url']
        eq_(parse_qsl(urlparse(url).query)[1], ('os', 'linux64'))

    @patch.object(firefox_desktop._storage, 'data',
                  Mock(return_value=dict(FIREFOX_ESR='24.2')))
    def test_esr_versions(self):
        """ESR versions should be dynamic based on data."""
        eq_(firefox_desktop.esr_major_versions, [24])
        eq_(firefox_desktop.esr_minor_versions, ['24.2'])

    @patch.object(firefox_desktop._storage, 'data',
                  Mock(return_value=dict(FIREFOX_ESR='24.6.0',
                                         FIREFOX_ESR_NEXT='31.0.0')))
    def test_esr_versions_prev(self):
        """ESR versions should show previous when available."""
        eq_(firefox_desktop.esr_major_versions, [24, 31])
        eq_(firefox_desktop.esr_minor_versions, ['24.6.0', '31.0.0'])

    @patch.object(firefox_desktop._storage, 'data',
                  Mock(return_value=dict(LATEST_FIREFOX_VERSION='Phoenix',
                                         FIREFOX_ESR='Albuquerque')))
    def test_esr_versions_no_latest(self):
        """ESR versions should not blow up if current version is broken."""
        eq_(firefox_desktop.esr_major_versions, [])
        eq_(firefox_desktop.esr_minor_versions, [])

    @patch.object(firefox_desktop._storage, 'data',
                  Mock(return_value=dict(LATEST_FIREFOX_VERSION='18.0.1')))
    def test_latest_major_version(self):
        """latest_major_version should return an int of the major version."""
        eq_(firefox_desktop.latest_major_version('release'), 18)

    @patch.object(firefox_desktop._storage, 'data',
                  Mock(return_value=dict(LATEST_FIREFOX_VERSION='Phoenix')))
    def test_latest_major_version_no_int(self):
        """latest_major_version should return 0 when no int."""
        eq_(firefox_desktop.latest_major_version('release'), 0)

    @override_settings(STUB_INSTALLER_LOCALES={'win': ['en-us']})
    def test_force_funnelcake_en_us_win_only(self):
        """
        Ensure that force_funnelcake doesn't affect non configured locale urls
        """
        url = firefox_desktop.get_download_url('release', '19.0', 'osx', 'en-US',
                                               force_funnelcake=True)
        ok_('product=firefox-latest&' not in url)

        url = firefox_desktop.get_download_url('beta', '20.0b4', 'win', 'fr',
                                               force_funnelcake=True)
        ok_('product=firefox-beta-latest&' not in url)

    @override_settings(STUB_INSTALLER_LOCALES={'win': ['en-us']})
    def test_force_full_installer_en_us_win_only(self):
        """
        Ensure that force_full_installer doesn't affect non configured locales
        """
        url = firefox_desktop.get_download_url('release', '19.0', 'osx', 'en-US',
                                               force_full_installer=True)
        ok_('product=firefox-latest&' not in url)

        url = firefox_desktop.get_download_url('beta', '20.0b4', 'win', 'fr',
                                               force_full_installer=True)
        ok_('product=firefox-beta-latest&' not in url)

    @override_settings(STUB_INSTALLER_LOCALES={'win': ['en-us']})
    def test_stub_installer_en_us_win_only(self):
        """
        Ensure that builds not in the setting don't get stub.
        """
        url = firefox_desktop.get_download_url('release', '19.0', 'osx', 'en-US')
        ok_('product=firefox-stub&' not in url)

        url = firefox_desktop.get_download_url('beta', '20.0b4', 'win', 'fr')
        ok_('product=firefox-beta-stub&' not in url)


@patch.object(firefox_android._storage, 'data',
              Mock(return_value=dict(version='22.0.1', beta_version='23.0')))
class TestFirefoxAndroid(TestCase):

    def test_latest_release_version(self):
        """latest_version should return the latest release version."""
        eq_(firefox_android.latest_version('release'), '22.0.1')

    def test_latest_beta_version(self):
        """latest_version should return the latest beta version."""
        eq_(firefox_android.latest_version('beta'), '23.0')

    @patch.object(firefox_android, 'latest_version', Mock(return_value='48.0a2'))
    def test_latest_alpha_platforms(self):
        """Android Gingerbread (2.3) is no longer supported as of Firefox 48"""
        platforms = [key for (key, value) in firefox_android.platforms('alpha')]
        eq_(platforms, ['android', 'android-x86'])

    @patch.object(firefox_android, 'latest_version', Mock(return_value='47.0a2'))
    def test_legacy_alpha_platforms(self):
        """Android Gingerbread (2.3) is supported as of Firefox 47"""
        platforms = [key for (key, value) in firefox_android.platforms('alpha')]
        eq_(platforms, ['android', 'android-api-9', 'android-x86'])


@override_settings(FIREFOX_IOS_RELEASE_VERSION='1.4')
class TestFirefoxIos(TestCase):

    def test_latest_release_version(self):
        """latest_version should return the latest release version."""
        eq_(firefox_ios.latest_version('release'), '1.4')
