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
from jinja2 import Markup

from bedrock.base.urlresolvers import reverse
from bedrock.firefox import views as fx_views
from bedrock.firefox.firefox_details import FirefoxDesktop
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
            call(alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale='fr'),
            call('beta', alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale='fr'),
            call('alpha', alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale='fr', platform='desktop'),
            call('nightly', alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale='fr', platform='desktop'),
        ])

    def test_buttons_ignore_non_lang(self):
        """
        The buttons should ignore an invalid lang.
        """
        self.client.get(self.url, {
            'installer_lang': 'not-a-locale'
        })
        self.button_mock.assert_has_calls([
            call(alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale=None),
            call('beta', alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale=None),
            call('alpha', alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale=None, platform='desktop'),
            call('nightly', alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale=None, platform='desktop'),
        ])

    def test_invalid_channel_specified(self):
        """
        All buttons should show when channel is invalid.
        """
        self.client.get(self.url, {
            'channel': 'dude',
        })
        self.button_mock.assert_has_calls([
            call(alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale=None),
            call('beta', alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale=None),
            call('alpha', alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale=None, platform='desktop'),
            call('nightly', alt_copy=Markup('Download Now'), button_class='mzp-t-secondary mzp-t-md', force_direct=True,
                 force_full_installer=True, locale=None, platform='desktop'),
        ])

    def test_one_button_when_channel_specified(self):
        """
        There should be only one button when the channel is given.
        """
        self.client.get(self.url, {
            'channel': 'beta',
        })
        self.button_mock.assert_called_once_with('beta',
                                                 alt_copy=Markup('Download Now'), button_class='mzp-t-md',
                                                 force_direct=True,
                                                 force_full_installer=True,
                                                 locale=None)


