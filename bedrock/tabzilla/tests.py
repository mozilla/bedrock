# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from datetime import datetime
from math import floor

from django.conf import settings
from django.test import RequestFactory
from django.test.utils import override_settings
from django.utils.http import parse_http_date

from bedrock.base.urlresolvers import reverse
from mock import patch
from nose.tools import eq_, ok_

from bedrock.mozorg.tests import TestCase
from bedrock.tabzilla.middleware import TabzillaLocaleURLMiddleware
from bedrock.tabzilla.views import template_last_modified


@patch('bedrock.tabzilla.views.os.path.getmtime')
@patch('bedrock.tabzilla.views.loader.get_template')
class LastModifiedTests(TestCase):
    def test_youngest_file_wins(self, template_mock, mtime_mock):
        tmpl_name = 'the_dude_is_a_template.html'
        template_mock.return_value.template.filename = tmpl_name
        mtimes = [1378762234.0, 1378762235.0]
        mtime_mock.side_effect = mtimes
        func = template_last_modified(tmpl_name)
        datestamp = func({})
        self.assertEqual(datestamp, datetime.fromtimestamp(max(mtimes)))
        mtime_mock.assert_any_call(tmpl_name)
        langfile = '{0}/locale/en-US/tabzilla/tabzilla.lang'.format(settings.ROOT)
        mtime_mock.assert_any_call(langfile)


class TabzillaViewTests(TestCase):
    def test_tabzilla_content_type(self):
        """ Content-Type header should be text/javascript. """
        with self.activate('en-US'):
            resp = self.client.get(reverse('tabzilla'))
        self.assertEqual(resp['content-type'], 'text/javascript')

    def test_cache_headers(self):
        """
        Should have appropriate Cache-Control and Expires headers.
        """
        with self.activate('en-US'):
            resp = self.client.get(reverse('tabzilla'))
        self.assertEqual(resp['cache-control'], 'max-age=43200')  # 12h

        now_date = floor(time.time())
        exp_date = parse_http_date(resp['expires'])
        self.assertAlmostEqual(now_date + 43200, exp_date, delta=2)


@patch.object(settings, 'DEV_LANGUAGES', ['en-US', 'de'])
@patch.object(settings, 'PROD_LANGUAGES', ['en-US', 'de'])
class TabzillaRedirectTests(TestCase):
    def _process_request(self, url):
        rf = RequestFactory()
        req = rf.get(url)
        return TabzillaLocaleURLMiddleware().process_request(req)

    @patch('bedrock.tabzilla.urls.default_collector')
    @patch('bedrock.tabzilla.urls.Packager')
    def test_tabzilla_css_redirect(self, packager_mock, collector_mock):
        """
        Tabzilla css redirect should use STATIC_URL setting and switch
        based on DEBUG setting.
        Bug 826866.
        """
        packager = packager_mock.return_value
        package = packager.package_for.return_value
        package.output_filename = settings.PIPELINE_CSS['tabzilla']['output_filename']
        packager.compile.return_value = ['css/tabzilla/tabzilla.css']
        tabzilla_css_url = '/en-US/tabzilla/media/css/tabzilla.css'
        with override_settings(DEBUG=False):
            with self.activate('en-US'):
                response = self.client.get(tabzilla_css_url)
        eq_(response.status_code, 301)
        ok_(response['location'].endswith('/css/tabzilla-min.css'), response['location'])

        with override_settings(DEBUG=True):
            with self.activate('en-US'):
                response = self.client.get(tabzilla_css_url)
        eq_(response.status_code, 301)
        ok_(response['location'].endswith('/css/tabzilla/tabzilla.css'), response['location'])

    @patch('bedrock.tabzilla.urls.default_collector')
    @patch('bedrock.tabzilla.urls.Packager')
    def test_tabzilla_css_less_processing(self, packager_mock, collector_mock):
        """
        The tabzilla.less file should be compiled by the redirect if
        settings.DEBUG is True.
        """
        compiler = packager_mock.return_value.compile
        tabzilla_css_url = '/en-US/tabzilla/media/css/tabzilla.css'
        with override_settings(DEBUG=False):
            with self.activate('en-US'):
                self.client.get(tabzilla_css_url)
        eq_(compiler.call_count, 0)

        with override_settings(DEBUG=True):
            with self.activate('en-US'):
                self.client.get(tabzilla_css_url)
        eq_(compiler.call_count, 1)

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

    @override_settings(DEV=False)
    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '//example.com')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', False)
    @patch('lib.l10n_utils.template_is_active')
    def test_redirect_to_cdn_inactive_locale(self, lang_mock):
        """
        The view should redirect to the CDN when the locale is not active.
        """
        lang_mock.return_value = False
        resp = self.client.get('/de/tabzilla/tabzilla.js')
        eq_(resp['location'], 'http://example.com/en-US/tabzilla/tabzilla.js')

    @override_settings(DEV=False)
    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '//example.com')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', False)
    @patch('lib.l10n_utils.template_is_active')
    def test_no_redirect_to_cdn_active_locale(self, lang_mock):
        """
        The view should NOT redirect to the CDN when the locale is active.
        """
        lang_mock.return_value = True
        resp = self.client.get('/de/tabzilla/tabzilla.js')
        ok_(resp.status_code == 200)

    @override_settings(DEV=False)
    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', False)
    @patch('lib.l10n_utils.template_is_active')
    def test_no_redirect_to_cdn_no_cdn(self, lang_mock):
        """
        The view should not redirect to the CDN when the CDN setting is empty.
        """
        lang_mock.return_value = False
        resp = self.client.get('/de/tabzilla/tabzilla.js')
        eq_(resp['location'], 'http://testserver/en-US/tabzilla/tabzilla.js')

    @override_settings(DEV=False)
    @patch('bedrock.tabzilla.middleware.settings.CDN_BASE_URL', '//example.com')
    @patch('bedrock.tabzilla.middleware.settings.TEMPLATE_DEBUG', True)
    @patch('lib.l10n_utils.template_is_active')
    def test_no_redirect_to_cdn_template_debug(self, lang_mock):
        """
        The view should not redirect to the CDN when TEMPLATE_DEBUG is True.
        """
        lang_mock.return_value = False
        resp = self.client.get('/de/tabzilla/tabzilla.js')
        eq_(resp['location'], 'http://testserver/en-US/tabzilla/tabzilla.js')
