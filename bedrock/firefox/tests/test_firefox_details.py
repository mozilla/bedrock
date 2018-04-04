# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
from urlparse import parse_qsl, urlparse

from django.core.cache import caches

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
    'FIREFOX_DEVEDITION': '26.0b2',
    'FIREFOX_AURORA': '',
    'FIREFOX_ESR': '24.1.0esr',
}
GOOD_VERSIONS_NO_DEV = {
    'LATEST_FIREFOX_VERSION': '25.0',
    'LATEST_FIREFOX_DEVEL_VERSION': '26.0b2',
    'FIREFOX_AURORA': '',
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
        self.assertEqual(result[0], '26.0b2')
        self.assertIs(result[1], GOOD_PLATS)


@patch.object(firefox_desktop, 'firefox_primary_builds', GOOD_BUILDS)
@patch.object(firefox_desktop, 'firefox_beta_builds', {})
@patch.object(firefox_desktop, 'firefox_versions', GOOD_VERSIONS_NO_DEV)
class TestLatestBuildsNoDevEdition(TestCase):
    """Should get same results as above and not blow up"""
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
        self.assertEqual(result[0], '26.0b2')
        self.assertIs(result[1], GOOD_PLATS)


class TestFirefoxDesktop(TestCase):
    pd_cache = caches['product-details']

    def setUp(self):
        self.pd_cache.clear()

    def test_get_download_url(self):
        url = firefox_desktop.get_download_url('release', '17.0.1', 'osx', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-latest-ssl'),
                              ('os', 'osx'),
                              ('lang', 'pt-BR')])
        # Windows 64-bit
        url = firefox_desktop.get_download_url('release', '38.0', 'win64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-stub'),
                              ('os', 'win64'),
                              ('lang', 'en-US')])
        # Linux 64-bit
        url = firefox_desktop.get_download_url('release', '17.0.1', 'linux64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-latest-ssl'),
                              ('os', 'linux64'),
                              ('lang', 'en-US')])

    def test_get_download_url_esr(self):
        """
        The ESR version should give us a bouncer url. There is no stub for ESR.
        """
        url = firefox_desktop.get_download_url('esr', '28.0a2', 'win', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-esr-latest-ssl'),
                              ('os', 'win'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('esr', '28.0a2', 'win64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-esr-latest-ssl'),
                              ('os', 'win64'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('esr', '28.0a2', 'osx', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-esr-latest-ssl'),
                              ('os', 'osx'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('esr', '28.0a2', 'linux', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-esr-latest-ssl'),
                              ('os', 'linux'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('esr', '28.0a2', 'linux64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-esr-latest-ssl'),
                              ('os', 'linux64'),
                              ('lang', 'en-US')])

    def test_get_download_url_esr_next(self):
        """
        The ESR_NEXT version should give us a bouncer url with a full version. There is no stub for ESR.
        """
        url = firefox_desktop.get_download_url('esr_next', '52.4.1esr', 'win', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-52.4.1esr-SSL'),
                              ('os', 'win'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('esr_next', '52.4.1esr', 'win64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-52.4.1esr-SSL'),
                              ('os', 'win64'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('esr_next', '52.4.1esr', 'osx', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-52.4.1esr-SSL'),
                              ('os', 'osx'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('esr_next', '52.4.1esr', 'linux', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-52.4.1esr-SSL'),
                              ('os', 'linux'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('esr_next', '52.4.1esr', 'linux64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-52.4.1esr-SSL'),
                              ('os', 'linux64'),
                              ('lang', 'en-US')])

    def test_get_download_url_winsha1(self):
        # sha1 should get the normal stub installer, bouncer handles the rest
        url = firefox_desktop.get_download_url('release', '56.0', 'winsha1', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-stub'),
                              ('os', 'win'),
                              ('lang', 'en-US')])

    def test_get_download_url_devedition(self):
        """
        The Developer Edition version should give us a bouncer url. For Windows,
        a stub url should be returned.
        """
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'win', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-stub'),
                              ('os', 'win'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'win64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-stub'),
                              ('os', 'win64'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'osx', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-latest-ssl'),
                              ('os', 'osx'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'linux', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-latest-ssl'),
                              ('os', 'linux'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'linux64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-latest-ssl'),
                              ('os', 'linux64'),
                              ('lang', 'en-US')])

    def test_get_download_url_devedition_full(self):
        """
        The Developer Edition version should give us a bouncer url. For Windows,
        a full url should be returned.
        """
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'win', 'en-US', True, True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-latest-ssl'),
                              ('os', 'win'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'win64', 'en-US', True, True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-latest-ssl'),
                              ('os', 'win64'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'osx', 'en-US', True, True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-latest-ssl'),
                              ('os', 'osx'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'linux', 'en-US', True, True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-latest-ssl'),
                              ('os', 'linux'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'linux64', 'en-US', True, True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-latest-ssl'),
                              ('os', 'linux64'),
                              ('lang', 'en-US')])

    def test_get_download_url_devedition_l10n(self):
        """
        The Developer Edition version should give us a bouncer url. A stub url
        should be returned for win32/64, while other platforms get a full url.
        The product name is the same as en-US.
        """
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'win', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-stub'),
                              ('os', 'win'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'win64', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-stub'),
                              ('os', 'win64'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'osx', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-latest-ssl'),
                              ('os', 'osx'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'linux', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-latest-ssl'),
                              ('os', 'linux'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('alpha', '28.0a2', 'linux64', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-devedition-latest-ssl'),
                              ('os', 'linux64'),
                              ('lang', 'pt-BR')])

    def test_get_download_url_nightly(self):
        """
        The Nightly version should give us a bouncer url. For Windows, a stub url
        should be returned.
        """
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'win', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-stub'),
                              ('os', 'win'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'win64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-stub'),
                              ('os', 'win64'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'osx', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-latest-ssl'),
                              ('os', 'osx'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'linux', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-latest-ssl'),
                              ('os', 'linux'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'linux64', 'en-US', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-latest-ssl'),
                              ('os', 'linux64'),
                              ('lang', 'en-US')])

    def test_get_download_url_nightly_full(self):
        """
        The Nightly version should give us a bouncer url. For Windows, a full url
        should be returned.
        """
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'win', 'en-US', True, True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-latest-ssl'),
                              ('os', 'win'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'win64', 'en-US', True, True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-latest-ssl'),
                              ('os', 'win64'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'osx', 'en-US', True, True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-latest-ssl'),
                              ('os', 'osx'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'linux', 'en-US', True, True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-latest-ssl'),
                              ('os', 'linux'),
                              ('lang', 'en-US')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'linux64', 'en-US', True, True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-latest-ssl'),
                              ('os', 'linux64'),
                              ('lang', 'en-US')])

    def test_get_download_url_nightly_l10n(self):
        """
        The Nightly version should give us a bouncer url. A stub url should be
        returned for win32/64, while other platforms get a full url. The product
        name is slightly different from en-US.
        """
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'win', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-stub'),
                              ('os', 'win'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'win64', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-stub'),
                              ('os', 'win64'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'osx', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-latest-l10n-ssl'),
                              ('os', 'osx'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'linux', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-latest-l10n-ssl'),
                              ('os', 'linux'),
                              ('lang', 'pt-BR')])
        url = firefox_desktop.get_download_url('nightly', '50.0a1', 'linux64', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-nightly-latest-l10n-ssl'),
                              ('os', 'linux64'),
                              ('lang', 'pt-BR')])

    def test_get_download_url_scene2_funnelcake(self):
        scene2 = firefox_desktop.download_base_url_transition
        url = firefox_desktop.get_download_url('release', '45.0', 'win', 'en-US')
        self.assertEqual(url, scene2)
        url = firefox_desktop.get_download_url('release', '45.0', 'win', 'en-US', funnelcake_id='64')
        self.assertEqual(url, scene2 + '?f=64')

    def test_get_download_url_scene2_with_locale(self):
        scene2 = firefox_desktop.download_base_url_transition
        url = firefox_desktop.get_download_url('release', '45.0', 'win', 'de',
                                               locale_in_transition=True)
        self.assertEqual(url, '/de' + scene2)

        url = firefox_desktop.get_download_url('release', '45.0', 'win', 'fr',
                                               locale_in_transition=True,
                                               funnelcake_id='64')
        self.assertEqual(url, '/fr' + scene2 + '?f=64')

    def get_download_url_ssl(self):
        """
        SSL-enabled links should always be used except Windows stub installers.
        """
        # SSL-enabled links won't be used for Windows builds (but SSL download
        # is enabled by default for stub installers)
        url = firefox_desktop.get_download_url('release', '27.0', 'win', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-stub'),
                              ('os', 'win'),
                              ('lang', 'pt-BR')])

        # SSL-enabled links will be used for OS X builds
        url = firefox_desktop.get_download_url('release', '27.0', 'osx', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-latest-ssl'),
                              ('os', 'osx'),
                              ('lang', 'pt-BR')])

        # SSL-enabled links will be used for Linux builds
        url = firefox_desktop.get_download_url('release', '27.0', 'linux', 'pt-BR', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-latest-ssl'),
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

    @patch.dict(os.environ, FUNNELCAKE_64_LOCALES='en-US', FUNNELCAKE_64_PLATFORMS='win')
    def test_funnelcake_direct_links_en_us_win_only(self):
        """
        Ensure funnelcake params are included for Windows en-US builds only.
        """
        url = firefox_desktop.get_download_url('release', '45.0', 'win', 'en-US', force_direct=True, funnelcake_id='64')
        ok_('product=firefox-stub-f64' in url)

        url = firefox_desktop.get_download_url('release', '45.0', 'win64', 'en-US', force_direct=True, funnelcake_id='64')
        ok_('product=firefox-stub-f64' not in url)

        url = firefox_desktop.get_download_url('release', '45.0', 'win', 'de', force_direct=True, funnelcake_id='64')
        ok_('product=firefox-stub-f64' not in url)

        url = firefox_desktop.get_download_url('release', '45.0', 'osx', 'en-US', force_direct=True, funnelcake_id='64')
        ok_('product=firefox-stub-f64' not in url)

    def test_no_funnelcake_direct_links_if_not_configured(self):
        """
        Ensure funnelcake params are included for Linux and OSX en-US builds only.
        """
        url = firefox_desktop.get_download_url('release', '45.0', 'win', 'en-US', force_direct=True, funnelcake_id='64')
        ok_('-f64' not in url)

        url = firefox_desktop.get_download_url('release', '45.0', 'win', 'en-US', force_direct=True, force_full_installer=True, funnelcake_id='64')
        ok_('-f64' not in url)

        url = firefox_desktop.get_download_url('release', '45.0', 'win', 'en-US', force_direct=True, force_funnelcake=True, funnelcake_id='64')
        ok_('-f64' not in url)

        url = firefox_desktop.get_download_url('release', '45.0', 'osx', 'de', force_direct=True, funnelcake_id='64')
        ok_('-f64' not in url)

        url = firefox_desktop.get_download_url('release', '45.0', 'osx', 'en-US', force_direct=True, funnelcake_id='64')
        ok_('-f64' not in url)

        url = firefox_desktop.get_download_url('release', '45.0', 'osx', 'fr', force_direct=True, funnelcake_id='64')
        ok_('-f64' not in url)

        url = firefox_desktop.get_download_url('release', '45.0', 'linux', 'de', force_direct=True, funnelcake_id='64')
        ok_('-f64' not in url)

        url = firefox_desktop.get_download_url('release', '45.0', 'linux', 'en-US', force_direct=True, funnelcake_id='64')
        ok_('-f64' not in url)

        url = firefox_desktop.get_download_url('release', '45.0', 'linux', 'fr', force_direct=True, funnelcake_id='64')
        ok_('-f64' not in url)

    def test_stub_installer_win_only(self):
        """
        Ensure that builds not in the setting don't get stub.
        """
        url = firefox_desktop.get_download_url('release', '19.0', 'osx', 'en-US')
        ok_('product=firefox-stub&' not in url)

        url = firefox_desktop.get_download_url('beta', '20.0b4', 'win', 'fr')
        ok_('product=firefox-beta-stub&' in url)

        url = firefox_desktop.get_download_url('beta', '20.0b4', 'win64', 'fr')
        ok_('product=firefox-beta-stub&' in url)

        url = firefox_desktop.get_download_url('beta', '20.0b4', 'linux', 'fr')
        ok_('product=firefox-beta-stub&' not in url)


class TestFirefoxAndroid(TestCase):
    archive_url_base = 'https://archive.mozilla.org/pub/mobile/nightly/'
    google_play_url_base = ('https://play.google.com/store/apps/details'
                            '?id=org.mozilla.')

    @patch.object(firefox_android._storage, 'data',
                  Mock(return_value=dict(version='22.0.1')))
    def test_latest_release_version(self):
        """latest_version should return the latest release version."""
        eq_(firefox_android.latest_version('release'), '22.0.1')

    @patch.object(firefox_android._storage, 'data',
                  Mock(return_value=dict(beta_version='23.0')))
    def test_latest_beta_version(self):
        """latest_version should return the latest beta version."""
        eq_(firefox_android.latest_version('beta'), '23.0')

    def test_get_download_url_nightly(self):
        """
        get_download_url should return the same Google Play link of the
        'org.mozilla.fennec_aurora' product regardless of the architecture type,
        if the force_direct option is unspecified.
        """
        ok_(firefox_android.get_download_url('nightly', 'arm')
            .startswith(self.google_play_url_base + 'fennec_aurora'))
        ok_(firefox_android.get_download_url('nightly', 'x86')
            .startswith(self.google_play_url_base + 'fennec_aurora'))

    @patch.object(firefox_android._storage, 'data',
                  Mock(return_value=dict(nightly_version='55.0a1')))
    def test_get_download_url_nightly_direct_legacy(self):
        """
        get_download_url should return a mozilla-central archive link depending
        on the architecture type, if the force_direct option is True. The ARM
        build URL should have api-15 instead of api-16.
        """
        eq_(firefox_android.get_download_url('nightly', 'arm', 'multi', True),
            self.archive_url_base + 'latest-mozilla-central-android-api-15/'
            'fennec-55.0a1.multi.android-arm.apk')
        eq_(firefox_android.get_download_url('nightly', 'x86', 'multi', True),
            self.archive_url_base + 'latest-mozilla-central-android-x86/'
            'fennec-55.0a1.multi.android-i386.apk')

    @patch.object(firefox_android._storage, 'data',
                  Mock(return_value=dict(nightly_version='56.0a1')))
    def test_get_download_url_nightly_direct(self):
        """
        get_download_url should return a mozilla-central archive link depending
        on the architecture type, if the force_direct option is True.
        """
        eq_(firefox_android.get_download_url('nightly', 'arm', 'multi', True),
            self.archive_url_base + 'latest-mozilla-central-android-api-16/'
            'fennec-56.0a1.multi.android-arm.apk')
        eq_(firefox_android.get_download_url('nightly', 'x86', 'multi', True),
            self.archive_url_base + 'latest-mozilla-central-android-x86/'
            'fennec-56.0a1.multi.android-i386.apk')

    def test_get_download_url_beta(self):
        """
        get_download_url should return the same Google Play link of the
        'org.mozilla.firefox_beta' product regardless of the architecture type,
        if the force_direct option is unspecified.
        """
        ok_(firefox_android.get_download_url('beta', 'arm')
            .startswith(self.google_play_url_base + 'firefox_beta'))
        ok_(firefox_android.get_download_url('beta', 'x86')
            .startswith(self.google_play_url_base + 'firefox_beta'))

    def test_get_download_url_beta_direct(self):
        """
        get_download_url should return a bouncer link depending on the
        architecture type, if the force_direct option is True.
        """
        url = firefox_android.get_download_url('beta', 'arm', 'multi', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'fennec-beta-latest'),
                              ('os', 'android'), ('lang', 'multi')])
        url = firefox_android.get_download_url('beta', 'x86', 'multi', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'fennec-beta-latest'),
                              ('os', 'android-x86'), ('lang', 'multi')])

    def test_get_download_url_release(self):
        """
        get_download_url should return the same Google Play link of the
        'org.mozilla.firefox' product regardless of the architecture type,
        if the force_direct option is unspecified.
        """
        ok_(firefox_android.get_download_url('release', 'arm')
            .startswith(self.google_play_url_base + 'firefox'))
        ok_(firefox_android.get_download_url('release', 'x86')
            .startswith(self.google_play_url_base + 'firefox'))

    def test_get_download_url_release_direct(self):
        """
        get_download_url should return a bouncer link depending on the
        architecture type, if the force_direct option is True.
        """
        url = firefox_android.get_download_url('release', 'arm', 'multi', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'fennec-latest'),
                              ('os', 'android'), ('lang', 'multi')])
        url = firefox_android.get_download_url('release', 'x86', 'multi', True)
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'fennec-latest'),
                              ('os', 'android-x86'), ('lang', 'multi')])


@patch.object(firefox_ios._storage, 'data',
              Mock(return_value=dict(ios_version='5.0', ios_beta_version='6.0')))
class TestFirefoxIos(TestCase):

    def test_latest_release_version(self):
        """latest_version should return the latest release version."""
        eq_(firefox_ios.latest_version('release'), '5.0')

    def test_latest_beta_version(self):
        """latest_version should return the latest beta version."""
        eq_(firefox_ios.latest_version('beta'), '6.0')