class TestFirefoxAll(TestCase):
    pd_cache = caches['product-details']

    def setUp(self):
        self.pd_cache.clear()
        self.firefox_desktop = FirefoxDesktop(json_dir=PROD_DETAILS_DIR)
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
        assert len(doc('.c-all-downloads-build')) == 9

        desktop_release_builds = len(self.firefox_desktop.get_filtered_full_builds('release'))
        assert len(doc('.c-locale-list[data-product="desktop_release"] > li')) == desktop_release_builds
        assert len(doc('.c-locale-list[data-product="desktop_release"] > li[data-language="en-US"] > ul > li > a')) == 8

        desktop_beta_builds = len(self.firefox_desktop.get_filtered_full_builds('beta'))
        assert len(doc('.c-locale-list[data-product="desktop_beta"] > li')) == desktop_beta_builds
        assert len(doc('.c-locale-list[data-product="desktop_beta"] > li[data-language="en-US"] > ul > li > a')) == 8

        desktop_developer_builds = len(self.firefox_desktop.get_filtered_full_builds('alpha'))
        assert len(doc('.c-locale-list[data-product="desktop_developer"] > li')) == desktop_developer_builds
        assert len(doc('.c-locale-list[data-product="desktop_developer"] > li[data-language="en-US"] > ul > li > a')) == 8

        desktop_nightly_builds = len(self.firefox_desktop.get_filtered_full_builds('nightly'))
        assert len(doc('.c-locale-list[data-product="desktop_nightly"] > li')) == desktop_nightly_builds
        assert len(doc('.c-locale-list[data-product="desktop_nightly"] > li[data-language="en-US"] > ul > li > a')) == 8

        desktop_esr_builds = len(self.firefox_desktop.get_filtered_full_builds('esr'))
        assert len(doc('.c-locale-list[data-product="desktop_esr"] > li')) == desktop_esr_builds
        assert len(doc('.c-locale-list[data-product="desktop_esr"] > li[data-language="en-US"] > ul > li > a')) == 8

        android_release_builds = 1
        assert len(doc('.c-locale-list[data-product="android_release"] > li')) == android_release_builds
        assert len(doc('.c-locale-list[data-product="android_release"] > li[data-language="multi"] > ul > li > a')) == 2

        android_beta_builds = 1
        assert len(doc('.c-locale-list[data-product="android_beta"] > li')) == android_beta_builds
        assert len(doc('.c-locale-list[data-product="android_beta"] > li[data-language="multi"] > ul > li > a')) == 1

        android_nightly_builds = 1
        assert len(doc('.c-locale-list[data-product="android_nightly"] > li')) == android_nightly_builds
        assert len(doc('.c-locale-list[data-product="android_nightly"] > li[data-language="multi"] > ul > li > a')) == 1

        ios_release_builds = 1
        assert len(doc('.c-locale-list[data-product="ios_release"] > li')) == ios_release_builds
        assert len(doc('.c-locale-list[data-product="ios_release"] > li[data-language="multi"] > ul > li > a')) == 2

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

    # begin context variable tests

    @override_settings(DEV=True)
    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_context_variables_whatsnew(self, render_mock):
        """Should pass the correct context variables"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='70.0')
        template = render_mock.call_args[0][1]
        ctx = render_mock.call_args[0][2]
        assert template == ['firefox/whatsnew/index-account.html']
        assert ctx['version'] == '70.0'
        assert ctx['analytics_version'] == '70'
        assert ctx['entrypoint'] == 'mozilla.org-whatsnew70'
        assert ctx['campaign'] == 'whatsnew70'
        assert ctx['utm_params'] == ('utm_source=mozilla.org-whatsnew70&utm_medium=referral'
                                     '&utm_campaign=whatsnew70&entrypoint=mozilla.org-whatsnew70')

    @override_settings(DEV=True)
    def test_context_variables_whatsnew_developer(self, render_mock):
        """Should pass the correct context variables for developer channel"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='72.0a2')
        template = render_mock.call_args[0][1]
        ctx = render_mock.call_args[0][2]
        assert template == ['firefox/developer/whatsnew.html']
        assert ctx['version'] == '72.0a2'
        assert ctx['analytics_version'] == '72developer'
        assert ctx['entrypoint'] == 'mozilla.org-whatsnew72developer'
        assert ctx['campaign'] == 'whatsnew72developer'
        assert ctx['utm_params'] == ('utm_source=mozilla.org-whatsnew72developer&utm_medium=referral'
                                     '&utm_campaign=whatsnew72developer&entrypoint=mozilla.org-whatsnew72developer')

    @override_settings(DEV=True)
    def test_context_variables_whatsnew_nightly(self, render_mock):
        """Should pass the correct context variables for nightly channel"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='72.0a1')
        template = render_mock.call_args[0][1]
        ctx = render_mock.call_args[0][2]
        assert template == ['firefox/nightly/whatsnew.html']
        assert ctx['version'] == '72.0a1'
        assert ctx['analytics_version'] == '72nightly'
        assert ctx['entrypoint'] == 'mozilla.org-whatsnew72nightly'
        assert ctx['campaign'] == 'whatsnew72nightly'
        assert ctx['utm_params'] == ('utm_source=mozilla.org-whatsnew72nightly&utm_medium=referral'
                                     '&utm_campaign=whatsnew72nightly&entrypoint=mozilla.org-whatsnew72nightly')

    # end context variable tests

    # begin nightly whatsnew tests

    @override_settings(DEV=True)
    def test_fx_nightly_68_0_a1_whatsnew(self, render_mock):
        """Should show nightly whatsnew template"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='68.0a1')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/nightly/whatsnew.html']

    # end nightly whatsnew tests

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
    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_default_whatsnew_sync(self, render_mock):
        """Should use sync template for 60.0"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='60.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index-account.html']

    @override_settings(DEV=True)
    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: False)
    def test_fx_default_whatsnew_fallback(self, render_mock):
        """Should use standard template for 60.0 as fallback"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='60.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index.html']

    @override_settings(DEV=True)
    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_default_whatsnew(self, render_mock):
        """Should use standard template for 59.0"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='59.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index.html']

    # begin 79.0 whatsnew tests

    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_79_0_0(self, render_mock):
        """Should use whatsnew-fx79 template for 79.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='79.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx79.html']

    # end 79.0 whatsnew tests

    # begin 80.0 whatsnew tests

    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_80_0_0(self, render_mock):
        """Should use whatsnew-fx80 template for 80.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='80.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx80.html']

    # end 80.0 whatsnew tests

    # begin 81.0 whatsnew tests

    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_81_0_0(self, render_mock):
        """Should use whatsnew-fx81 template for 81.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='81.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx81.html']

    # end 81.0 whatsnew tests

    # begin 82.0 whatsnew tests

    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_82_0_0(self, render_mock):
        """Should use whatsnew-fx82 template for 82.0 in English"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='82.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx82.html']

    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_82_0_0_locale(self, render_mock):
        """Should use standard whatsnew template for 82.0 in other locales"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'es-ES'
        self.view(req, version='82.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index-account.html']

    def test_fx_82_0_0_china(self, render_mock):
        """Should use standard whatsnew template in China for en-US locale"""
        self.view = fx_views.WhatsNewChinaView.as_view()
        req = self.rf.get('/firefox/whatsnew/china/')
        req.locale = 'en-US'
        self.view(req, version='82.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index-account.html']

    # end 82.0 whatsnew tests

    # begin 83.0 whatsnew tests

    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_83_0_0(self, render_mock):
        """Should use whatsnew-fx83 template for 83.0 in English"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='83.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx83-en.html']

    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_83_0_0_locale(self, render_mock):
        """Should use standard whatsnew template for 83.0 in other locales"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'es-ES'
        self.view(req, version='83.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index-account.html']

    def test_fx_83_0_0_german(self, render_mock):
        """Should use standard whatsnew template in German for de locale"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'de'
        self.view(req, version='83.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx83-de.html']

    # end 83.0 whatsnew tests

    # begin 84.0 whatsnew tests

    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_84_0_0(self, render_mock):
        """Should use whatsnew-fx84 template for 84.0 in English"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='84.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx84.html']

    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_84_0_0_locale(self, render_mock):
        """Should use standard whatsnew template for 84.0 in other locales"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'es-ES'
        self.view(req, version='84.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index-account.html']

    def test_fx_84_0_0_china(self, render_mock):
        """Should use standard whatsnew template in China for en-US locale"""
        self.view = fx_views.WhatsNewChinaView.as_view()
        req = self.rf.get('/firefox/whatsnew/china/')
        req.locale = 'en-US'
        self.view(req, version='84.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index-account.html']

    # end 84.0 whatsnew tests

    # begin 85.0 whatsnew tests

    def test_fx_85_0_0(self, render_mock):
        """Should use whatsnew-fx85 template for 85.0 in English"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='85.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx85.html']

    def test_fx_85_0_0_de(self, render_mock):
        """Should use whatsnew-mobile-de template for 85.0 in German"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'de'
        self.view(req, version='85.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-mobile-de.html']

    def test_fx_85_0_0_locale(self, render_mock):
        """Should use standard whatsnew template for 85.0 in other locales"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'es-ES'
        self.view(req, version='85.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index-account.html']

    def test_fx_85_0_0_china(self, render_mock):
        """Should use standard whatsnew template in China for en-US locale"""
        self.view = fx_views.WhatsNewChinaView.as_view()
        req = self.rf.get('/firefox/whatsnew/china/')
        req.locale = 'en-US'
        self.view(req, version='85.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index-account.html']

    # end 85.0 whatsnew tests

    # begin 86.0 whatsnew tests

    def test_fx_86_0_0_en(self, render_mock):
        """Should use whatsnew-fx86 template for 86.0 in English"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'en-US'
        self.view(req, version='86.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx86-en.html']

    def test_fx_86_0_0_de(self, render_mock):
        """Should use whatsnew-mobile-qrcode-de template for 86.0 in German"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'de'
        self.view(req, version='86.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-mobile-qrcode-de.html']

    def test_fx_86_0_0_fr(self, render_mock):
        """Should use whatsnew-fx81 template for 86.0 in French"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'fr'
        self.view(req, version='86.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx81.html']

    def test_fx_86_0_0_locale(self, render_mock):
        """Should use standard whatsnew template for 86.0 in other locales"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'es-ES'
        self.view(req, version='86.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/index-account.html']

    # end 86.0 whatsnew tests

    # begin 87.0 whatsnew tests

    def test_fx_87_0_0_de(self, render_mock):
        """Should use VPN waitlist signup template for 87.0 in German"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'de'
        self.view(req, version='87.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx87-de.html']

    def test_fx_87_0_0_fr(self, render_mock):
        """Should use VPN waitlist signup template for 87.0 in French"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'fr'
        self.view(req, version='87.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx87-fr.html']

    # end 87.0 whatsnew tests


