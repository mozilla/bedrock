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
from mock import ANY, call, Mock, patch
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
        eq_(len(doc('.build-table')), 2)
        eq_(len(doc('.not-found.hide')), 2)

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
        Android x64 builds are only available in multi and en-US locales.
        """
        resp = self.client.get(self._get_url('android'))
        doc = pq(resp.content)
        eq_(len(doc('tr#multi a')), 2)
        eq_(len(doc('tr#multi .android-x86')), 1)
        eq_(len(doc('tr#en-US a')), 2)
        eq_(len(doc('tr#en-US .android-x86')), 1)
        eq_(len(doc('tr#fr a')), 1)
        eq_(len(doc('tr#fr .android-x86')), 0)

    def test_404(self):
        """
        Firefox for iOS and Firefox Aurora for Android don't have the /all/ page.
        Also, Firefox for Android doesn't have the ESR channel.
        """
        resp = self.client.get(self._get_url('ios'))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self._get_url('android', 'aurora'))
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(self._get_url('android', 'organizations'))
        self.assertEqual(resp.status_code, 404)


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
        render_mock.assert_called_once_with(req, ['firefox/australis/whatsnew.html'], ANY)

    @override_settings(DEV=True)
    def test_fx_dev_browser_35_0_a2_whatsnew(self, render_mock):
        """Should show dev browser whatsnew template"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='35.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/dev-whatsnew.html'])

    # begin 42.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_42_0(self, render_mock):
        """Should use tracking protection whatsnew template for 42.0"""
        req = self.rf.get('/en-US/firefox/whatsnew/')
        self.view(req, version='42.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew_42/whatsnew.html'])

    # end 42.0 whatsnew tests

    @override_settings(DEV=True)
    def test_older_whatsnew(self, render_mock):
        """Should show default whatsnew template for 38.0 and below"""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=34.0')
        self.view(req, version='38.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew.html'])

    @override_settings(DEV=True)
    def test_rv_prefix(self, render_mock):
        """Prefixed oldversion shouldn't impact version sniffing."""
        req = self.rf.get('/en-US/firefox/whatsnew/?oldversion=rv:10.0')
        self.view(req, version='36.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/whatsnew.html'])

    # begin zh-TW 49.0 whatsnew tests

    @override_settings(DEV=True)
    def test_zh_TW_fx_49_0(self, render_mock):
        """Should use custom zh-TW template for zh-TW on 49.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'zh-TW'
        self.view(req, version='49.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew-zh-TW-49.html'])

    @override_settings(DEV=True)
    def test_zh_TW_fx_not_49_0(self, render_mock):
        """Should use tracking protection whatsnew template for zh-TW not on 49.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'zh-TW'
        self.view(req, version='49.0.1')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew_42/whatsnew.html'])

    @override_settings(DEV=True)
    def test_not_zh_TW_fx_49_0(self, render_mock):
        """Should use tracking protection whatsnew template for non-zh-TW on 49.0"""
        req = self.rf.get('/firefox/whatsnew/')
        req.locale = 'es-ES'
        self.view(req, version='49.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/whatsnew_42/whatsnew.html'])

    # end 42.0 whatsnew tests


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
            ['firefox/australis/firstrun.html'], ANY)

    @override_settings(DEV=True)
    def test_fx_australis_29(self, render_mock):
        """Should use old firstrun template"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='29.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/firstrun.html'])

    @override_settings(DEV=True)
    def test_fx_dev_browser(self, render_mock):
        """Should use dev browser firstrun template"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='35.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/dev-firstrun.html'])

    @override_settings(DEV=True)
    def test_fx_dev_browser_34_0_a2(self, render_mock):
        """Should use old firstrun template for older aurora"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='34.0a2')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/firstrun.html'])

    @override_settings(DEV=True)
    def test_fx_firstrun_38_0_5(self, render_mock):
        """Should use fx38.0.5 firstrun template for 38.0.5"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='38.0.5')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/australis/fx38_0_5/firstrun.html'])

    @override_settings(DEV=True)
    @patch('bedrock.mozorg.templatetags.misc.switch', Mock(return_value=True))
    def test_fx_firstrun_40_0(self, render_mock):
        """Should use horizon firstrun template for 40.0"""
        req = self.rf.get('/en-US/firefox/firstrun/')
        self.view(req, version='40.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/firstrun-horizon.html'])

    @override_settings(DEV=True)
    @patch('bedrock.mozorg.templatetags.misc.switch', Mock(return_value=True))
    def test_fx_firstrun_40_0_invalid_variation(self, render_mock):
        """
        Should use horizon firstrun template if an invalid variation is specified.
        """
        req = self.rf.get('/en-US/firefox/firstrun/?v=8')
        self.view(req, version='46.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/firstrun-horizon.html'])

    @override_settings(DEV=True)
    @patch('bedrock.mozorg.templatetags.misc.switch', Mock(return_value=True))
    def test_fx_firstrun_40_0_space_variant_non_enUS(self, render_mock):
        """
        Should use horizon firstrun template for non en-US 40.0+ with
        ?v=[1,2,3,4,5,6] query param
        """
        req = self.rf.get('/firefox/firstrun/?v=2')
        req.locale = 'de'
        self.view(req, version='46.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/firstrun-horizon.html'])

        req = self.rf.get('/firefox/firstrun/?v=5')
        req.locale = 'de'
        self.view(req, version='46.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/firstrun-horizon.html'])

    # ravioli funnelcake tests
    @override_settings(DEV=True)
    def test_ravioli_funnelcake(self, render_mock):
        """Should use ravioli template for f=90"""
        req = self.rf.get('/firefox/firstrun/?f=90')
        self.view(req, version='49.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/ravioli.html'])

    @override_settings(DEV=True)
    def test_ravioli_other_funnelcake(self, render_mock):
        """Should use firstrun horizon template for non-ravioli funnelcakes"""
        req = self.rf.get('/firefox/firstrun/?f=89')
        self.view(req, version='49.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/firstrun-horizon.html'])

    @override_settings(DEV=True)
    def test_ravioli_other_locales(self, render_mock):
        """Should use firstrun horizon template for non en-US locales"""
        req = self.rf.get('/firefox/firstrun/?f=90')
        req.locale = 'de'
        self.view(req, version='49.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/firstrun-horizon.html'])


