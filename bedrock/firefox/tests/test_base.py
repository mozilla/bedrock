# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from unittest.mock import Mock, call, patch

from django.core.cache import caches
from django.http import HttpResponse
from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_jinja.backend import Jinja2
from markupsafe import Markup
from pyquery import PyQuery as pq

from bedrock.base.urlresolvers import reverse
from bedrock.firefox import views as fx_views
from bedrock.firefox.firefox_details import FirefoxDesktop, firefox_desktop
from bedrock.mozorg.tests import TestCase

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")
PROD_DETAILS_DIR = os.path.join(TEST_DATA_DIR, "product_details_json")
GOOD_PLATS = {"Windows": {}, "OS X": {}, "Linux": {}}
jinja_env = Jinja2.get_default().env


class TestInstallerHelp(TestCase):
    def setUp(self):
        self.button_mock = Mock()
        self.patcher = patch.dict(jinja_env.globals, download_firefox=self.button_mock)
        self.patcher.start()
        self.view_name = "firefox.installer-help"
        with self.activate_locale("en-US"):
            self.url = reverse(self.view_name)

    def tearDown(self):
        self.patcher.stop()

    def test_buttons_use_lang(self):
        """
        The buttons should use the lang from the query parameter.
        """
        self.client.get(self.url, {"installer_lang": "fr"})
        self.button_mock.assert_has_calls(
            [
                call(
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale="fr",
                    platform="desktop",
                ),
                call(
                    "beta",
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale="fr",
                    platform="desktop",
                ),
                call(
                    "alpha",
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale="fr",
                    platform="desktop",
                ),
                call(
                    "nightly",
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale="fr",
                    platform="desktop",
                ),
            ]
        )

    def test_buttons_ignore_non_lang(self):
        """
        The buttons should ignore an invalid lang.
        """
        self.client.get(self.url, {"installer_lang": "not-a-locale"})
        self.button_mock.assert_has_calls(
            [
                call(
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale=None,
                    platform="desktop",
                ),
                call(
                    "beta",
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale=None,
                    platform="desktop",
                ),
                call(
                    "alpha",
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale=None,
                    platform="desktop",
                ),
                call(
                    "nightly",
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale=None,
                    platform="desktop",
                ),
            ]
        )

    def test_invalid_channel_specified(self):
        """
        All buttons should show when channel is invalid.
        """
        self.client.get(
            self.url,
            {
                "channel": "dude",
            },
        )
        self.button_mock.assert_has_calls(
            [
                call(
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale=None,
                    platform="desktop",
                ),
                call(
                    "beta",
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale=None,
                    platform="desktop",
                ),
                call(
                    "alpha",
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale=None,
                    platform="desktop",
                ),
                call(
                    "nightly",
                    alt_copy=Markup("Download Now"),
                    button_class="mzp-t-secondary mzp-t-md",
                    force_direct=True,
                    force_full_installer=True,
                    locale=None,
                    platform="desktop",
                ),
            ]
        )

    def test_one_button_when_channel_specified(self):
        """
        There should be only one button when the channel is given.
        """
        self.client.get(
            self.url,
            {
                "channel": "beta",
            },
        )
        self.button_mock.assert_called_once_with(
            "beta",
            alt_copy=Markup("Download Now"),
            button_class="mzp-t-md",
            force_direct=True,
            force_full_installer=True,
            locale=None,
            platform="desktop",
        )


