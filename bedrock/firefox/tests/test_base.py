# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.test.client import Client, RequestFactory
from django.test.utils import override_settings
from funfactory.helpers import static

from funfactory.urlresolvers import reverse
from mock import ANY, call, Mock, patch
from nose.tools import eq_, ok_
from pyquery import PyQuery as pq

from bedrock.firefox import views as fx_views
from bedrock.firefox.firefox_details import FirefoxDesktop, FirefoxAndroid
from bedrock.firefox.utils import product_details
from bedrock.mozorg.tests import TestCase


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
PROD_DETAILS_DIR = os.path.join(TEST_DATA_DIR, 'product_details_json')
GOOD_PLATS = {'Windows': {}, 'OS X': {}, 'Linux': {}}

with patch.object(settings, 'PROD_DETAILS_DIR', PROD_DETAILS_DIR):
    firefox_desktop = FirefoxDesktop()
    firefox_android = FirefoxAndroid()


class TestInstallerHelp(TestCase):
    def setUp(self):
        self.button_mock = Mock()
        self.patcher = patch.dict('jingo.env.globals',
                                  download_firefox=self.button_mock)
        self.patcher.start()
        self.view_name = 'firefox.installer-help'
        with self.activate('en-US'):
            self.url = reverse(self.view_name)

    def tearDown(self):
        self.patcher.stop()

    def test_buttons_use_lang(self):
        """
        The buttons should use the lang from the query parameter.
        """
        self.client.get(self.url, {
            'installer_lang': 'fr'
        })
        self.button_mock.assert_has_calls([
            call(force_direct=True, force_full_installer=True, locale='fr'),
            call('beta', small=ANY, force_direct=True,
                 force_full_installer=True, icon=ANY, locale='fr'),
            call('alpha', small=ANY, force_direct=True,
                 force_full_installer=True, icon=ANY, locale='fr'),
        ])

    def test_buttons_ignore_non_lang(self):
        """
        The buttons should ignore an invalid lang.
        """
        self.client.get(self.url, {
            'installer_lang': 'not-a-locale'
        })
        self.button_mock.assert_has_calls([
            call(force_direct=True, force_full_installer=True, locale=None),
            call('beta', small=ANY, force_direct=True,
                 force_full_installer=True, icon=ANY, locale=None),
            call('alpha', small=ANY, force_direct=True,
                 force_full_installer=True, icon=ANY, locale=None),
        ])

    def test_invalid_channel_specified(self):
        """
        All buttons should show when channel is invalid.
        """
        self.client.get(self.url, {
            'channel': 'dude',
        })
        self.button_mock.assert_has_calls([
            call(force_direct=True, force_full_installer=True, locale=None),
            call('beta', small=ANY, force_direct=True,
                 force_full_installer=True, icon=ANY, locale=None),
            call('alpha', small=ANY, force_direct=True,
                 force_full_installer=True, icon=ANY, locale=None),
        ])

    def test_one_button_when_channel_specified(self):
        """
        There should be only one button when the channel is given.
        """
        self.client.get(self.url, {
            'channel': 'beta',
        })
        self.button_mock.assert_called_once_with('beta', force_direct=True,
                                                 force_full_installer=True,
                                                 locale=None)


