# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from math import floor
import time
from hashlib import md5

from django.conf import settings
from django.test import Client, RequestFactory
from django.utils.http import parse_http_date

from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_, ok_

from bedrock.mozorg.tests import TestCase
from bedrock.tabzilla.middleware import TabzillaLocaleURLMiddleware


class TabzillaViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_tabzilla_content_type(self):
        """ Content-Type header should be text/javascript. """
        with self.activate('en-US'):
            resp = self.client.get(reverse('tabzilla'))
        self.assertEqual(resp['content-type'], 'text/javascript')

    def test_cache_headers(self):
        """
        Should have appropriate Cache-Control, Expires, and ETag headers.
        """
        with self.activate('en-US'):
            resp = self.client.get(reverse('tabzilla'))
        self.assertEqual(resp['cache-control'], 'max-age=43200')  # 12h

        now_date = floor(time.time())
        exp_date = parse_http_date(resp['expires'])
        self.assertAlmostEqual(now_date + 43200, exp_date, delta=2)

        etag = '"%s"' % md5(resp.content).hexdigest()
        self.assertEqual(resp['etag'], etag)


@patch.object(settings, 'DEV_LANGUAGES', ['en-US', 'de'])
@patch.object(settings, 'PROD_LANGUAGES', ['en-US', 'de'])
class TabzillaRedirectTests(TestCase):
    def setUp(self):
        self.client = Client()

    def _process_request(self, url):
        rf = RequestFactory()
        req = rf.get(url)
        return TabzillaLocaleURLMiddleware().process_request(req)

    def test_locale_preserved(self):
        """The tabzilla URL should preserve the locale through redirects."""
        resp = self.client.get('/de/tabzilla/media/js/tabzilla.js')
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp['Location'],
                         'http://testserver/de/tabzilla/tabzilla.js')

    @patch.object(settings, 'MEDIA_URL', '//example.com/')
    @patch.object(settings, 'TEMPLATE_DEBUG', False)
    def test_tabzilla_css_redirect(self):
        """
        Tabzilla css redirect should use MEDIA_URL setting and switch
        based on TEMPLATE_DEBUG setting.
        Bug 826866.
        """
        tabzilla_css_url = '/en-US/tabzilla/media/css/tabzilla.css'
        with self.activate('en-US'):
            response = self.client.get(tabzilla_css_url)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'http://example.com/css/tabzilla-min.css')

        with patch.object(settings, 'TEMPLATE_DEBUG', True):
            with self.activate('en-US'):
                response = self.client.get(tabzilla_css_url)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'http://example.com/css/tabzilla/tabzilla.less.css')

    @patch('jingo_minify.helpers.build_less')
    def test_tabzilla_css_less_processing(self, less_mock):
        """
        The tabzilla.less file should be compiled by the redirect if
        settings.LESS_PREPROCESS is True.
        """
        tabzilla_css_url = '/en-US/tabzilla/media/css/tabzilla.css'
        with patch.object(settings, 'LESS_PREPROCESS', False):
            with self.activate('en-US'):
                self.client.get(tabzilla_css_url)
        eq_(less_mock.call_count, 0)

        with patch.object(settings, 'LESS_PREPROCESS', True):
            with self.activate('en-US'):
                self.client.get(tabzilla_css_url)
        eq_(less_mock.call_count, 1)

    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '//example.com')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', True)
    def test_no_cdn_redirect_middleware_template_debug(self):
        """
        Tabzilla should NOT redirect to a CDN when it redirects to a locale
        when TEMPLATE_DEBUG = True.
        """
        resp = self._process_request('/tabzilla/tabzilla.js')
        eq_(resp['location'], '/en-US/tabzilla/tabzilla.js')

    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '//example.com')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', False)
    def test_no_cdn_redirect_middleware_specified_locale(self):
        """
        Tabzilla should NOT redirect to a CDN when it doesn't need to redirect
        to a locale.
        """
        resp = self._process_request('/en-US/tabzilla/tabzilla.js')
        ok_(resp is None)

    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', True)
    def test_no_cdn_redirect_middleware_no_cdn(self):
        """
        Tabzilla should NOT redirect to a CDN when it redirects to a locale
        when no CDN is configured.
        """
        resp = self._process_request('/tabzilla/tabzilla.js')
        eq_(resp['location'], '/en-US/tabzilla/tabzilla.js')

    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '//example.com')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', False)
    def test_cdn_redirect_middleware(self):
        """
        Tabzilla should redirect to a CDN when it redirects to a locale
        """
        resp = self._process_request('/tabzilla/tabzilla.js')
        eq_(resp['location'], 'http://example.com/en-US/tabzilla/tabzilla.js')

    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '//example.com')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', False)
    def test_no_cdn_redirect_middleware(self):
        """
        Middleware should NOT redirect to a CDN when it's not tabzilla
        """
        resp = self._process_request('/')
        eq_(resp['location'], '/en-US/')

    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '//example.com')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', False)
    @patch('lib.l10n_utils.settings.DEV', False)
    @patch('lib.l10n_utils.lang_file_is_active')
    def test_redirect_to_cdn_inactive_locale(self, lang_mock):
        """
        The view should redirect to the CDN when the locale is not active.
        """
        lang_mock.return_value = False
        resp = self.client.get('/de/tabzilla/tabzilla.js')
        eq_(resp['location'], 'http://example.com/en-US/tabzilla/tabzilla.js')

    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '//example.com')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', False)
    @patch('lib.l10n_utils.settings.DEV', False)
    @patch('lib.l10n_utils.lang_file_is_active')
    def test_no_redirect_to_cdn_active_locale(self, lang_mock):
        """
        The view should NOT redirect to the CDN when the locale is active.
        """
        lang_mock.return_value = True
        resp = self.client.get('/de/tabzilla/tabzilla.js')
        ok_(resp.status_code == 200)

    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', False)
    @patch('lib.l10n_utils.settings.DEV', False)
    @patch('lib.l10n_utils.lang_file_is_active')
    def test_no_redirect_to_cdn_no_cdn(self, lang_mock):
        """
        The view should not redirect to the CDN when the CDN setting is empty.
        """
        lang_mock.return_value = False
        resp = self.client.get('/de/tabzilla/tabzilla.js')
        eq_(resp['location'], 'http://testserver/en-US/tabzilla/tabzilla.js')

    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '//example.com')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', True)
    @patch('lib.l10n_utils.settings.DEV', False)
    @patch('lib.l10n_utils.lang_file_is_active')
    def test_no_redirect_to_cdn_template_debug(self, lang_mock):
        """
        The view should not redirect to the CDN when TEMPLATE_DEBUG is True.
        """
        lang_mock.return_value = False
        resp = self.client.get('/de/tabzilla/tabzilla.js')
        eq_(resp['location'], 'http://testserver/en-US/tabzilla/tabzilla.js')