class TestFirefoxAll(TestCase):
    pd_cache = caches["product-details"]

    def setUp(self):
        self.pd_cache.clear()
        self.firefox_desktop = FirefoxDesktop(json_dir=PROD_DETAILS_DIR)
        self.patcher = patch.object(fx_views, "firefox_desktop", self.firefox_desktop)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_all_step_1(self):
        resp = self.client.get(reverse("firefox.all"))
        doc = pq(resp.content)

        # Step 1 is active, steps 2,3,4 are disabled.
        assert len(doc(".t-step-disabled")) == 3
        # 5 desktop products, 4 mobile products.
        assert len(doc(".c-product-list > li")) == 9

    def test_all_step_2(self):
        resp = self.client.get(reverse("firefox.all_product", kwargs={"product_slug": "desktop-release"}))
        doc = pq(resp.content)

        # Step 1 is done, step 2 is active, steps 3,4 are disabled.
        assert doc(".c-steps > h2").eq(0).find(".c-step-choice").text() == "Firefox"
        assert len(doc(".t-step-disabled")) == 2
        # platforms for desktop-release, including Windows Store
        assert len(doc(".c-platform-list > li")) == 9

    def test_all_step_3(self):
        resp = self.client.get(reverse("firefox.all_platform", kwargs={"product_slug": "desktop-release", "platform": "win64"}))
        doc = pq(resp.content)

        # Step 1,2 is done, step 3 is active, step 4 are disabled.
        assert doc(".c-steps > h2").eq(0).find(".c-step-choice").text() == "Firefox"
        assert doc(".c-steps > h2").eq(1).find(".c-step-choice").text() == "Windows 64-bit"
        assert len(doc(".t-step-disabled")) == 1
        # first locale matches request.locale
        assert doc(".c-lang-list > li").eq(0).text() == "English (US) - English (US)"
        # number of locales equals the number of builds
        assert len(doc(".c-lang-list > li")) == len(firefox_desktop.get_filtered_full_builds("release"))

    def test_all_step_4(self):
        resp = self.client.get(reverse("firefox.all_locale", kwargs={"product_slug": "desktop-release", "platform": "win64", "locale": "en-US"}))
        doc = pq(resp.content)

        # Step 1,2,3 is done, step 4 is active, no more steps
        assert doc(".c-steps > h2").eq(0).find(".c-step-choice").text() == "Firefox"
        assert doc(".c-steps > h2").eq(1).find(".c-step-choice").text() == "Windows 64-bit"
        assert doc(".c-steps > h2").eq(2).find(".c-step-choice").text() == "English (US) - English (US)"
        assert len(doc(".t-step-disabled")) == 0
        # The download button should be present and correct.
        assert len(doc(".c-download-button")) == 1
        assert (
            doc(".c-download-button").attr("href")
            == list(filter(lambda b: b["locale"] == "en-US", firefox_desktop.get_filtered_full_builds("release")))[0]["platforms"]["win64"][
                "download_url"
            ]
        )