@patch.object(fx_views, 'firefox_desktop', firefox_desktop)
class TestFirefoxAll(TestCase):
    def setUp(self):
        with self.activate('en-US'):
            self.url = reverse('firefox.all')

    def test_no_search_results(self):
        """
        Tables should be gone and not-found message should be shown when there
        are no search results.
        """
        resp = self.client.get(self.url + '?q=DOES_NOT_EXIST')
        doc = pq(resp.content)
        ok_(not doc('table.build-table'))
        ok_(not doc('.not-found.hide'))

    def test_no_search_query(self):
        """
        When not searching all builds should show.
        """
        resp = self.client.get(self.url)
        doc = pq(resp.content)
        eq_(len(doc('.build-table')), 2)
        eq_(len(doc('.not-found.hide')), 2)

        num_builds = len(firefox_desktop.get_filtered_full_builds('release'))
        num_builds += len(firefox_desktop.get_filtered_test_builds('release'))
        eq_(len(doc('tr[data-search]')), num_builds)

    def test_no_locale_details(self):
        """
        When a localized build has been added to the Firefox details while the
        locale details are not updated yet, the filtered build list should not
        include the localized build.
        """
        builds = firefox_desktop.get_filtered_full_builds('release')
        ok_('uz' in firefox_desktop.firefox_primary_builds)
        ok_('uz' not in firefox_desktop.languages)
        eq_(len([build for build in builds if build['locale'] == 'uz']), 0)


class TestFirefoxPartners(TestCase):
    @patch('bedrock.firefox.views.settings.DEBUG', True)
    def test_js_bundle_files_debug_true(self):
        """
        When DEBUG is on the bundle should return the individual files
        with the STATIC_URL.
        """
        bundle = 'partners_desktop'
        files = settings.PIPELINE_JS[bundle]['source_filenames']
        files = [static(f) for f in files]
        self.assertEqual(files,
                         json.loads(fx_views.get_js_bundle_files(bundle)))

    @patch('bedrock.firefox.views.settings.DEBUG', False)
    def test_js_bundle_files_debug_false(self):
        """
        When DEBUG is off the bundle should return a single minified filename.
        """
        bundle = 'partners_desktop'
        filename = static('js/%s-bundle.js' % bundle)
        bundle_file = json.loads(fx_views.get_js_bundle_files(bundle))
        self.assertEqual(len(bundle_file), 1)
        self.assertEqual(bundle_file[0], filename)

    @patch('bedrock.mozorg.views.requests.post')
    def test_sf_form_proxy_error_response(self, post_patch):
        """An error response from SF should be returned."""
        new_mock = Mock()
        new_mock.status_code = 400
        post_patch.return_value = new_mock
        with self.activate('en-US'):
            url = reverse('mozorg.partnerships')
            resp = self.client.post(url, {
                'first_name': 'The',
                'last_name': 'Dude',
                'company': 'Urban Achievers',
                'email': 'thedude@mozilla.com',
            }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 400)

        # decode JSON response
        resp_data = json.loads(resp.content)

        self.assertEqual(resp_data['msg'], 'bad_request')
        self.assertTrue(post_patch.called)

    @patch('bedrock.mozorg.views.requests.post')
    def test_sf_form_proxy_invalid_form(self, post_patch):
        """A form error should result in a 400 response."""
        with self.activate('en-US'):
            url = reverse('mozorg.partnerships')
            resp = self.client.post(url, {
                'first_name': 'Dude' * 20,
            }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 400)

        resp_data = json.loads(resp.content)

        self.assertEqual(resp_data['msg'], 'Form invalid')
        self.assertFalse(post_patch.called)

    @patch('bedrock.mozorg.views.requests.post')
    def test_sf_form_proxy(self, post_patch):
        new_mock = Mock()
        new_mock.status_code = 200
        post_patch.return_value = new_mock
        with self.activate('en-US'):
            url = reverse('mozorg.partnerships')
            resp = self.client.post(url, {
                'first_name': 'The',
                'last_name': 'Dude',
                'title': 'Abider of things',
                'company': 'Urban Achievers',
                'email': 'thedude@mozilla.com',
            }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)

        resp_data = json.loads(resp.content)

        self.assertEqual(resp_data['msg'], 'ok')
        post_patch.assert_called_once_with(ANY, {
            'first_name': u'The',
            'last_name': u'Dude',
            'description': u'',
            'retURL': 'http://www.mozilla.org/en-US/about/'
                      'partnerships?success=1',
            'title': u'Abider of things',
            'URL': u'',
            'company': u'Urban Achievers',
            'oid': '00DU0000000IrgO',
            'phone': u'',
            'street': u'',
            'zip': u'',
            'city': u'',
            'state': u'',
            'country': u'',
            'mobile': u'',
            '00NU0000002pDJr': [],  # interest (multi-select)
            '00NU00000053D4G': u'',  # interested_countries
            '00NU00000053D4L': u'',  # interested_languages
            '00NU00000053D4a': u'',  # campaign_type
            'industry': u'',
            'email': u'thedude@mozilla.com',
            'lead_source': 'www.mozilla.org/about/partnerships/',
        })

    def test_sf_form_csrf_status(self):
        """Test that CSRF checks return 200 with token and 403 without."""
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.get(reverse('firefox.partners.index'))
        post_url = reverse('mozorg.partnerships')
        response = csrf_client.post(post_url, {
            'first_name': "Partner",
            'csrfmiddlewaretoken': response.cookies['csrftoken'].value,
        })
        self.assertEqual(response.status_code, 200)
        response = csrf_client.post(post_url, {'first_name': "Partner"})
        self.assertEqual(response.status_code, 403)


