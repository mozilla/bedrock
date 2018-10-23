# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

from django.core.cache import caches
from django.http import HttpResponse
from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_jinja.backend import Jinja2
from mock import call, Mock, patch
from nose.tools import eq_, ok_
from pyquery import PyQuery as pq

from bedrock.base.urlresolvers import reverse
from bedrock.firefox import views as fx_views
from bedrock.firefox.firefox_details import FirefoxDesktop, FirefoxAndroid, FirefoxIOS
from bedrock.firefox.utils import product_details
from bedrock.mozorg.tests import TestCase


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
PROD_DETAILS_DIR = os.path.join(TEST_DATA_DIR, 'product_details_json')
GOOD_PLATS = {'Windows': {}, 'OS X': {}, 'Linux': {}}
jinja_env = Jinja2.get_default().env

firefox_desktop = FirefoxDesktop(json_dir=PROD_DETAILS_DIR)
firefox_android = FirefoxAndroid(json_dir=PROD_DETAILS_DIR)
firefox_ios = FirefoxIOS(json_dir=PROD_DETAILS_DIR)


class TestInstallerHelp(TestCase):
    def setUp(self):
        self.button_mock = Mock()
        self.patcher = patch.dict(jinja_env.globals,
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
            call('beta', force_direct=True, force_full_installer=True, locale='fr'),
            call('alpha', force_direct=True, force_full_installer=True, locale='fr', platform='desktop'),
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
            call('beta', force_direct=True, force_full_installer=True, locale=None),
            call('alpha', force_direct=True, force_full_installer=True, locale=None, platform='desktop'),
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
            call('beta', force_direct=True, force_full_installer=True, locale=None),
            call('alpha', force_direct=True, force_full_installer=True, locale=None, platform='desktop'),
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
    pd_cache = caches['product-details']

    def setUp(self):
        self.pd_cache.clear()

    def _get_url(self, platform='desktop', channel='release'):
        with self.activate('en-US'):
            kwargs = {}

            if platform != 'desktop':
                kwargs['platform'] = platform
            if channel != 'release':
                kwargs['channel'] = channel

            return reverse('firefox.all', kwargs=kwargs)

    def test_no_search_results(self):
        """
        Tables should be gone and not-found message should be shown when there
        are no search results.
        """
        resp = self.client.get(self._get_url() + '?q=DOES_NOT_EXIST')
        doc = pq(resp.content)
        ok_(not doc('table.build-table'))
        ok_(not doc('.not-found.hide'))

    def test_no_search_query(self):
        """
        When not searching all builds should show.
        """
        resp = self.client.get(self._get_url())
        doc = pq(resp.content)
        eq_(len(doc('.build-table')), 1)
        eq_(len(doc('.not-found.hide')), 1)

        num_builds = len(firefox_desktop.get_filtered_full_builds('release'))
        num_builds += len(firefox_desktop.get_filtered_test_builds('release'))
        eq_(len(doc('tr[data-search]')), num_builds)
        eq_(len(doc('tr#en-US a')), 5)

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

    def test_android(self):
        """
        The Firefox for Android download table should only show the multi-locale
        builds for ARM and x86.
        """
        resp = self.client.get(self._get_url('android'))
        doc = pq(resp.content)
        eq_(len(doc('tbody tr')), 1)
        eq_(len(doc('tbody tr#multi a')), 2)
        eq_(len(doc('tbody tr#multi .android')), 1)
        eq_(len(doc('tbody tr#multi .android-x86')), 1)

    def test_404(self):
        """
        Firefox for iOS doesn't have the /all/ page. Also, Firefox for Android
        doesn't have the ESR channel.
        """
        resp = self.client.get(self._get_url('ios'))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self._get_url('android', 'organizations'))
        self.assertEqual(resp.status_code, 404)

    def test_301(self):
        """Android Aurora download page should be redirected to Nightly"""
        resp = self.client.get(self._get_url('android', 'aurora'))
        eq_(resp.status_code, 301)
        ok_(resp['Location'].endswith('/firefox/android/nightly/all/'))


