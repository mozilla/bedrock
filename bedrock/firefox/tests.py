# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import json

import os
from urlparse import parse_qsl, urlparse

from django.conf import settings
from django.test.client import Client
from django.utils import simplejson

from funfactory.urlresolvers import reverse
from mock import ANY, call, Mock, patch
from nose.tools import eq_, ok_
from pyquery import PyQuery as pq

from bedrock.firefox import views as fx_views
from bedrock.firefox.firefox_details import FirefoxDetails, MobileDetails
from bedrock.firefox.utils import product_details
from bedrock.mozorg.tests import TestCase


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
PROD_DETAILS_DIR = os.path.join(TEST_DATA_DIR, 'product_details_json')

with patch.object(settings, 'PROD_DETAILS_DIR', PROD_DETAILS_DIR):
    firefox_details = FirefoxDetails()
    mobile_details = MobileDetails()


class TestInstallerHelp(TestCase):
    def setUp(self):
        self.button_mock = Mock()
        self.patcher = patch.dict('jingo.env.globals',
                                  download_firefox=self.button_mock)
        self.patcher.start()
        self.client = Client()
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
            call('aurora', small=ANY, force_direct=True,
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
            call('aurora', small=ANY, force_direct=True,
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
            call('aurora', small=ANY, force_direct=True,
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


@patch.object(fx_views, 'firefox_details', firefox_details)
class TestFirefoxDetails(TestCase):

    def test_get_download_url(self):
        url = firefox_details.get_download_url('OS X', 'pt-BR', '17.0')
        self.assertListEqual(parse_qsl(urlparse(url).query),
                             [('product', 'firefox-17.0'),
                              ('os', 'osx'),
                              ('lang', 'pt-BR')])

    def test_filter_builds_by_locale_name(self):
        # search english
        builds = firefox_details.get_filtered_full_builds(
            firefox_details.latest_version('release'),
            'ujara'
        )
        eq_(len(builds), 1)
        eq_(builds[0]['name_en'], 'Gujarati')

        # search native
        builds = firefox_details.get_filtered_full_builds(
            firefox_details.latest_version('release'),
            u'જરા'
        )
        eq_(len(builds), 1)
        eq_(builds[0]['name_en'], 'Gujarati')

    @patch.dict(firefox_details.firefox_versions,
                LATEST_FIREFOX_VERSION='25.0.2')
    def test_esr_major_versions(self):
        """ESR versions should be dynamic based on latest"""
        eq_(firefox_details.esr_major_versions, [10, 17, 24])

    @patch.dict(firefox_details.firefox_versions,
                LATEST_FIREFOX_VERSION='Phoenix')
    def test_esr_major_versions_no_latest(self):
        """ESR versions should not blow up if current version is broken."""
        eq_(firefox_details.esr_major_versions, [])

    @patch.dict(firefox_details.firefox_versions,
                LATEST_FIREFOX_VERSION='18.0.1')
    def test_latest_major_version(self):
        """latest_major_version should return an int of the major version."""
        eq_(firefox_details.latest_major_version('release'), 18)

    @patch.dict(firefox_details.firefox_versions,
                LATEST_FIREFOX_VERSION='Phoenix')
    def test_latest_major_version_no_int(self):
        """latest_major_version should return 0 when no int."""
        eq_(firefox_details.latest_major_version('release'), 0)


@patch.object(fx_views, 'mobile_details', mobile_details)
class TestMobileDetails(TestCase):

    @patch.dict(mobile_details.mobile_details,
                version='22.0.1')
    def test_latest_release_version(self):
        """latest_version should return the latest release version."""
        eq_(mobile_details.latest_version('release'), '22.0.1')

    @patch.dict(mobile_details.mobile_details,
                beta_version='23.0')
    def test_latest_beta_version(self):
        """latest_version should return the latest beta version."""
        eq_(mobile_details.latest_version('beta'), '23.0')


@patch.object(fx_views, 'firefox_details', firefox_details)
class TestFirefoxAll(TestCase):
    def setUp(self):
        self.client = Client()
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

        release = firefox_details.latest_version('release')
        num_builds = len(firefox_details.get_filtered_full_builds(release))
        num_builds += len(firefox_details.get_filtered_test_builds(release))
        eq_(len(doc('tr[data-search]')), num_builds)


class TestFirefoxPartners(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('bedrock.firefox.views.settings.DEBUG', True)
    def test_js_bundle_files_debug_true(self):
        """
        When DEBUG is on the bundle should return the individual files
        with the MEDIA_URL.
        """
        bundle = 'partners_desktop'
        files = settings.MINIFY_BUNDLES['js'][bundle]
        files = [settings.MEDIA_URL + f for f in files]
        self.assertEqual(files,
                         json.loads(fx_views.get_js_bundle_files(bundle)))

    @patch('bedrock.firefox.views.settings.DEBUG', False)
    def test_js_bundle_files_debug_false(self):
        """
        When DEBUG is off the bundle should return a single minified filename.
        """
        bundle = 'partners_desktop'
        filename = '%sjs/%s-min.js?build=' % (settings.MEDIA_URL, bundle)
        bundle_file = json.loads(fx_views.get_js_bundle_files(bundle))
        self.assertEqual(len(bundle_file), 1)
        self.assertTrue(bundle_file[0].startswith(filename))

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
        resp_data = simplejson.loads(resp.content)

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

        # decode JSON response
        resp_data = simplejson.loads(resp.content)

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

        # decode JSON response
        resp_data = simplejson.loads(resp.content)

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
            '00NU0000002pDJr': [],
            'email': u'thedude@mozilla.com',
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


@patch.object(fx_views, 'firefox_details', firefox_details)
class FxVersionRedirectsMixin(object):
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

    def test_bad_firefox(self):
        """
        Any user agents with malformed Firefox UA strings should be permanently
        redirected to /firefox/new/.
        """
        user_agent = 'Mozilla/5.0 (SaferSurf) Firefox 1.5'
        self.assert_ua_redirects_to(user_agent, 'firefox.new')

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='14.0')
    def test_old_firefox(self):
        """
        Any older versions of Firefox should be permanently redirected to
        /firefox/new/.
        """
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) '
                      'Gecko/20100101 Firefox/13.0')
        self.assert_ua_redirects_to(user_agent, 'firefox.new')

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='13.0.5')
    def test_current_minor_version_firefox(self):
        """
        Should show current even if behind by a patch version
        """
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) '
                      'Gecko/20100101 Firefox/13.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='18.0')
    def test_esr_firefox(self):
        """
        Currently released ESR firefoxen should not redirect. At present
        they are 10.0.x and 17.0.x.
        """
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:10.0.12) '
                      'Gecko/20111101 Firefox/10.0.12')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')

        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:17.0) '
                      'Gecko/20100101 Firefox/17.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='16.0')
    def test_current_firefox(self):
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:16.0) '
                      'Gecko/20100101 Firefox/16.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='16.0')
    def test_future_firefox(self):
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:18.0) '
                      'Gecko/20100101 Firefox/18.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')