none_mock = Mock()
none_mock.return_value = None


@patch.object(fx_views.WhatsnewView, 'redirect_to', none_mock)
@patch('bedrock.firefox.views.l10n_utils.render', return_value=HttpResponse())
class TestWhatsNew(TestCase):
    def setUp(self):
        self.view = fx_views.WhatsnewView.as_view()
        self.rf = RequestFactory(HTTP_USER_AGENT='Firefox')

    @override_settings(DEV=True)
    def test_can_post(self, render_mock):
        """Home page must accept post for newsletter signup."""
        req = self.rf.post('/en-US/firefox/whatsnew/')
        self.view(req)
        # would return 405 before calling render otherwise
        render_mock.assert_called_once_with(req, ['firefox/whatsnew.html'], ANY)

    @patch.object(fx_views.WhatsnewView, 'fxos_locales', ['de'])
    @override_settings(DEV=True)
    def test_fxos_locales(self, render_mock):
        """Should use a different template for fxos locales."""
        req = self.rf.get('/de/firefox/whatsnew/')
        req.locale = 'de'
        self.view(req)
        template = render_mock.call_args[0][1]
        ctx = render_mock.call_args[0][2]
        ok_('locales_with_video' not in ctx)
        eq_(template, ['firefox/whatsnew-fxos.html'])

    @override_settings(DEV=True)
    def test_fx_australis_29(self, render_mock):
        """Should use australis template for 29.0."""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='29.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_australis_29_0_1(self, render_mock):
        """Should use australis template for 29.0.1"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='29.0.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_30(self, render_mock):
        """Should use australis template for 30.0."""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='30.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_31(self, render_mock):
        """Should use australis template for 31.0."""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='31.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_33_0(self, render_mock):
        """Should use australis template for 33.0."""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='33.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_33_0_1(self, render_mock):
        """Should use australis template for 33.0.1"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='33.0.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_33_1(self, render_mock):
        """Should use privacy tour template for 33.1"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='33.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/privacy_tour/no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_34_0(self, render_mock):
        """Should use no tour template for 34.0"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='34.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_34_0_with_oldversion(self, render_mock):
        """Should use search tour template for 34.0 with old version"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=33.0')
        self.view(req, version='34.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/tour.html'])

    @override_settings(DEV=True)
    def test_fx_34_0_1(self, render_mock):
        """Should use search tour template for 34.0.1"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='34.0.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_34_1(self, render_mock):
        """Should use no tour template for 34.1"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='34.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_34_0_locale(self, render_mock):
        """Should use australis template for 34.0 non en-US locales"""
        req = self.rf.get('/de/firefox/whatsnew/')
        req.locale = 'de'
        self.view(req, version='34.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_35_0_locale(self, render_mock):
        """Should use australis template for 35.0 non en-US locales"""
        req = self.rf.get('/de/firefox/whatsnew/')
        req.locale = 'de'
        self.view(req, version='35.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-no-tour.html'])

    # 34.0.5 search tour tests

    @override_settings(DEV=True)
    def test_fx_34_0_5(self, render_mock):
        """Should use no tour template for 34.0.5"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='34.0.5')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_34_0_5_with_oldversion(self, render_mock):
        """Should use 34.0.5 search tour template for 34.0.5 with old version"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=33.0')
        self.view(req, version='34.0.5')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/tour-34.0.5.html'])

    @override_settings(DEV=True)
    def test_fx_34_0_6_with_oldversion(self, render_mock):
        """Should use 34.0.5 search tour template for 34.0.6 with old version"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=33.0')
        self.view(req, version='34.0.6')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/tour-34.0.5.html'])

    @override_settings(DEV=True)
    def test_fx_34_1_with_oldversion(self, render_mock):
        """Should use 34.0.5 search tour template for 34.1 with old version"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=33.0')
        self.view(req, version='34.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/tour-34.0.5.html'])

    @override_settings(DEV=True)
    def test_fx_34_0_5_with_wrong_oldversion(self, render_mock):
        """Should no tour template for 34.0.5 with old version 34.x"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=34.0')
        self.view(req, version='34.0.5')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_34_0_5_locale(self, render_mock):
        """Should use australis template for 34.0.5 non en-US locales"""
        req = self.rf.get('/de/firefox/whatsnew/?oldversion=33.0')
        req.locale = 'de'
        self.view(req, version='34.0.5')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_35_0(self, render_mock):
        """Should use no tour template for 35.0 with no old version"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='35.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_35_0_with_oldversion(self, render_mock):
        """Should use 34.0.5 search tour template for 35.0 with old version"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=34.0')
        self.view(req, version='35.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/tour-34.0.5.html'])

    @override_settings(DEV=True)
    def test_fx_35_locale(self, render_mock):
        """Should use australis template for 35 non en-US locales"""
        req = self.rf.get('/de/firefox/whatsnew/?oldversion=34.0')
        req.locale = 'de'
        self.view(req, version='35.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_35_0_with_wrong_oldversion(self, render_mock):
        """Should no tour template for 35.0 with old version that is greater"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=35.1')
        self.view(req, version='35.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/search_tour/no-tour.html'])

    # end 34.0.5 search tour tests

    # begin 36.0 hello tour tests

    @override_settings(DEV=True)
    def test_fx_36_0(self, render_mock):
        """Should use no tour template for 36.0 with no old version"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='36.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/fx36/whatsnew-no-tour.html'])

    @override_settings(DEV=True)
    def test_fx_36_0_with_oldversion(self, render_mock):
        """Should use hello whatsnew tour template for 36.0 with old version"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=35.0')
        self.view(req, version='36.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/fx36/whatsnew-tour.html'])

    @override_settings(DEV=True)
    def test_fx_36_0_with_wrong_oldversion(self, render_mock):
        """Should no tour template for 36.0 with old version that is greater"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=36.1')
        self.view(req, version='36.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/fx36/whatsnew-no-tour.html'])

    # end 36.0 hello tour tests

    @override_settings(DEV=True)
    def test_fx_37_0_whatsnew(self, render_mock):
        """Should show Android SMS template for 37.0"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=36.0')
        self.view(req, version='37.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew-fx37.html'])

    # ESR31 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_esr_31_4_0_with_oldversion(self, render_mock):
        """Should use australis tour template for 31.4.0 with old version"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=24.8.0')
        self.view(req, version='31.4.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-tour.html'])

    @override_settings(DEV=True)
    def test_fx_esr_31_4_0_with_wrong_oldversion(self, render_mock):
        """Should not show tour for 31.4.0 with wrong old version"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=30.0')
        self.view(req, version='31.4.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew-no-tour.html'])

    # end ESR31 whatsnew tests

    @override_settings(DEV=True)
    def test_rv_prefix(self, render_mock):
        """Prefixed oldversion shouldn't impact version sniffing."""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=rv:10.0')
        self.view(req, version='33.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/privacy_tour/tour.html'])

    @override_settings(DEV=False)
    def test_fx_australis_secure_redirect(self, render_mock):
        """Should redirect to https: for 29.0."""
        url = '/en-US/firefox/whatsnew/'
        req = self.rf.get(url)
        with patch.object(req, 'is_secure', return_value=False):
            resp = self.view(req, version='29.0')
        eq_(resp['location'], 'https://testserver' + url)

    @override_settings(DEV=True)
    def test_fx_australis_secure_redirect_not_dev(self, render_mock):
        """Should not redirect to https: in DEV mode."""
        url = '/en-US/firefox/whatsnew/'
        req = self.rf.get(url)
        with patch.object(req, 'is_secure', return_value=False):
            resp = self.view(req, version='29.0')
        eq_(resp.status_code, 200)

    @override_settings(DEV=True)
    def test_fx_australis_secure_redirect_secure(self, render_mock):
        """Should not redirect to https: when already secure."""
        url = '/en-US/firefox/whatsnew/'
        req = self.rf.get(url)
        with patch.object(req, 'is_secure', return_value=True):
            resp = self.view(req, version='29.0')
        eq_(resp.status_code, 200)


