# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.test.client import RequestFactory
from django.test.utils import override_settings

import jingo
from mock import patch
from nose.tools import eq_, ok_
from product_details import product_details
from pyquery import PyQuery as pq

from bedrock.mozorg.helpers.download_buttons import (
    firefox_details,
    latest_version,
    make_download_link
)
from bedrock.mozorg.tests import TestCase


_ALL = settings.STUB_INSTALLER_ALL


def render(s, context=None):
    context = context or {}
    t = jingo.env.from_string(s)
    return t.render(context)


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

AURORA_DIR = ('https://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/'
              'latest-mozilla-aurora')

mkln = make_download_link


@patch.object(firefox_details, 'firefox_primary_builds', GOOD_BUILDS)
@patch.object(firefox_details, 'firefox_beta_builds', {})
@patch.dict(firefox_details.firefox_versions, GOOD_VERSIONS)
class TestLatestVersion(TestCase):
    def test_latest_version(self):
        """Should return platforms if localized build does exist."""
        result = latest_version('de', 'release')
        self.assertEqual(result[0], '25.0')
        self.assertIs(result[1], GOOD_PLATS)

    def test_latest_version_is_none_if_no_build(self):
        """Should return None if the localized build for the channel doesn't exist."""
        result = latest_version('fr', 'release')
        self.assertIsNone(result)

    def test_latest_version_channels(self):
        """Should work with all channels."""
        result = latest_version('en-US', 'beta')
        self.assertEqual(result[0], '26.0b2')
        self.assertIs(result[1], GOOD_PLATS)

        result = latest_version('en-US', 'aurora')
        self.assertEqual(result[0], '27.0a1')
        self.assertIs(result[1], GOOD_PLATS)


class TestDownloadButtons(TestCase):

    def latest_version(self):
        return product_details.firefox_versions['LATEST_FIREFOX_VERSION']

    def check_desktop_links(self, links):
        """Desktop links should have the correct firefox version"""
        # valid product strings
        keys = [
            'firefox-%s' % self.latest_version(),
            'firefox-stub',
            'firefox-latest',
            'firefox-beta-stub',
            'firefox-beta-latest',
        ]

        for link in links:
            url = pq(link).attr('href')
            ok_(any(key in url for key in keys))

    def check_dumb_button(self, doc):
        # Make sure 5 links are present
        links = doc('li a')
        eq_(links.length, 5)

        self.check_desktop_links(links[:4])

        # Check that last link is Android
        eq_(pq(links[4]).attr('href'), settings.GOOGLE_PLAY_FIREFOX_LINK)

    def test_button_force_direct(self):
        """
        If the force_direct parameter is True, all download links must be
        directly to https://download.mozilla.org.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(force_direct=true) }}",
                        {'request': get_request}))

        # Check that the first 4 links are direct.
        links = doc('.download-list a')
        for link in links[:4]:
            link = pq(link)
            ok_(link.attr('href')
                .startswith('https://download.mozilla.org'))
            # direct links should not have the data attr.
            ok_(link.attr('data-direct-link') is None)

    def test_button_has_data_attr_if_not_direct(self):
        """
        If the button points to the thank you page, it should have a
        `data-direct-link` attribute that contains the direct url.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox() }}",
                        {'request': get_request}))

        # The first 4 links should be for desktop.
        links = doc('.download-list a')
        for link in links[:4]:
            ok_(pq(link).attr('data-direct-link')
                .startswith('https://download.mozilla.org'))
        # The fourth link is mobile and should not have the attr
        ok_(pq(links[4]).attr('data-direct-link') is None)

    @override_settings(AURORA_STUB_INSTALLER=True)
    def test_stub_aurora_installer_enabled_en_us(self):
        """Check that only the windows link goes to stub with en-US"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox('aurora') }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:4]
        ok_('stub' in pq(links[0]).attr('href'))
        for link in links[1:]:
            ok_('stub' not in pq(link).attr('href'))

    @override_settings(AURORA_STUB_INSTALLER=True)
    def test_stub_aurora_installer_enabled_locales(self):
        """Check that the stub is not served to locales"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('aurora') }}",
                        {'request': get_request}))

        links = doc('.download-list a')
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @override_settings(AURORA_STUB_INSTALLER=False)
    def test_stub_aurora_installer_disabled_en_us(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox('aurora') }}",
                        {'request': get_request}))

        links = doc('li a')[:4]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @override_settings(AURORA_STUB_INSTALLER=False)
    def test_stub_aurora_installer_disabled_locale(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('aurora') }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:4]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @override_settings(AURORA_STUB_INSTALLER=True)
    def test_stub_aurora_installer_override_en_us(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox('aurora', "
                        "force_full_installer=True) }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:4]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @override_settings(AURORA_STUB_INSTALLER=True)
    def test_stub_aurora_installer_override_locale(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('aurora', "
                        "force_full_installer=True) }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:4]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    def test_aurora_mobile(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox('aurora', mobile=True) }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 2)
        eq_(pq(list[0]).attr('class'), 'os_android armv7')
        eq_(pq(list[1]).attr('class'), 'os_android x86')

        list = doc('.download-other .arch')
        eq_(list.length, 2)
        eq_(pq(list[0]).attr('class'), 'arch armv7')
        eq_(pq(list[1]).attr('class'), 'arch x86')

    def test_beta_mobile(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox('beta', mobile=True) }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'os_android')

        list = doc('.download-other .arch')
        eq_(list.length, 0)

    def test_firefox_mobile(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox(mobile=True) }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'os_android')

        list = doc('.download-other .arch')
        eq_(list.length, 0)

    @override_settings(STUB_INSTALLER_LOCALES={'win': ['en-us']})
    def test_force_funnelcake_en_us_win_only(self):
        """
        Ensure that force_funnelcake doesn't affect non configured locale urls
        """
        url = make_download_link('firefox', 'release', '19.0', 'os_osx',
                                 'en-US', force_funnelcake=True)
        ok_('product=firefox-latest&' not in url)

        url = make_download_link('firefox', 'beta', '20.0b4', 'os_windows',
                                 'fr', force_funnelcake=True)
        ok_('product=firefox-beta-latest&' not in url)

    @override_settings(STUB_INSTALLER_LOCALES={'win': ['en-us']})
    def test_force_full_installer_en_us_win_only(self):
        """
        Ensure that force_full_installer doesn't affect non configured locales
        """
        url = make_download_link('firefox', 'release', '19.0', 'os_osx',
                                 'en-US', force_full_installer=True)
        ok_('product=firefox-latest&' not in url)

        url = make_download_link('firefox', 'beta', '20.0b4', 'os_windows',
                                 'fr', force_full_installer=True)
        ok_('product=firefox-beta-latest&' not in url)

    @override_settings(STUB_INSTALLER_LOCALES={'win': ['en-us']})
    def test_stub_installer_en_us_win_only(self):
        """
        Ensure that builds not in the setting don't get stub.
        """
        url = make_download_link('firefox', 'release', '19.0', 'os_osx',
                                 'en-US')
        ok_('product=firefox-stub&' not in url)

        url = make_download_link('firefox', 'beta', '20.0b4', 'os_windows',
                                 'fr')
        ok_('product=firefox-beta-stub&' not in url)
