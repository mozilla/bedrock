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

    def test_all_builds_results(self):
        """
        The unified page should display builds for all products
        """
        resp = self.client.get(reverse('firefox.all'))
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
    def test_fx_72beta_whatsnew(self, render_mock):
        """Should show Fx72beta whatsnew template"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='72.0beta')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/beta/whatsnew-fx72-en.html']

    @override_settings(DEV=True)
    def test_fx_oldbeta_whatsnew(self, render_mock):
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
        """Should use default whatsnew template for 70.0 for other locales"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'es-ES'
        self.view(req, version='70.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index.html']

    def test_fx_70_0_2(self, render_mock):
        """Should use default whatsnew template for 70.0.2 when updating from 70.0"""
        req = self.rf.get('/firefox/whatsnew/?oldversion=70.0')
        req.locale = 'en-US'
        self.view(req, version='70.0.2')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index.html']

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