@patch('bedrock.firefox.views.l10n_utils.render', return_value=HttpResponse())
class TestWhatsNewFirefoxLite(TestCase):
    def setUp(self):
        self.view = fx_views.WhatsNewFirefoxLiteView.as_view()
        self.rf = RequestFactory(HTTP_USER_AGENT='Firefox')

    @patch.dict(os.environ, SWITCH_FIREFOX_LITE_WHATSNEW='True')
    def test_fx_lite_africa(self, render_mock):
        """Should use firefox-lite template for Africa for en-US locale"""
        req = self.rf.get('/firefox/whatsnew/africa/')
        req.locale = 'en-US'
        self.view(req, version='79.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/firefox-lite.html']

    @patch.dict(os.environ, SWITCH_FIREFOX_LITE_WHATSNEW='True')
    def test_fx_lite_india(self, render_mock):
        """Should use firefox-lite template for India for en-US locale"""
        req = self.rf.get('/firefox/whatsnew/india/')
        req.locale = 'en-US'
        self.view(req, version='79.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/firefox-lite.html']

    @patch.object(fx_views, 'ftl_file_is_active', lambda *x: True)
    def test_fx_whatsnew(self, render_mock):
        """Should use regular whatsnew templates for other locales"""
        req = self.rf.get('/firefox/whatsnew/india/')
        req.locale = 'de'
        self.view(req, version='79.0')
        template = render_mock.call_args[0][1]
        assert template == ['firefox/whatsnew/whatsnew-fx79.html']


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