class TestWhatsnewRedirect(FxVersionRedirectsMixin, TestCase):
    def setUp(self):
        self.client = Client()
        with self.activate('en-US'):
            self.url = reverse('firefox.whatsnew', args=['13.0'])


class TestFirstrunRedirect(FxVersionRedirectsMixin, TestCase):
    def setUp(self):
        self.client = Client()
        with self.activate('en-US'):
            self.url = reverse('firefox.firstrun', args=['13.0'])

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='16.0')
    def test_firstrun_standard(self):
        """
        Hitting /firefox/{version}/firstrun/ with latest Fx should render
        firefox/firstrun.html, regardless of {version}.
        """
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:16.0) '
                      'Gecko/20100101 Firefox/16.0')

        expected = 'See how Firefox keeps the power of the web in your hands'

        # TODO: use assertTemplateUsed in place of assertIn when available?
        # jinja may get in the way though...

        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        self.assertIn(expected, response.content)

        self.url = reverse('firefox.firstrun', args=['24.0'])
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        self.assertIn(expected, response.content)

        self.url = reverse('firefox.firstrun')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        self.assertIn(expected, response.content)

    @patch.dict(product_details.firefox_versions,
            LATEST_FIREFOX_VERSION='16.0')
    def test_firstrun_alternate(self):
        """
        Hitting /firefox/{version}/firstrun/?f={fx_views.FirstrunView.funnelcake_campaign}
        with latest Fx & en-US locale should render firefox/firstrun/a.html, regardless of
        {version}. Any other f value or locale should render firefox/firstrun.html.
        """
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:16.0) '
                      'Gecko/20100101 Firefox/16.0')

        fc_id = fx_views.FirstrunView.funnelcake_campaign
        expected = 'Use Themes to change the look of your Firefox just about any way you like.'

        # en-US with proper funnelcake id should give expected content
        response = self.client.get(self.url + '?f=' + fc_id, HTTP_USER_AGENT=user_agent)
        self.assertIn(expected, response.content)

        # en-US with improper funnelcake id should not give expected content
        response = self.client.get(self.url + '?f=0', HTTP_USER_AGENT=user_agent)
        self.assertNotIn(expected, response.content)

        # en-US with no funnelcake id should not give expected content
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        self.assertNotIn(expected, response.content)

        # en-US with proper funnelcake id and no {version} should give expected content
        self.url = reverse('firefox.firstrun')
        response = self.client.get(self.url + '?f=' + fc_id, HTTP_USER_AGENT=user_agent)
        self.assertIn(expected, response.content)

        # es-ES with proper funnelcake id should not give expected content
        with self.activate('es-ES'):
            self.url = reverse('firefox.firstrun', args=['16.0'])
            response = self.client.get(self.url + '?f=' + fc_id, HTTP_USER_AGENT=user_agent)
            self.assertNotIn(expected, response.content)


