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
from pyquery import PyQuery as pq

from bedrock.base.urlresolvers import reverse
from bedrock.firefox import views as fx_views
from bedrock.firefox.firefox_details import FirefoxDesktop, FirefoxAndroid
from bedrock.mozorg.tests import TestCase


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
PROD_DETAILS_DIR = os.path.join(TEST_DATA_DIR, 'product_details_json')
GOOD_PLATS = {'Windows': {}, 'OS X': {}, 'Linux': {}}
jinja_env = Jinja2.get_default().env


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


class TestFirefoxAll(TestCase):
    pd_cache = caches['product-details']

    def setUp(self):
        self.pd_cache.clear()
        self.firefox_desktop = FirefoxDesktop(json_dir=PROD_DETAILS_DIR)
        self.firefox_android = FirefoxAndroid(json_dir=PROD_DETAILS_DIR)
        self.patcher = patch.object(
            fx_views, 'firefox_desktop', self.firefox_desktop)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def _get_url(self, platform='desktop', channel='release'):
        with self.activate('en-US'):
            kwargs = {}

            if platform != 'desktop':
                kwargs['platform'] = platform
            if channel != 'release':
                kwargs['channel'] = channel

            return reverse('firefox.all', kwargs=kwargs)

    @patch.object(fx_views, 'lang_file_is_active', lambda *x: True)
    def test_all_builds_results(self):
        """
        The unified page should display builds for all products
        """
        resp = self.client.get(self._get_url())
        doc = pq(resp.content)
        assert len(doc('.c-all-downloads-build')) == 8

        desktop_release_builds = len(self.firefox_desktop.get_filtered_full_builds('release'))
        assert len(doc('.c-locale-list[data-product="desktop_release"] > li')) == desktop_release_builds
        assert len(doc('.c-locale-list[data-product="desktop_release"] > li[data-language="en-US"] > ul > li > a')) == 7

        desktop_beta_builds = len(self.firefox_desktop.get_filtered_full_builds('beta'))
        assert len(doc('.c-locale-list[data-product="desktop_beta"] > li')) == desktop_beta_builds
        assert len(doc('.c-locale-list[data-product="desktop_beta"] > li[data-language="en-US"] > ul > li > a')) == 7

        desktop_developer_builds = len(self.firefox_desktop.get_filtered_full_builds('alpha'))
        assert len(doc('.c-locale-list[data-product="desktop_developer"] > li')) == desktop_developer_builds
        assert len(doc('.c-locale-list[data-product="desktop_developer"] > li[data-language="en-US"] > ul > li > a')) == 7

        desktop_nightly_builds = len(self.firefox_desktop.get_filtered_full_builds('nightly'))
        assert len(doc('.c-locale-list[data-product="desktop_nightly"] > li')) == desktop_nightly_builds
        assert len(doc('.c-locale-list[data-product="desktop_nightly"] > li[data-language="en-US"] > ul > li > a')) == 7

        desktop_esr_builds = len(self.firefox_desktop.get_filtered_full_builds('esr'))
        assert len(doc('.c-locale-list[data-product="desktop_esr"] > li')) == desktop_esr_builds
        assert len(doc('.c-locale-list[data-product="desktop_esr"] > li[data-language="en-US"] > ul > li > a')) == 7

        android_release_builds = len(self.firefox_android.get_filtered_full_builds('release'))
        assert len(doc('.c-locale-list[data-product="android_release"] > li')) == android_release_builds
        assert len(doc('.c-locale-list[data-product="android_release"] > li[data-language="multi"] > ul > li > a')) == 2

        android_beta_builds = len(self.firefox_android.get_filtered_full_builds('beta'))
        assert len(doc('.c-locale-list[data-product="android_beta"] > li')) == android_beta_builds
        assert len(doc('.c-locale-list[data-product="android_beta"] > li[data-language="multi"] > ul > li > a')) == 2

        android_nightly_builds = len(self.firefox_android.get_filtered_full_builds('nightly'))
        assert len(doc('.c-locale-list[data-product="android_nightly"] > li')) == android_nightly_builds
        assert len(doc('.c-locale-list[data-product="android_nightly"] > li[data-language="multi"] > ul > li > a')) == 2

    @patch.object(fx_views, 'lang_file_is_active', lambda *x: False)
    def test_no_search_results(self):
        """
        Tables should be gone and not-found message should be shown when there
        are no search results.
        """
        resp = self.client.get(self._get_url() + '?q=DOES_NOT_EXIST')
        doc = pq(resp.content)
        assert not doc('table.build-table')
        assert not doc('.not-found.hide')

    @patch.object(fx_views, 'lang_file_is_active', lambda *x: False)
    def test_no_search_query(self):
        """
        When not searching all builds should show.
        """
        resp = self.client.get(self._get_url())
        doc = pq(resp.content)
        assert len(doc('.build-table')) == 1
        assert len(doc('.not-found.hide')) == 1

        num_builds = len(
            self.firefox_desktop.get_filtered_full_builds('release'))
        num_builds += len(
            self.firefox_desktop.get_filtered_test_builds('release'))
        assert len(doc('tr[data-search]')) == num_builds
        assert len(doc('tr#en-US a')) == 7

    def test_no_locale_details(self):
        """
        When a localized build has been added to the Firefox details while the
        locale details are not updated yet, the filtered build list should not
        include the localized build.
        """
        builds = self.firefox_desktop.get_filtered_full_builds('release')
        assert 'uz' in self.firefox_desktop.firefox_primary_builds
        assert 'uz' not in self.firefox_desktop.languages
        assert len([build for build in builds if build['locale'] == 'uz']) == 0

    def test_android(self):
        """
        The Firefox for Android download table should only show the multi-locale
        builds for ARM and x86.
        """
        resp = self.client.get(self._get_url('android'))
        doc = pq(resp.content)
        assert len(doc('tbody tr')) == 1
        assert len(doc('tbody tr#multi a')) == 2
        assert len(doc('tbody tr#multi .android')) == 1
        assert len(doc('tbody tr#multi .android-x86')) == 1

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
        assert resp.status_code == 301
        assert resp['Location'].endswith('/firefox/android/nightly/all/')