@patch.object(fx_views.TourView, 'redirect_to', none_mock)
@patch('bedrock.firefox.views.l10n_utils.render', return_value=HttpResponse())
class TestTourView(TestCase):
    def setUp(self):
        self.view = fx_views.TourView.as_view()
        self.rf = RequestFactory(HTTP_USER_AGENT='Firefox')

    @override_settings(DEV=True)
    def test_fx_tour_template(self, render_mock):
        """Should use firstrun tour template"""
        req = self.rf.get('/en-US/firefox/tour/')
        self.view(req, version='29.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/help-menu-tour.html'])

    @override_settings(DEV=True)
    def test_fx_dev_browser_35_0_a2(self, render_mock):
        """Should use dev browser firstrun template for 35.0a2"""
        req = self.rf.get('/en-US/firefox/tour/')
        self.view(req, version='35.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/dev-firstrun.html'])

    @override_settings(DEV=True)
    def test_fx_dev_browser_35_1_a2(self, render_mock):
        """Should use dev browser firstrun template for 35.1a2"""
        req = self.rf.get('/en-US/firefox/tour/')
        self.view(req, version='35.1a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/dev-firstrun.html'])

    @override_settings(DEV=True)
    def test_fx_dev_browser_36_0_a2(self, render_mock):
        """Should use dev browser firstrun template for 36.0a2"""
        req = self.rf.get('/en-US/firefox/tour/')
        self.view(req, version='36.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/dev-firstrun.html'])

    @override_settings(DEV=True)
    def test_fx_dev_browser_34_0_a2(self, render_mock):
        """Should use standard firstrun template for older aurora"""
        req = self.rf.get('/en-US/firefox/tour/')
        self.view(req, version='34.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/help-menu-tour.html'])

    @override_settings(DEV=True)
    def test_fx_search_tour_34_0(self, render_mock):
        """Should use search tour template for 34.0"""
        req = self.rf.get('/en-US/firefox/tour/')
        self.view(req, version='34.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/help-menu-34-tour.html'])

    @override_settings(DEV=True)
    def test_fx_search_tour_34_0_5(self, render_mock):
        """Should use search tour template for 34.0.5"""
        req = self.rf.get('/en-US/firefox/tour/')
        self.view(req, version='34.0.5')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/help-menu-34-tour.html'])

    @override_settings(DEV=True)
    def test_fx_search_tour_34_0_locales(self, render_mock):
        """Should use australis template for 34.0 non en-US locales"""
        req = self.rf.get('/en-US/firefox/tour/')
        req.locale = 'de'
        self.view(req, version='34.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/help-menu-tour.html'])

    @override_settings(DEV=True)
    def test_fx_firstrun_tour_36_0(self, render_mock):
        """Should use fx36 tour template for 36.0"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='36.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/fx36/help-menu-36-tour.html'])

    @override_settings(DEV=False)
    def test_fx_australis_secure_redirect(self, render_mock):
        """Should redirect to https"""
        url = '/en-US/firefox/tour/'
        req = self.rf.get(url)
        with patch.object(req, 'is_secure', return_value=False):
            resp = self.view(req, version='29.0')
        eq_(resp['location'], 'https://testserver' + url)

    @override_settings(DEV=True)
    def test_fx_australis_secure_redirect_not_dev(self, render_mock):
        """Should not redirect to https: in DEV mode."""
        url = '/en-US/firefox/tour/'
        req = self.rf.get(url)
        with patch.object(req, 'is_secure', return_value=False):
            resp = self.view(req, version='29.0')
        eq_(resp.status_code, 200)

    @override_settings(DEV=True)
    def test_fx_australis_secure_redirect_secure(self, render_mock):
        """Should not redirect to https: when already secure."""
        url = '/en-US/firefox/tour/'
        req = self.rf.get(url)
        with patch.object(req, 'is_secure', return_value=True):
            resp = self.view(req, version='29.0')
        eq_(resp.status_code, 200)


@patch.object(fx_views.FirstrunView, 'redirect_to', none_mock)
@patch('bedrock.firefox.views.l10n_utils.render', return_value=HttpResponse())
class TestFirstRun(TestCase):
    def setUp(self):
        self.view = fx_views.FirstrunView.as_view()
        self.rf = RequestFactory()

    @override_settings(DEV=True)
    def test_can_post(self, render_mock):
        """Home page must accept post for newsletter signup."""
        req = self.rf.post('/en-US/firefox/firstrun/')
        self.view(req)
        # would return 405 before calling render otherwise
        render_mock.assert_called_once_with(req,
            ['firefox/australis/firstrun-tour.html'], ANY)

    @override_settings(DEV=True)
    def test_fx_australis_29(self, render_mock):
        """Should use firstrun tour template"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='29.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/firstrun-tour.html'])

    @override_settings(DEV=True)
    def test_fx_dev_browser_35_0_a2(self, render_mock):
        """Should use dev browser firstrun template for 35.0a2"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='35.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/dev-firstrun.html'])

    @override_settings(DEV=True)
    def test_fx_dev_browser_35_1_a2(self, render_mock):
        """Should use dev browser firstrun template for 35.1a2"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='35.1a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/dev-firstrun.html'])

    @override_settings(DEV=True)
    def test_fx_dev_browser_36_0_a2(self, render_mock):
        """Should use dev browser firstrun template for 36.0a2"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='36.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/dev-firstrun.html'])

    @override_settings(DEV=True)
    def test_fx_dev_browser_34_0_a2(self, render_mock):
        """Should use standard firstrun template for older aurora"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='34.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/firstrun-tour.html'])

    @override_settings(DEV=True)
    def test_fx_search_tour_34_0(self, render_mock):
        """Should use search tour template for 34.0"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='34.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/firstrun-34-tour.html'])

    @override_settings(DEV=True)
    def test_fx_search_tour_34_0_5(self, render_mock):
        """Should use search tour template for 34.0.5"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='34.0.5')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/firstrun-34-tour.html'])

    @override_settings(DEV=True)
    def test_fx_search_tour_34_0_locales(self, render_mock):
        """Should use australis template for 34.0 non en-US locales"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        req.locale = 'de'
        self.view(req, version='34.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/firstrun-tour.html'])

    @override_settings(DEV=True)
    def test_fx_firstrun_tour_36_0(self, render_mock):
        """Should use fx36 tour template for 36.0"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='36.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/fx36/firstrun-tour.html'])

    @override_settings(DEV=False)
    def test_fx_australis_secure_redirect(self, render_mock):
        """Should redirect to https:"""
        url = '/en-US/firefox/firstrun/'
        req = self.rf.get(url)
        with patch.object(req, 'is_secure', return_value=False):
            resp = self.view(req, version='29.0')
        eq_(resp['location'], 'https://testserver' + url)

    @override_settings(DEV=True)
    def test_fx_australis_secure_redirect_not_dev(self, render_mock):
        """Should not redirect to https: in DEV mode."""
        url = '/en-US/firefox/firstrun/'
        req = self.rf.get(url)
        with patch.object(req, 'is_secure', return_value=False):
            resp = self.view(req, version='29.0')
        eq_(resp.status_code, 200)

    @override_settings(DEV=True)
    def test_fx_australis_secure_redirect_secure(self, render_mock):
        """Should not redirect to https: when already secure."""
        url = '/en-US/firefox/firstrun/'
        req = self.rf.get(url)
        with patch.object(req, 'is_secure', return_value=True):
            resp = self.view(req, version='29.0')
        eq_(resp.status_code, 200)

    # tests from growth firstrun test. should be removed after 2/24/2015.

    @override_settings(DEV=True)
    def test_fx_growth_tour_0_35_0_1(self, render_mock):
        """Should use firstrun 34 tour template for 35.0.1 with funnelcake 34"""
        req = self.rf.get('/en-US/firefox/firstrun/?f=34')
        self.view(req, version='35.0.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/firstrun-34-tour.html'])

    @override_settings(DEV=True)
    def test_fx_growth_tour_1_35_0_1(self, render_mock):
        """Should use growth tour template 1 for 35.0.1 with funnelcake 35"""
        req = self.rf.get('/en-US/firefox/firstrun/?f=35')
        self.view(req, version='35.0.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/growth-firstrun-test1.html'])

    @override_settings(DEV=True)
    def test_fx_growth_tour_2_35_0_1(self, render_mock):
        """Should use growth tour template 2 for 35.0.1 with funnelcake 36"""
        req = self.rf.get('/en-US/firefox/firstrun/?f=36')
        self.view(req, version='35.0.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/growth-firstrun-test2.html'])


