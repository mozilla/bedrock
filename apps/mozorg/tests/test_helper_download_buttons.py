# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest

from django.conf import settings
from test_utils import RequestFactory

import jingo
from mock import patch
from nose.tools import assert_not_equal, eq_, ok_
from product_details import product_details
from pyquery import PyQuery as pq


# Where should this function go?
def render(s, context={}):
    t = jingo.env.from_string(s)
    return t.render(**context)


class TestDownloadButtons(unittest.TestCase):

    def latest_version(self):
        return product_details.firefox_versions['LATEST_FIREFOX_VERSION']

    def check_desktop_links(self, links):
        """Desktop links should have the correct firefox version"""
        key = 'firefox-%s' % self.latest_version()

        for link in links:
            assert_not_equal(pq(link).attr('href').find(key), -1)

    def check_dumb_button(self, doc):
        # Make sure 4 links are present
        links = doc('li a')
        eq_(links.length, 4)

        self.check_desktop_links(links[:3])

        # Check that last link is Android
        eq_(pq(links[3]).attr('href'),
            'https://market.android.com/details?id=org.mozilla.firefox')

    def test_button(self, format='large'):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_button('button', '%s') }}" % format,
                        {'request': get_request}))

        eq_(doc.attr('id'), 'button')

        self.check_dumb_button(doc('noscript'))
        self.check_dumb_button(doc('.unrecognized-download'))
        self.check_dumb_button(doc('.download-list'))

        eq_(doc('.download-other a').length, 3)

    def test_small_button(self):
        self.test_button('small')

    def test_button_force_direct(self):
        """
        If the force_direct parameter is True, all download links must be
        directly to https://download.mozilla.org.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_button('button', force_direct=true) }}",
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
        doc = pq(render("{{ download_button('button') }}",
                        {'request': get_request}))

        # The first 3 links should be for desktop.
        links = doc('.download-list a')
        for link in links[:3]:
            ok_(pq(link).attr('data-direct-link')
                .startswith('https://download.mozilla.org'))
        # The fourth link is mobile and should not have the attr
        ok_(pq(links[3]).attr('data-direct-link') is None)

    @patch.object(settings, 'AURORA_STUB_INSTALLER', True)
    def test_stub_aurora_installer_enabled_en_us(self):
        """Check that only the windows link goes to stub with en-US"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_button('button', build='aurora') }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:3]
        ok_('stub' in pq(links[0]).attr('href'))
        for link in links[1:]:
            ok_('stub' not in pq(link).attr('href'))

    @patch.object(settings, 'AURORA_STUB_INSTALLER', True)
    def test_stub_aurora_installer_enabled_locales(self):
        """Check that the stub is not served to locales"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_button('button', build='aurora') }}",
                        {'request': get_request}))

        links = doc('.download-list a')
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @patch.object(settings, 'AURORA_STUB_INSTALLER', False)
    def test_stub_aurora_installer_disabled_en_us(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_button('button', build='aurora') }}",
                        {'request': get_request}))

        links = doc('li a')[:3]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @patch.object(settings, 'AURORA_STUB_INSTALLER', False)
    def test_stub_aurora_installer_disabled_locale(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_button('button', build='aurora') }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:3]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @patch.object(settings, 'AURORA_STUB_INSTALLER', True)
    def test_stub_aurora_installer_override_en_us(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_button('button', build='aurora', \
                            force_full_installer=True) }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:3]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @patch.object(settings, 'AURORA_STUB_INSTALLER', True)
    def test_stub_aurora_installer_override_locale(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_button('button', build='aurora', \
                            force_full_installer=True) }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:3]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))
