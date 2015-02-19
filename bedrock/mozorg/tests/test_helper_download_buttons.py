# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.test.client import RequestFactory
from django.test.utils import override_settings

import jingo
from nose.tools import eq_, ok_
from product_details import product_details
from pyquery import PyQuery as pq

from bedrock.mozorg.tests import TestCase


def render(s, context=None):
    context = context or {}
    t = jingo.env.from_string(s)
    return t.render(context)


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
    def test_stub_aurora_installer_enabled_locales(self):
        """Check that the stub is not served to locales"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('alpha') }}",
                        {'request': get_request}))

        links = doc('.download-list a')
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @override_settings(AURORA_STUB_INSTALLER=False)
    def test_stub_aurora_installer_disabled_locale(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('alpha') }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:4]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @override_settings(AURORA_STUB_INSTALLER=True)
    def test_stub_aurora_installer_override_locale(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('alpha', "
                        "force_full_installer=True) }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:4]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    def test_aurora_mobile(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox('alpha', platform='android') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 3)
        eq_(pq(list[0]).attr('class'), 'os_android armv7 api-9')
        eq_(pq(list[1]).attr('class'), 'os_android armv7 api-11')
        eq_(pq(list[2]).attr('class'), 'os_android x86')

        list = doc('.download-other .arch')
        eq_(list.length, 3)
        eq_(pq(list[0]).attr('class'), 'arch armv7 api-9')
        eq_(pq(list[1]).attr('class'), 'arch armv7 api-11')
        eq_(pq(list[2]).attr('class'), 'arch x86')

    def test_beta_mobile(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox('beta', platform='android') }}",
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
        doc = pq(render("{{ download_firefox(platform='android') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'os_android')

        list = doc('.download-other .arch')
        eq_(list.length, 0)

    def test_check_old_firefox(self):
        """
        Make sure check_old_fx class is only applied if both check_old_fx=True
        and simple=True.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'

        # missing required 'simple=True' param
        doc = pq(render("{{ download_firefox(check_old_fx=True) }}",
                        {'request': get_request}))

        dlbuttons = doc('.download-button')
        eq_(dlbuttons.length, 1)

        # 'download-button-check-old-fx' class should not be present
        dlbtn = pq(dlbuttons[0])
        self.assertFalse(dlbtn('.download-button-check-old-fx'))

        # contains required 'simple=True' param
        doc = pq(render("{{ download_firefox(simple=True, check_old_fx=True) }}",
                        {'request': get_request}))

        dlbuttons = doc('.download-button')
        eq_(dlbuttons.length, 1)

        # 'download-button-check-old-fx' class should be present
        dlbtn = pq(dlbuttons[0])
        self.assertTrue(dlbtn('.download-button-check-old-fx'))