@patch.object(fx_views, 'firefox_desktop', firefox_desktop)
class FxVersionRedirectsMixin(object):
    @override_settings(DEV=True)  # avoid https redirects
    def assert_ua_redirects_to(self, ua, url_name, status_code=301):
        response = self.client.get(self.url, HTTP_USER_AGENT=ua)
        eq_(response.status_code, status_code)
        eq_(response['Vary'], 'User-Agent')
        eq_(response['Location'],
            'http://testserver%s' % reverse(url_name))

        # An additional redirect test with a query string
        query = '?ref=getfirefox'
        response = self.client.get(self.url + query, HTTP_USER_AGENT=ua)
        eq_(response.status_code, status_code)
        eq_(response['Vary'], 'User-Agent')
        eq_(response['Location'],
            'http://testserver%s' % reverse(url_name) + query)

    def test_non_firefox(self):
        """
        Any non-Firefox user agents should be permanently redirected to
        /firefox/new/.
        """
        user_agent = 'random'
        self.assert_ua_redirects_to(user_agent, 'firefox.new')

    @override_settings(DEV=True)
    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='13.0.5')
    @patch('bedrock.firefox.firefox_details.firefox_desktop.latest_builds',
           return_value=('13.0.5', GOOD_PLATS))
    def test_current_minor_version_firefox(self, latest_mock):
        """
        Should show current even if behind by a patch version
        """
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) '
                      'Gecko/20100101 Firefox/13.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')

    @override_settings(DEV=True)
    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='25.0',
                FIREFOX_ESR='24.1')
    @patch('bedrock.firefox.firefox_details.firefox_desktop.latest_builds',
           return_value=('25.0', GOOD_PLATS))
    def test_esr_firefox(self, latest_mock):
        """
        Currently released ESR firefoxen should not redirect. At present
        that is 24.0.x.
        """
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:24.0) '
                      'Gecko/20100101 Firefox/24.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')

    @override_settings(DEV=True)
    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='16.0')
    @patch('bedrock.firefox.firefox_details.firefox_desktop.latest_builds',
           return_value=('16.0', GOOD_PLATS))
    def test_current_firefox(self, latest_mock):
        """
        Currently released firefoxen should not redirect.
        """
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:16.0) '
                      'Gecko/20100101 Firefox/16.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')

    @override_settings(DEV=True)
    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='16.0')
    @patch('bedrock.firefox.firefox_details.firefox_desktop.latest_builds',
           return_value=('16.0', GOOD_PLATS))
    def test_future_firefox(self, latest_mock):
        """
        Pre-release firefoxen should not redirect.
        """
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:18.0) '
                      'Gecko/20100101 Firefox/18.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')