@patch('bedrock.firefox.views.l10n_utils.render', return_value=HttpResponse())
class TestWhatsNew(TestCase):
    def setUp(self):
        self.view = fx_views.WhatsnewView.as_view()
        self.rf = RequestFactory(HTTP_USER_AGENT='Firefox')

    # begin nightly whatsnew tests

    @override_settings(DEV=True)
    def test_fx_nightly_68_0_a1_whatsnew(self, render_mock):
        """Should show nightly whatsnew template"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='68.0a1')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/nightly_whatsnew.html']

    # end nightly whatsnew tests

    # begin beta whatsnew tests

    @override_settings(DEV=True)
    def test_fx_beta_whatsnew(self, render_mock):
        """Should show default whatsnew template"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='71.0beta')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index.html']

    # end beta whatsnew tests

    # begin dev edition whatsnew tests

    @override_settings(DEV=True)
    def test_fx_dev_browser_35_0_a2_whatsnew(self, render_mock):
        """Should show default whatsnew template"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='35.0a2')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index.html']

    @override_settings(DEV=True)
    def test_fx_dev_browser_57_0_a2_whatsnew(self, render_mock):
        """Should show dev browser 57 whatsnew template"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='57.0a2')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/developer/whatsnew.html']

    @override_settings(DEV=True)
    @patch.dict(os.environ, SWITCH_DEV_WHATSNEW_68='False')
    def test_fx_dev_browser_68_0_a2_whatsnew_off(self, render_mock):
        """Should show regular dev browser whatsnew template"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='68.0a2')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/developer/whatsnew.html']

    # end dev edition whatsnew tests

    @override_settings(DEV=True)
    def test_rv_prefix(self, render_mock):
        """Prefixed oldversion shouldn't impact version sniffing."""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=rv:10.0')
        self.view(req, version='54.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index.html']

    @override_settings(DEV=True)
    def test_fx_default_whatsnew(self, render_mock):
        """Should use standard template for 62.0"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='62.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index.html']

    # begin id locale-specific tests

    @override_settings(DEV=True)
    def test_id_locale_template_lite(self, render_mock):
        """Should use id locale specific template for Firefox Lite"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'id'
        self.view(req, version='63.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index-lite.id.html']

    # end id locale-specific tests

    # begin 67.0.5 whatsnew tests

    def test_fx_67_0_1(self, render_mock):
        """Should use trailhead template for 67.0.1"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='67.0.1')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx67.0.5.html']

    def test_fx_67_0_1_locales(self, render_mock):
        """Should use standard template for 67.0.1 for other locales"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'es-ES'
        self.view(req, version='67.0.1')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx67.html']

    # end 67.0.5 whatsnew tests

    # begin 68.0 whatsnew tests

    def test_fx_68_0(self, render_mock):
        """Should use trailhead template for 68.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='68.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx68-trailhead.html']

    def test_fx_68_0_locales(self, render_mock):
        """Should use standard template for 68.0 for other locales"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'es-ES'
        self.view(req, version='68.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx68.html']

    # end 68.0 whatsnew tests

    # begin 69.0 whatsnew tests

    def test_fx_69_0(self, render_mock):
        """Should use whatsnew-69 template for 69.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='69.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx69.html']

    # end 69.0 whatsnew tests

    # begin 70.0 whatsnew tests

    def test_fx_70_0_en(self, render_mock):
        """Should use whatsnew-70-en template for 70.0 for en- locales"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='70.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx70-en.html']

    def test_fx_70_0_de(self, render_mock):
        """Should use whatsnew-70-de template for 70.0 in de locale"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'de'
        self.view(req, version='70.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx70-de.html']

    def test_fx_70_0_fr(self, render_mock):
        """Should use whatsnew-70-fr template for 70.0 in fr locale"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'fr'
        self.view(req, version='70.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx70-fr.html']

    def test_fx_70_0(self, render_mock):
        """Should use default whatsnew-70 template for 70.0 for other locales"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'es-ES'
        self.view(req, version='70.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx70.html']

    # end 70.0 whatsnew tests


@patch('bedrock.firefox.views.l10n_utils.render', return_value=HttpResponse())
class TestWhatsNewIndia(TestCase):
    def setUp(self):
        self.view = fx_views.WhatsNewIndiaView.as_view()
        self.rf = RequestFactory(HTTP_USER_AGENT='Firefox')

    def test_fx_india(self, render_mock):
        """Should use whatsnew-india template for india for en-* locales"""
        req = self.rf.get('/firefox/whatsnew/india/')
        req.locale = 'en-GB'
        self.view(req, version='70.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index-lite.html']


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
        assert template == ['firefox/firstrun/firstrun.html']

    @override_settings(DEV=True)
    def test_fx_firstrun_56_0(self, render_mock):
        """Should use the default firstrun template"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='56.0a2')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/firstrun/firstrun.html']

    @override_settings(DEV=True)
    def test_fxdev_firstrun_57_0(self, render_mock):
        """Should use 57 quantum dev edition firstrun template"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='57.0a2')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/developer/firstrun.html']

    @override_settings(DEV=True)
    def test_fx_firstrun_57_0(self, render_mock):
        """Should use 57 quantum firstrun template"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='57.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/firstrun/firstrun.html']

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
        assert template == ['firefox/tracking-protection-tour/index.html']

    @override_settings(DEV=True)
    def test_fx_tracking_protection_63_0_v0(self, render_mock):
        """Should use variation 0 template"""
        req = self.rf.get('/en-US/firefox/tracking-protection/start/?variation=0')
        self.view(req, version='62.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/tracking-protection-tour/variation-0.html']

    @override_settings(DEV=True)
    def test_fx_tracking_protection_63_0_v1(self, render_mock):
        """Should use variation 1 template"""
        req = self.rf.get('/en-US/firefox/tracking-protection/start/?variation=1')
        self.view(req, version='62.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/tracking-protection-tour/variation-1.html']

    @override_settings(DEV=True)
    def test_fx_tracking_protection_63_0_v2(self, render_mock):
        """Should use variation 2 template"""
        req = self.rf.get('/en-US/firefox/tracking-protection/start/?variation=2')
        self.view(req, version='62.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/tracking-protection-tour/variation-2.html']


@patch('bedrock.firefox.views.l10n_utils.render', return_value=HttpResponse())
class TestContentBlockingTour(TestCase):
    def setUp(self):
        self.view = fx_views.ContentBlockingTourView.as_view()
        self.rf = RequestFactory()

    @override_settings(DEV=True)
    def test_fx_content_blocking_65_0(self, render_mock):
        """Should use default content blocking tour template"""
        req = self.rf.get('/en-US/firefox/content-blocking/start/')
        self.view(req, version='65.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/content-blocking-tour/index.html']

    @override_settings(DEV=True)
    def test_fx_content_blocking_65_0_v2(self, render_mock):
        """Should use variation 2 template"""
        req = self.rf.get('/en-US/firefox/content-blocking/start/?variation=2')
        self.view(req, version='65.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/content-blocking-tour/variation-2.html']