@patch('bedrock.firefox.views.l10n_utils.render', return_value=HttpResponse())
class TestWhatsNew(TestCase):
    def setUp(self):
        self.view = fx_views.WhatsnewView.as_view()
        self.rf = RequestFactory(HTTP_USER_AGENT='Firefox')

    @override_settings(DEV=True)
    def test_fx_dev_browser_35_0_a2_whatsnew(self, render_mock):
        """Should show dev browser whatsnew template"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='35.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/dev-whatsnew.html'])

    @override_settings(DEV=True)
    def test_rv_prefix(self, render_mock):
        """Prefixed oldversion shouldn't impact version sniffing."""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=rv:10.0')
        self.view(req, version='54.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/index.html'])

    @override_settings(DEV=True)
    def test_fx_default_whatsnew(self, render_mock):
        """Should use standard template for 54.0"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='54.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/index.html'])

    # begin id locale-specific tests

    @override_settings(DEV=True)
    @patch.dict(os.environ, SWITCH_FIREFOX_LITE_WHATSNEW='True')
    def test_id_locale_template_lite(self, render_mock):
        """Should use id locale specific template for Firefox Lite"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'id'
        self.view(req, version='63.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/index-lite.id.html'])

    @override_settings(DEV=True)
    @patch.dict(os.environ, SWITCH_FIREFOX_LITE_WHATSNEW='False')
    def test_id_locale_template_rocket(self, render_mock):
        """Should use id locale specific template for Firefox Rocket"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'id'
        self.view(req, version='63.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/index.id.html'])

    # end id locale-specific tests

    # begin zh-TW locale-specific tests

    @override_settings(DEV=True)
    def test_zh_TW_locale_template(self, render_mock):
        """Should use zh-TW locale specific template"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'zh-TW'
        self.view(req, version='63.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/index.zh-TW.html'])

    # end zh-TW locale-specific tests

    # begin 57.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_57_0_EN(self, render_mock):
        """Should use English CEO letter template for 57.0 in English"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='57.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/fx57/whatsnew-57.en-US.html'])

    @override_settings(DEV=True)
    def test_fx_57_0_locale(self, render_mock):
        """Should use regular template for 57.0 in locales without the letter"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'nl'
        self.view(req, version='57.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/fx57/whatsnew-57.html'])

    @override_settings(DEV=True)
    def test_fx_dev_57_0(self, render_mock):
        """Should use developer whatsnew page for 57.0 dev edition"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='57.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/developer/whatsnew.html'])

    @override_settings(DEV=True)
    def test_fx_57_0_old_version(self, render_mock):
        """Should use Quantum template when updating from older major version"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=56.0')
        self.view(req, version='57.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/fx57/whatsnew-57.en-US.html'])

    @override_settings(DEV=True)
    def test_fx_57_0_old_minor_version(self, render_mock):
        """Should use mobile promo template when updating from older minor version"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=57.0.1')
        self.view(req, version='57.0.2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/index.html'])

    # end 57.0 whatsnew tests

    # begin 59.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_59_0(self, render_mock):
        """Should use Firefox Accounts template for 59.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='59.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/whatsnew-fxa.html'])

    @override_settings(DEV=True)
    def test_fx_59_0_old_major_version(self, render_mock):
        """Should use Firefox Accounts template when updating from older major version"""
        req = self.rf.get('/firefox/whatsnew/?oldversion=58.0')
        req.locale = 'en-US'
        self.view(req, version='59.0.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/whatsnew-fxa.html'])

    @override_settings(DEV=True)
    def test_fx_59_0_old_minor_version(self, render_mock):
        """Should use regular whatsnew template when updating from older minor version"""
        req = self.rf.get('/firefox/whatsnew/?oldversion=59.0')
        req.locale = 'en-US'
        self.view(req, version='59.0.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/index.html'])

    # end 59.0 whatsnew tests

    # begin 60.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_60_0(self, render_mock):
        """Should use FxA/Fx mobile/Focus template for 60.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='60.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/whatsnew-fx60.html'])

    @override_settings(DEV=True)
    def test_fx_60_0_old_major_version(self, render_mock):
        """Should use FxA/Fx mobile/Focus template when updating from older major version"""
        req = self.rf.get('/firefox/whatsnew/?oldversion=59.0')
        req.locale = 'en-US'
        self.view(req, version='60.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/whatsnew-fx60.html'])

    # end 60.0 whatsnew tests

    # begin 61.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_61_0(self, render_mock):
        """Should use FxA/Fx mobile/Focus template for 61.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='61.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/whatsnew-fx61.html'])

    @override_settings(DEV=True)
    def test_fx_61_0_old_major_version(self, render_mock):
        """Should use FxA/Fx mobile/Focus template when updating from older major version"""
        req = self.rf.get('/firefox/whatsnew/?oldversion=60.0')
        req.locale = 'en-US'
        self.view(req, version='61.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/whatsnew-fx61.html'])

    # end 61.0 whatsnew tests

    # begin 62.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_62_0(self, render_mock):
        """Should use Pocket/FxA/Fx mobile/Focus template for 62.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='62.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/whatsnew-fx62.html'])

    @override_settings(DEV=True)
    def test_fx_62_0_old_major_version(self, render_mock):
        """Should use Pocket/FxA/Fx mobile/Focus template when updating from older major version"""
        req = self.rf.get('/firefox/whatsnew/?oldversion=61.0')
        req.locale = 'en-US'
        self.view(req, version='62.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/whatsnew-fx62.html'])

    # end 62.0 whatsnew tests

    # begin 63.0 whatsnew tests

    def test_fx_63_0(self, render_mock):
        """Should use standard template for 63.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='63.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew/whatsnew-fx63.html'])

    # end 63.0 whatsnew tests