class TestWhatsnewRedirect(FxVersionRedirectsMixin, TestCase):
    def setUp(self):
        self.user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:29.0) '
                      'Gecko/20100101 Firefox/29.0')

        self.expected = 'data-has-tour="True"'
        self.url = reverse('firefox.whatsnew', args=['33.1'])

    @override_settings(DEV=True)
    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='16.0')
    @patch('bedrock.mozorg.helpers.misc.find_static', return_value=True)
    def test_whatsnew_tour_oldversion(self, find_static):
        """Should not show tour if upgrading from 33.1 onwards."""
        # sanity check that it should show for other values of "oldversion"
        response = self.client.get(self.url + '?oldversion=28.0', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=27.0.1', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=4.0', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=rv:10.0', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=33.0', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=33.0.1', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=33.1', HTTP_USER_AGENT=self.user_agent)
        self.assertNotIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=33.1.1', HTTP_USER_AGENT=self.user_agent)
        self.assertNotIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=34.0', HTTP_USER_AGENT=self.user_agent)
        self.assertNotIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=35.0', HTTP_USER_AGENT=self.user_agent)
        self.assertNotIn(self.expected, response.content)

        # if there's no oldversion parameter, show no tour
        response = self.client.get(self.url, HTTP_USER_AGENT=self.user_agent)
        self.assertNotIn(self.expected, response.content)

    @override_settings(DEV=True)
    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='16.0')
    def test_whatsnew_search_tour_oldversion(self):
        """Should not show tour if upgrading from 34.0 onwards."""

        self.url = reverse('firefox.whatsnew', args=['34.1'])

        # sanity check that it should show for other values of "oldversion"
        response = self.client.get(self.url + '?oldversion=28.0', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=27.0.1', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=4.0', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=rv:10.0', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=33.0', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=33.0.1', HTTP_USER_AGENT=self.user_agent)
        self.assertIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=34.0', HTTP_USER_AGENT=self.user_agent)
        self.assertNotIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=34.0.1', HTTP_USER_AGENT=self.user_agent)
        self.assertNotIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=34.1', HTTP_USER_AGENT=self.user_agent)
        self.assertNotIn(self.expected, response.content)

        response = self.client.get(self.url + '?oldversion=35.0', HTTP_USER_AGENT=self.user_agent)
        self.assertNotIn(self.expected, response.content)

        # if there's no oldversion parameter, show no tour
        response = self.client.get(self.url, HTTP_USER_AGENT=self.user_agent)
        self.assertNotIn(self.expected, response.content)


class TestHelloStartView(TestCase):
    def setUp(self):
        self.user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:35.0) '
                      'Gecko/20100101 Firefox/35.0')
        self.url = reverse('firefox.hello.start', args=['35.0'])

    def test_fx_hello_redirect_non_firefox(self):
        """Should redirect to /firefox/new if not on Firefox"""

        self.user_agent = ('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
        self.url = reverse('firefox.hello.start', args=['35.0'])
        response = self.client.get(self.url)
        self.assertIn('/firefox/new/', response['location'])