@patch("bedrock.firefox.views.l10n_utils.render", return_value=HttpResponse())
class TestWhatsNew(TestCase):
    def setUp(self):
        self.view = fx_views.WhatsnewView.as_view()
        self.rf = RequestFactory(HTTP_USER_AGENT="Firefox")

    # begin context variable tests

    @override_settings(DEV=True)
    @patch.object(fx_views, "ftl_file_is_active", lambda *x: True)
    def test_context_variables_whatsnew(self, render_mock):
        """Should pass the correct context variables"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="70.0")
        template = render_mock.call_args[0][1]
        ctx = render_mock.call_args[0][2]
        assert template == ["firefox/whatsnew/index.html"]
        assert ctx["version"] == "70.0"
        assert ctx["analytics_version"] == "70"
        assert ctx["entrypoint"] == "mozilla.org-whatsnew70"
        assert ctx["campaign"] == "whatsnew70"
        assert ctx["utm_params"] == (
            "utm_source=mozilla.org-whatsnew70&utm_medium=referral&utm_campaign=whatsnew70&entrypoint=mozilla.org-whatsnew70"
        )

    @override_settings(DEV=True)
    def test_context_variables_whatsnew_developer(self, render_mock):
        """Should pass the correct context variables for developer channel"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="72.0a2")
        template = render_mock.call_args[0][1]
        ctx = render_mock.call_args[0][2]
        assert template == ["firefox/developer/whatsnew.html"]
        assert ctx["version"] == "72.0a2"
        assert ctx["analytics_version"] == "72developer"
        assert ctx["entrypoint"] == "mozilla.org-whatsnew72developer"
        assert ctx["campaign"] == "whatsnew72developer"
        assert ctx["utm_params"] == (
            "utm_source=mozilla.org-whatsnew72developer&utm_medium=referral"
            "&utm_campaign=whatsnew72developer&entrypoint=mozilla.org-whatsnew72developer"
        )

    @override_settings(DEV=True)
    def test_context_variables_whatsnew_nightly(self, render_mock):
        """Should pass the correct context variables for nightly channel"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="100.0a1")
        template = render_mock.call_args[0][1]
        ctx = render_mock.call_args[0][2]
        assert template == ["firefox/nightly/whatsnew.html"]
        assert ctx["version"] == "100.0a1"
        assert ctx["analytics_version"] == "100nightly"
        assert ctx["entrypoint"] == "mozilla.org-whatsnew100nightly"
        assert ctx["campaign"] == "whatsnew100nightly"
        assert ctx["utm_params"] == (
            "utm_source=mozilla.org-whatsnew100nightly&utm_medium=referral&utm_campaign=whatsnew100nightly&entrypoint=mozilla.org-whatsnew100nightly"
        )

    # end context variable tests

    # begin nightly whatsnew tests

    @override_settings(DEV=True)
    def test_fx_nightly_68_0_a1_whatsnew(self, render_mock):
        """Should show nightly whatsnew template"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="68.0a1")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/nightly/whatsnew.html"]

    @override_settings(DEV=True)
    def test_fx_nightly_100_0_a1_whatsnew(self, render_mock):
        """Should show nightly whatsnew template"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="100.0a1")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/nightly/whatsnew.html"]

    # end nightly whatsnew tests

    # begin dev edition whatsnew tests

    @override_settings(DEV=True)
    def test_fx_dev_browser_35_0_a2_whatsnew(self, render_mock):
        """Should show default whatsnew template"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="35.0a2")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    @override_settings(DEV=True)
    def test_fx_dev_browser_57_0_a2_whatsnew(self, render_mock):
        """Should show dev browser 57 whatsnew template"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="57.0a2")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/developer/whatsnew.html"]

    @override_settings(DEV=True)
    @patch.dict(os.environ, SWITCH_FIREFOX_DEVELOPER_WHATSNEW_MDNPLUS="False")
    def test_fx_dev_browser_102_0_a2_whatsnew_off(self, render_mock):
        """Should show regular dev browser whatsnew template"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="102.0a2")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/developer/whatsnew.html"]

    @override_settings(DEV=True)
    @patch.dict(os.environ, SWITCH_FIREFOX_DEVELOPER_WHATSNEW_MDNPLUS="True")
    def test_fx_dev_browser_102_0_a2_whatsnew_mdnplus(self, render_mock):
        """Should show MDN Plus dev browser whatsnew template when switch is on"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="102.0a2")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/developer/whatsnew-mdnplus.html"]

    # end dev edition whatsnew tests

    # begin 126 beta whatsnew tests

    @override_settings(DEV=True)
    def test_fx_126_0_0beta_en_US(self, render_mock):
        """Should use whatsnew-fx126beta-en-US template for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="126.0beta")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126beta-en-US.html"]

    @override_settings(DEV=True)
    def test_fx_126_0_0beta_en_CA(self, render_mock):
        """Should use whatsnew-fx126beta-en-CA template for en-CA locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-CA"
        self.view(req, version="126.0beta")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126beta-en-CA.html"]

    @override_settings(DEV=True)
    def test_fx_126_0_0beta_de(self, render_mock):
        """Should use whatsnew-fx126beta-de template for de locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="126.0beta")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126beta-de.html"]

    @override_settings(DEV=True)
    def test_fx_126_0_0beta_pl(self, render_mock):
        """Should use default template for pl locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "pl"
        self.view(req, version="126.0beta")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    # end 126 beta whatsnew tests

    # begin 127 beta whatsnew tests

    @override_settings(DEV=True)
    def test_fx_127_0_0beta_en_US(self, render_mock):
        """Should use whatsnew-fx126beta-en-US template for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="127.0beta")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126beta-en-US.html"]

    @override_settings(DEV=True)
    def test_fx_127_0_0beta_en_CA(self, render_mock):
        """Should use whatsnew-fx126beta-en-CA template for en-CA locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-CA"
        self.view(req, version="127.0beta")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126beta-en-CA.html"]

    @override_settings(DEV=True)
    def test_fx_127_0_0beta_de(self, render_mock):
        """Should use whatsnew-fx126beta-de template for de locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="127.0beta")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126beta-de.html"]

    @override_settings(DEV=True)
    def test_fx_127_0_0beta_pl(self, render_mock):
        """Should use default template for pl locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "pl"
        self.view(req, version="127.0beta")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    # end 127 beta whatsnew tests

    @override_settings(DEV=True)
    def test_rv_prefix(self, render_mock):
        """Prefixed oldversion shouldn't impact version sniffing."""
        req = self.rf.get("/en-US/firefox/whatsnew/?oldversion=rv:10.0")
        self.view(req, version="54.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    @override_settings(DEV=True)
    @patch.object(fx_views, "ftl_file_is_active", lambda *x: True)
    def test_fx_default_whatsnew_sync(self, render_mock):
        """Should use sync template for 60.0"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="60.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    @override_settings(DEV=True)
    @patch.object(fx_views, "ftl_file_is_active", lambda *x: False)
    def test_fx_default_whatsnew_fallback(self, render_mock):
        """Should use standard template for 60.0 as fallback"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="60.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    @override_settings(DEV=True)
    @patch.object(fx_views, "ftl_file_is_active", lambda *x: True)
    def test_fx_default_whatsnew(self, render_mock):
        """Should use standard template for 59.0"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="59.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    # begin 125.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_125_0_0_en_us(self, render_mock):
        """Should use whatsnew-fx125-na template for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="125.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx125-na.html"]

    @override_settings(DEV=True)
    def test_fx_125_0_0_us_gb(self, render_mock):
        """Should use whatsnew-fx125-eu template for en-US locale in UK"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="GB")
        req.locale = "en-US"
        self.view(req, version="125.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx125-eu.html"]

    @override_settings(DEV=True)
    def test_fx_125_0_0_en_gb(self, render_mock):
        """Should use whatsnew-fx125-eu template for en-GB locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-GB"
        self.view(req, version="125.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx125-eu.html"]

    @override_settings(DEV=True)
    def test_fx_125_0_0_de(self, render_mock):
        """Should use whatsnew-fx125-eu template for de locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="125.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx125-eu.html"]

    @override_settings(DEV=True)
    def test_fx_125_0_0_fr(self, render_mock):
        """Should use whatsnew-fx125-eu template for fr locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "fr"
        self.view(req, version="125.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx125-eu.html"]

    @override_settings(DEV=True)
    def test_fx_125_0_0_pl(self, render_mock):
        """Should use whatsnew-fx125-eu template for pl locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "pl"
        self.view(req, version="125.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx125-eu.html"]

    # end 125.0 whatsnew tests

    # begin 126.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_126_0_0_en_us(self, render_mock):
        """Should use whatsnew-fx126-na template for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="126.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126-na.html"]

    @override_settings(DEV=True)
    def test_fx_126_0_0_en_ca(self, render_mock):
        """Should use whatsnew-fx126-na template for en-CA locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-CA"
        self.view(req, version="126.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126-na.html"]

    @override_settings(DEV=True)
    def test_fx_126_0_0_en_gb(self, render_mock):
        """Should use whatsnew-fx126-eu template for en-GB locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-GB"
        self.view(req, version="126.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126-eu.html"]

    @override_settings(DEV=True)
    def test_fx_126_0_0_us_gb(self, render_mock):
        """Should use whatsnew-fx126-eu template for en-US locale in GB"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="GB")
        req.locale = "en-US"
        self.view(req, version="126.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126-eu.html"]

    @override_settings(DEV=True)
    def test_fx_126_0_0_de(self, render_mock):
        """Should use whatsnew-fx126-eu template for de locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="126.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126-eu.html"]

    @override_settings(DEV=True)
    def test_fx_126_0_0_fr(self, render_mock):
        """Should use whatsnew-fx126-eu template for fr locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "fr"
        self.view(req, version="126.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126-eu.html"]

    @override_settings(DEV=True)
    def test_fx_126_0_0_es_es(self, render_mock):
        """Should use whatsnew-fx126-eu template for es-ES locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "es-ES"
        self.view(req, version="126.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126-eu.html"]

    @override_settings(DEV=True)
    def test_fx_126_0_0_it(self, render_mock):
        """Should use whatsnew-fx126-eu template for it locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "it"
        self.view(req, version="126.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126-eu.html"]

    @override_settings(DEV=True)
    def test_fx_126_0_0_pl(self, render_mock):
        """Should use whatsnew-fx126-eu template for pl locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "pl"
        self.view(req, version="126.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx126-eu.html"]

    # end 126.0 whatsnew tests

    # begin 127.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_127_0_0_en_us(self, render_mock):
        """Should use whatsnew-fx127-na template for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="127.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx127-na.html"]

    @override_settings(DEV=True)
    def test_fx_127_0_0_en_ca(self, render_mock):
        """Should use whatsnew-fx127-na template for en-CA locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-CA"
        self.view(req, version="127.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx127-na.html"]

    @override_settings(DEV=True)
    def test_fx_127_0_0_en_gb(self, render_mock):
        """Should use whatsnew-fx127-eu template for en-GB locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-GB"
        self.view(req, version="127.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx127-eu.html"]

    @override_settings(DEV=True)
    def test_fx_127_0_0_us_gb(self, render_mock):
        """Should use whatsnew-fx127-eu template for en-US locale in GB"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="GB")
        req.locale = "en-US"
        self.view(req, version="127.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx127-eu.html"]

    @override_settings(DEV=True)
    def test_fx_127_0_0_de(self, render_mock):
        """Should use whatsnew-fx127-eu template for de locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="127.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx127-eu.html"]

    @override_settings(DEV=True)
    def test_fx_127_0_0_fr(self, render_mock):
        """Should use whatsnew-fx127-eu template for fr locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "fr"
        self.view(req, version="127.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx127-eu.html"]

    @override_settings(DEV=True)
    def test_fx_127_0_0_es_es(self, render_mock):
        """Should use whatsnew-fx127-eu template for es-ES locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "es-ES"
        self.view(req, version="127.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx127-eu.html"]

    @override_settings(DEV=True)
    def test_fx_127_0_0_it(self, render_mock):
        """Should use whatsnew-fx127-eu template for it locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "it"
        self.view(req, version="127.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx127-eu.html"]

    @override_settings(DEV=True)
    def test_fx_127_0_0_pl(self, render_mock):
        """Should use whatsnew-fx127-eu template for pl locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "pl"
        self.view(req, version="127.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx127-eu.html"]

    # end 127.0 whatsnew tests

    # begin 128.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_128_0_0_en_us(self, render_mock):
        """Should use whatsnew-fx128-na template for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-na.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_en_ca(self, render_mock):
        """Should use whatsnew-fx128-na template for en-CA locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-CA"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-na.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_en_gb_v1(self, render_mock):
        """Should use whatsnew-fx128-eu-addons template for en-GB locale and v=1"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-GB"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-addons.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_fr_v1(self, render_mock):
        """Should use whatsnew-fx128-eu-addons template for fr locale and v=1"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "fr"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-addons.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_de_v1(self, render_mock):
        """Should use whatsnew-fx128-eu-addons template for de locale and v=1"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-addons.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_es_es_v1(self, render_mock):
        """Should use whatsnew-fx128-eu-addons template for es-ES locale and v=1"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "es-ES"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-addons.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_it_v1(self, render_mock):
        """Should use whatsnew-fx128-eu-addons template for it locale and v=1"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "it"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-addons.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_pl_v1(self, render_mock):
        """Should use whatsnew-fx128-eu-addons template for pl locale and v=1"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "pl"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-addons.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_en_gb_v2(self, render_mock):
        """Should use whatsnew-fx128-eu-donate template for en-GB locale and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2")
        req.locale = "en-GB"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-donate.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_fr_v2(self, render_mock):
        """Should use whatsnew-fx128-eu-donate template for fr locale and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2")
        req.locale = "fr"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-donate.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_de_v2(self, render_mock):
        """Should use whatsnew-fx128-eu-donate template for de locale and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2")
        req.locale = "de"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-donate.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_en_gb_v3(self, render_mock):
        """Should use whatsnew-fx128-eu-donate template for en-GB locale and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3")
        req.locale = "en-GB"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-donate.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_fr_v3(self, render_mock):
        """Should use whatsnew-fx128-eu-donate template for fr locale and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3")
        req.locale = "fr"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-donate.html"]

    @override_settings(DEV=True)
    def test_fx_128_0_0_de_v3(self, render_mock):
        """Should use whatsnew-fx128-eu-donate template for de locale and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3")
        req.locale = "de"
        self.view(req, version="128.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx128-eu-donate.html"]

    # end 128.0 whatsnew tests

    # begin 129.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_129_0_0_en_us(self, render_mock):
        """Should use whatsnew-fx129-na template for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="129.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx129-na.html"]

    @override_settings(DEV=True)
    def test_fx_129_0_0_en_ca(self, render_mock):
        """Should use whatsnew-fx129-na template for en-CA locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-CA"
        self.view(req, version="129.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx129-na.html"]

    @override_settings(DEV=True)
    def test_fx_129_0_0_en_gb(self, render_mock):
        """Should use whatsnew-fx129-eu template for en-GB locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-GB"
        self.view(req, version="129.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx129-eu.html"]

    @override_settings(DEV=True)
    def test_fx_129_0_0_fr(self, render_mock):
        """Should use whatsnew-fx129-eu template for fr locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "fr"
        self.view(req, version="129.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx129-eu.html"]

    @override_settings(DEV=True)
    def test_fx_129_0_0_de(self, render_mock):
        """Should use whatsnew-fx129-eu template for de locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="129.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx129-eu.html"]

    @override_settings(DEV=True)
    def test_fx_129_0_0_es_es(self, render_mock):
        """Should use whatsnew-fx129-eu template for es-ES locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "es-ES"
        self.view(req, version="129.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx129-eu.html"]

    @override_settings(DEV=True)
    def test_fx_129_0_0_it(self, render_mock):
        """Should use whatsnew-fx129-eu template for it locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "it"
        self.view(req, version="129.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx129-eu.html"]

    @override_settings(DEV=True)
    def test_fx_129_0_0_pl(self, render_mock):
        """Should use whatsnew-fx129-eu template for pl locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "pl"
        self.view(req, version="129.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx129-eu.html"]

    # end 129.0 whatsnew tests


@patch("bedrock.firefox.views.l10n_utils.render", return_value=HttpResponse())
class TestFirstRun(TestCase):
    def setUp(self):
        self.view = fx_views.FirstrunView.as_view()
        self.rf = RequestFactory()

    @override_settings(DEV=True)
    def test_fx_firstrun_release_channel(self, render_mock):
        """Should redirect to /firefox/new/ page"""
        req = self.rf.get("/en-US/firefox/firstrun/")
        resp = self.view(req, version="40.0")
        assert resp.status_code == 301
        assert resp["location"].endswith("/firefox/new/?reason=outdated")

    @override_settings(DEV=True)
    def test_fx_firstrun_dev_edition_old(self, render_mock):
        """Should redirect to the /firefox/developer/ page"""
        req = self.rf.get("/en-US/firefox/firstrun/")
        resp = self.view(req, version="56.0a2")
        assert resp.status_code == 301
        assert resp["location"].endswith("/firefox/developer/")

    @override_settings(DEV=True)
    def test_fx_firstrun_57_0(self, render_mock):
        """Should use 57 quantum firstrun template"""
        req = self.rf.get("/en-US/firefox/firstrun/")
        resp = self.view(req, version="57.0")
        assert resp.status_code == 301
        assert resp["location"].endswith("/firefox/new/?reason=outdated")
