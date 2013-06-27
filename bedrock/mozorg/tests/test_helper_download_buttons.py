# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.test.utils import override_settings
from django.utils import unittest
from test_utils import RequestFactory

import jingo
from nose.tools import eq_, ok_
from product_details import product_details
from pyquery import PyQuery as pq

from bedrock.mozorg.helpers.download_buttons import make_download_link


def render(s, context={}):
    t = jingo.env.from_string(s)
    return t.render(context)


class TestDownloadButtons(unittest.TestCase):

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
        # Make sure 4 links are present
        links = doc('li a')
        eq_(links.length, 4)

        self.check_desktop_links(links[:3])

        # Check that last link is Android
        eq_(pq(links[3]).attr('href'),
            'https://play.google.com/store/apps/details?id=org.mozilla.firefox')

    def test_button(self, small=False):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(small=%s, "
                        "dom_id='button') }}" % small,
                        {'request': get_request}))

        eq_(doc.attr('id'), 'button')

        self.check_dumb_button(doc('noscript'))
        self.check_dumb_button(doc('.unrecognized-download'))
        self.check_dumb_button(doc('.download-list'))

        eq_(doc('.download-other a').length, 6)

    def test_small_button(self):
        self.test_button(True)

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

        # Check that the first 3 links are direct.
        links = doc('.download-list a')
        for link in links[:3]:
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

        # The first 3 links should be for desktop.
        links = doc('.download-list a')
        for link in links[:3]:
            ok_(pq(link).attr('data-direct-link')
                .startswith('https://download.mozilla.org'))
        # The fourth link is mobile and should not have the attr
        ok_(pq(links[3]).attr('data-direct-link') is None)

    @override_settings(AURORA_STUB_INSTALLER=True)
    def test_stub_aurora_installer_enabled_en_us(self):
        """Check that only the windows link goes to stub with en-US"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox('aurora') }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:3]
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

        links = doc('li a')[:3]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @override_settings(AURORA_STUB_INSTALLER=False)
    def test_stub_aurora_installer_disabled_locale(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('aurora') }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:3]
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

        links = doc('.download-list a')[:3]
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

        links = doc('.download-list a')[:3]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    def test_download_transition_link_contains_locale(self):
        """
        "transition" download links should include the locale in the path as
        well as the query string.
        """
        locale = settings.LOCALES_WITH_TRANSITION[0]
        url = make_download_link('firefox', 'release', 19.0, 'os_osx', locale)
        good_url = ('/{locale}/products/download.html?product=firefox-19.0&'
                    'os=osx&lang={locale}').format(locale=locale)
        eq_(url, good_url)

    @override_settings(STUB_INSTALLER_LOCALES={'win': ['en-us']})
    def test_force_funnelcake(self):
        """
        force_funnelcake should force the product to be 'firefox-latest'
        for en-US windows release downloads, and 'firefox-beta-latest' for
        beta.
        """
        url = make_download_link('firefox', 'release', 19.0, 'os_windows',
                                 'en-US', force_funnelcake=True)
        ok_('product=firefox-latest&' in url)

        url = make_download_link('firefox', 'beta', '20.0b4', 'os_windows',
                                 'en-US', force_funnelcake=True)
        ok_('product=firefox-beta-latest&' in url)

    @override_settings(STUB_INSTALLER_LOCALES={'win': ['en-us']})
    def test_force_funnelcake_en_us_win_only(self):
        """
        Ensure that force_funnelcake doesn't affect non configured locale urls
        """
        url = make_download_link('firefox', 'release', 19.0, 'os_osx',
                                 'en-US', force_funnelcake=True)
        ok_('product=firefox-latest&' not in url)

        url = make_download_link('firefox', 'beta', '20.0b4', 'os_windows',
                                 'fr', force_funnelcake=True)
        ok_('product=firefox-beta-latest&' not in url)

    @override_settings(STUB_INSTALLER_LOCALES={'win': ['en-us']})
    def test_force_full_installer(self):
        """
        force_full_installer should force the product to be 'firefox-latest'
        for configured locale release downloads, and 'firefox-beta-latest' for
        beta.
        """
        url = make_download_link('firefox', 'release', 19.0, 'os_windows',
                                 'en-US', force_full_installer=True)
        ok_('product=firefox-latest&' in url)

        url = make_download_link('firefox', 'beta', '20.0b4', 'os_windows',
                                 'en-US', force_full_installer=True)
        ok_('product=firefox-beta-latest&' in url)

    @override_settings(STUB_INSTALLER_LOCALES={'win': ['en-us']})
    def test_force_full_installer_en_us_win_only(self):
        """
        Ensure that force_full_installer doesn't affect non configured locales
        """
        url = make_download_link('firefox', 'release', 19.0, 'os_osx',
                                 'en-US', force_full_installer=True)
        ok_('product=firefox-latest&' not in url)

        url = make_download_link('firefox', 'beta', '20.0b4', 'os_windows',
                                 'fr', force_full_installer=True)
        ok_('product=firefox-beta-latest&' not in url)

    @override_settings(STUB_INSTALLER_LOCALES={
        'win': ['en-us'], 'osx': ['fr', 'de'], 'linux': []})
    def test_stub_installer(self):
        """Button should give stub for builds in the setting always."""
        url = make_download_link('firefox', 'release', 19.0, 'os_windows',
                                 'en-US')
        ok_('product=firefox-stub&' in url)

        url = make_download_link('firefox', 'release', 19.0, 'os_osx',
                                 'fr')
        ok_('product=firefox-stub&' in url)

        url = make_download_link('firefox', 'release', 19.0, 'os_osx',
                                 'de')
        ok_('product=firefox-stub&' in url)

        url = make_download_link('firefox', 'beta', '20.0b4', 'os_windows',
                                 'en-US')
        ok_('product=firefox-beta-stub&' in url)

    @override_settings(STUB_INSTALLER_LOCALES={
        'win': settings.STUB_INSTALLER_ALL})
    def test_stub_installer_all(self):
        """Button should give stub for all langs when ALL is set."""
        url = make_download_link('firefox', 'release', 19.0, 'os_windows',
                                 'en-US')
        ok_('product=firefox-stub&' in url)

        url = make_download_link('firefox', 'release', 19.0, 'os_windows',
                                 'fr')
        ok_('product=firefox-stub&' in url)

        url = make_download_link('firefox', 'release', 19.0, 'os_windows',
                                 'de')
        ok_('product=firefox-stub&' in url)

        url = make_download_link('firefox', 'beta', '20.0b4', 'os_windows',
                                 'es-ES')
        ok_('product=firefox-beta-stub&' in url)

    @override_settings(STUB_INSTALLER_LOCALES={'win': ['en-us']})
    def test_stub_installer_en_us_win_only(self):
        """
        Ensure that builds not in the setting don't get stub.
        """
        url = make_download_link('firefox', 'release', 19.0, 'os_osx',
                                 'en-US')
        ok_('product=firefox-stub&' not in url)

        url = make_download_link('firefox', 'beta', '20.0b4', 'os_windows',
                                 'fr')
        ok_('product=firefox-beta-stub&' not in url)