@patch.object(fx_views.FirstrunLearnMoreView, 'redirect_to', none_mock)
@patch('bedrock.firefox.views.l10n_utils.render', return_value=HttpResponse())
class TestFirstRunLearnMore(TestCase):
    def setUp(self):
        self.view = fx_views.FirstrunLearnMoreView.as_view()
        self.rf = RequestFactory()

    @override_settings(DEV=True)
    def test_default_template(self, render_mock):
        """Should use default learnmore template"""
        req = self.rf.get('/firefox/firstrun/learnmore')
        self.view(req, version='45.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/learnmore/learnmore.html'])

    @override_settings(DEV=True)
    def test_yahoo_funnelcake_64_template(self, render_mock):
        """Should use yahoo search template for f=64"""
        req = self.rf.get('/firefox/firstrun/learnmore?f=64')
        self.view(req, version='45.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/learnmore/yahoo-search.html'])

    @override_settings(DEV=True)
    def test_yahoo_funnelcake_65_template(self, render_mock):
        """Should use yahoo search template for f=65"""
        req = self.rf.get('/firefox/firstrun/learnmore?f=65')
        self.view(req, version='45.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/learnmore/yahoo-search.html'])

    @override_settings(DEV=True)
    def test_yahoo_funnelcake_other_locales_template(self, render_mock):
        """Should use default learnmore template for non en-US locales"""
        req = self.rf.get('/firefox/firstrun/learnmore?f=64')
        req.locale = 'de'
        self.view(req, version='45.0')
        template = render_mock.call_args[0][1]
        eq_(template, ['firefox/firstrun/learnmore/learnmore.html'])


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