@patch('bedrock.firefox.views.l10n_utils.render', return_value=HttpResponse())
class TestFirstRun(TestCase):
    def setUp(self):
        self.view = fx_views.FirstrunView.as_view()
        self.rf = RequestFactory()

    @override_settings(DEV=True)
    def test_fx_firstrun_40_0(self, render_mock):
        """Should use default firstrun template"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='40.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/index.html'])

    @override_settings(DEV=True)
    def test_fx_firstrun_56_0(self, render_mock):
        """Should use the default dev edition firstrun template"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='56.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/dev-firstrun.html'])

    @override_settings(DEV=True)
    def test_fxdev_firstrun_57_0(self, render_mock):
        """Should use 57 quantum dev edition firstrun template"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='57.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/developer/firstrun.html'])

    @override_settings(DEV=True)
    def test_fx_firstrun_57_0(self, render_mock):
        """Should use 57 quantum firstrun template"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='57.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/firstrun-quantum.html'])

    # test redirect to /firefox/new/ for legacy /firstrun URLs - Bug 1343823

    @override_settings(DEV=True)
    def test_fx_firstrun_legacy_redirect(self, render_mock):
        req = self.rf.get('/firefox/firstrun/')
        req.locale = 'en-US'
        resp = self.view(req, version='39.0')
        assert resp.status_code == 301
        assert resp['location'].endswith('/firefox/new/')

    def test_fx_firstrun_dev_edition_legacy_redirect(self, render_mock):
        req = self.rf.get('/firefox/firstrun/')
        req.locale = 'en-US'
        resp = self.view(req, version='39.0a2')
        assert resp.status_code == 301
        assert resp['location'].endswith('/firefox/new/')


@patch.object(fx_views, 'firefox_desktop', firefox_desktop)
class FxVersionRedirectsMixin(object):
    @override_settings(DEV=True)  # avoid https redirects
    def assert_ua_redirects_to(self, ua, url_name, status_code=301):
        response = self.client.get(self.url, HTTP_USER_AGENT=ua)
        eq_(response.status_code, status_code)
        eq_(response['Cache-Control'], 'max-age=0')
        eq_(response['Location'],
            'http://testserver%s' % reverse(url_name))

        # An additional redirect test with a query string
        query = '?ref=getfirefox'
        response = self.client.get(self.url + query, HTTP_USER_AGENT=ua)
        eq_(response.status_code, status_code)
        eq_(response['Cache-Control'], 'max-age=0')
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
        eq_(response['Cache-Control'], 'max-age=0')

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
        eq_(response['Cache-Control'], 'max-age=0')

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
        eq_(response['Cache-Control'], 'max-age=0')

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
        eq_(response['Cache-Control'], 'max-age=0')


@patch('bedrock.firefox.views.l10n_utils.render', return_value=HttpResponse())
class TestTrackingProtectionTour(TestCase):
    def setUp(self):
        self.view = fx_views.TrackingProtectionTourView.as_view()
        self.rf = RequestFactory()

    @override_settings(DEV=True)
    def test_fx_tracking_protection_62_0(self, render_mock):
        """Should use default tracking protection tour template"""
        req = self.rf.get('/en-US/firefox/tracking-protection/start/')
        self.view(req, version='62.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/tracking-protection-tour/index.html'])

    @override_settings(DEV=True)
    def test_fx_tracking_protection_63_0_v0(self, render_mock):
        """Should use variation 0 template"""
        req = self.rf.get('/en-US/firefox/tracking-protection/start/?variation=0')
        self.view(req, version='62.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/tracking-protection-tour/variation-0.html'])

    @override_settings(DEV=True)
    def test_fx_tracking_protection_63_0_v1(self, render_mock):
        """Should use variation 1 template"""
        req = self.rf.get('/en-US/firefox/tracking-protection/start/?variation=1')
        self.view(req, version='62.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/tracking-protection-tour/variation-1.html'])

    @override_settings(DEV=True)
    def test_fx_tracking_protection_63_0_v2(self, render_mock):
        """Should use variation 2 template"""
        req = self.rf.get('/en-US/firefox/tracking-protection/start/?variation=2')
        self.view(req, version='62.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/tracking-protection-tour/variation-2.html'])