@patch.object(fx_views, 'firefox_details', firefox_details)
@patch.object(fx_views, 'mobile_details', mobile_details)
class TestNotesRedirects(TestCase):
    def setUp(self):
        self.client = Client()

    def _test(self, url_from, url_to):
        with self.activate('en-US'):
            url = '/en-US' + url_from
        response = self.client.get(url)
        eq_(response.status_code, 302)
        eq_(response['Location'], 'http://testserver/en-US' + url_to)

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='22.0')
    def test_desktop_release_version(self):
        self._test('/firefox/notes/',
                   '/firefox/22.0/releasenotes/')

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_DEVEL_VERSION='23.0b1')
    def test_desktop_beta_version(self):
        self._test('/firefox/beta/notes/',
                   '/firefox/23.0beta/releasenotes/')

    @patch.dict(product_details.firefox_versions,
                FIREFOX_AURORA='24.0a2')
    def test_desktop_aurora_version(self):
        self._test('/firefox/aurora/notes/',
                   '/firefox/24.0a2/auroranotes/')

    @patch.dict(product_details.mobile_details,
                version='22.0')
    def test_mobile_release_version(self):
        self._test('/mobile/notes/',
                   '/mobile/22.0/releasenotes/')

    @patch.dict(product_details.mobile_details,
                beta_version='23.0b1')
    def test_mobile_beta_version(self):
        self._test('/mobile/beta/notes/',
                   '/mobile/23.0beta/releasenotes/')

    @patch.dict(product_details.mobile_details,
                alpha_version='24.0a2')
    def test_mobile_aurora_version(self):
        self._test('/mobile/aurora/notes/',
                   '/mobile/24.0a2/auroranotes/')


@patch.object(fx_views, 'firefox_details', firefox_details)
class TestSysreqRedirect(TestCase):
    def setUp(self):
        self.client = Client()

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='22.0')
    def test_release_version(self):
        with self.activate('en-US'):
            url = '/en-US/firefox/system-requirements.html'
        response = self.client.get(url)
        eq_(response.status_code, 302)
        eq_(response['Location'],
            'http://testserver/en-US/firefox/22.0/system-requirements/')
