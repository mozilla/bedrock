# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from unittest.mock import Mock, call, patch

from django.http import HttpResponse
from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_jinja.backend import Jinja2
from markupsafe import Markup
from waffle.testutils import override_switch

from bedrock.base.urlresolvers import reverse
from bedrock.firefox import views as fx_views
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
    @override_switch("FIREFOX_DEVELOPER_WHATSNEW_MDNPLUS", active=False)
    def test_fx_dev_browser_102_0_a2_whatsnew_off(self, render_mock):
        """Should show regular dev browser whatsnew template"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="102.0a2")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/developer/whatsnew.html"]

    @override_settings(DEV=True)
    @override_switch("FIREFOX_DEVELOPER_WHATSNEW_MDNPLUS", active=True)
    def test_fx_dev_browser_102_0_a2_whatsnew_mdnplus(self, render_mock):
        """Should show MDN Plus dev browser whatsnew template when switch is on"""
        req = self.rf.get("/en-US/firefox/whatsnew/")
        self.view(req, version="102.0a2")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/developer/whatsnew-mdnplus.html"]

    # end dev edition whatsnew tests

    # begin 135 beta whatsnew tests

    @override_settings(DEV=True)
    def test_fx_135_0_0beta_en_US(self, render_mock):
        """Should use whatsnew-fx135beta template for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="135.0beta")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx135beta.html"]

    @override_settings(DEV=True)
    def test_fx_135_0_0beta_pl(self, render_mock):
        """Should use default template for pl locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "pl"
        self.view(req, version="135.0beta")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    # end 135 beta whatsnew tests

    # begin 135 na whatsnew tests

    @override_settings(DEV=True)
    def test_fx_135_0_0_en_US(self, render_mock):
        """Should use whatsnew-fx135-na template for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="135.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx135-na.html"]

    @override_settings(DEV=True)
    def test_fx_135_0_0_en_CA(self, render_mock):
        """Should use whatsnew-fx135-na template for en-CA locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-CA"
        self.view(req, version="135.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx135-na.html"]

    # end 135 na whatsnew tests

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

    # begin 130.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_130_0_0_en_us(self, render_mock):
        """Should use whatsnew-fx130 template for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="130.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx130.html"]

    @override_settings(DEV=True)
    def test_fx_130_0_0_en_ca(self, render_mock):
        """Should use whatsnew-fx130 template for en-CA locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-CA"
        self.view(req, version="130.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx130.html"]

    @override_settings(DEV=True)
    def test_fx_130_0_0_en_gb(self, render_mock):
        """Should use whatsnew-fx130 template for en-GB locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-GB"
        self.view(req, version="130.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx130.html"]

    @override_settings(DEV=True)
    def test_fx_130_0_0_de(self, render_mock):
        """Should use whatsnew-fx130 template for de locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="130.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx130.html"]

    @override_settings(DEV=True)
    def test_fx_130_0_0_fr(self, render_mock):
        """Should use whatsnew-fx130 template for fr locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "fr"
        self.view(req, version="130.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx130.html"]

    @override_settings(DEV=True)
    def test_fx_130_0_0_es_es(self, render_mock):
        """Should use whatsnew-fx130 template for es-ES locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "es-ES"
        self.view(req, version="130.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx130.html"]

    @override_settings(DEV=True)
    def test_fx_130_0_0_it(self, render_mock):
        """Should use whatsnew-fx130 template for it locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "it"
        self.view(req, version="130.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx130.html"]

    @override_settings(DEV=True)
    def test_fx_130_0_0_pl(self, render_mock):
        """Should use whatsnew-fx130 template for pl locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "pl"
        self.view(req, version="130.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx130.html"]

    @override_settings(DEV=True)
    def test_fx_130_0_0_en_us_v1(self, render_mock):
        """Should use default WNP template for en-US locale when branch=experiment-wnp-130-tabs and variant=v1"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-130-tabs&variant=v1")
        req.locale = "en-US"
        self.view(req, version="130.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    # end 130.0 whatsnew tests

    # begin 131.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_131_0_0_en_us_no_experiment(self, render_mock):
        """Should use WNP 131 template for en-US when no experiment params are present"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-na.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_en_us_v1(self, render_mock):
        """Should use default WNP template for en-US locale when branch=experiment-wnp-131-tabs and variant=v1"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v1")
        req.locale = "en-US"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_en_us_v2(self, render_mock):
        """Should use whatsnew-fx131-na.html template for en-US locale when branch=experiment-wnp-131-tabs and variant=v2"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v2")
        req.locale = "en-US"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-na.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_en_ca_no_experiment(self, render_mock):
        """Should use WNP 131 template for en-CA when no experiment params are present"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-na.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_en_ca_v1(self, render_mock):
        """Should use default WNP template for en-CA locale when branch=experiment-wnp-131-tabs and variant=v1"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v1")
        req.locale = "en-CA"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_en_ca_v2(self, render_mock):
        """Should use whatsnew-fx131-na.html template for en-CA locale when branch=experiment-wnp-131-tabs and variant=v2"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v2")
        req.locale = "en-CA"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-na.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_en_gb_no_experiment(self, render_mock):
        """Should use WNP 131 template for en-GB when no experiment params are present"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-GB"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-eu.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_en_gb_v1(self, render_mock):
        """Should use default WNP template for en-GB locale when branch=experiment-wnp-131-tabs and variant=v1"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v1")
        req.locale = "en-GB"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_en_gb_v3(self, render_mock):
        """Should use whatsnew-fx131-eu.html template for en-GB locale when branch=experiment-wnp-131-tabs and variant=v3"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v3")
        req.locale = "en-GB"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-eu.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_en_gb_v4(self, render_mock):
        """Should use whatsnew-fx131-eu.html template for en-GB locale when branch=experiment-wnp-131-tabs and variant=v4"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v4")
        req.locale = "en-GB"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-eu.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_de_no_experiment(self, render_mock):
        """Should use WNP 131 template for de when no experiment params are present"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-eu.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_de_v1(self, render_mock):
        """Should use default WNP template for de locale when branch=experiment-wnp-131-tabs and variant=v1"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v1")
        req.locale = "de"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_de_v3(self, render_mock):
        """Should use whatsnew-fx131-eu.html template for de locale when branch=experiment-wnp-131-tabs and variant=v3"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v3")
        req.locale = "de"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-eu.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_de_v4(self, render_mock):
        """Should use whatsnew-fx131-eu.html template for de locale when branch=experiment-wnp-131-tabs and variant=v4"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v4")
        req.locale = "de"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-eu.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_fr_no_experiment(self, render_mock):
        """Should use WNP 131 template for fr when no experiment params are present"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "fr"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-eu.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_fr_v1(self, render_mock):
        """Should use default WNP template for de locale when branch=experiment-wnp-131-tabs and variant=v1"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v1")
        req.locale = "fr"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_fr_v3(self, render_mock):
        """Should use whatsnew-fx131-eu.html template for de locale when branch=experiment-wnp-131-tabs and variant=v3"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v3")
        req.locale = "fr"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-eu.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_fr_v4(self, render_mock):
        """Should use whatsnew-fx131-eu.html template for de locale when branch=experiment-wnp-131-tabs and variant=v4"""
        req = self.rf.get("/firefox/whatsnew/?branch=experiment-wnp-131-tabs&variant=v4")
        req.locale = "fr"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx131-eu.html"]

    @override_settings(DEV=True)
    def test_fx_131_0_0_other_locales(self, render_mock):
        """Should use default WNP template for locales that are not part of the experiment"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "es-ES"
        self.view(req, version="131.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    # end 131.0 whatsnew tests

    # begin 132.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_132_0_0_en_ca(self, render_mock):
        """Should use whatsnew-fx132-na.html template for en-CA locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-CA"
        self.view(req, version="132.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx132-na.html"]

    @override_settings(DEV=True)
    def test_fx_132_0_0_en_us(self, render_mock):
        """Should use whatsnew-fx132-na.html template for for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="132.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx132-na.html"]

    @override_settings(DEV=True)
    def test_fx_132_0_0_en_gb(self, render_mock):
        """Should use whatsnew-fx132-na.html template for en-GB locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-GB"
        self.view(req, version="132.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx132-na.html"]

    @override_settings(DEV=True)
    def test_fx_132_0_0_de(self, render_mock):
        """Should use whatsnew-fx132-eu.html template for de locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="132.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx132-eu.html"]

    @override_settings(DEV=True)
    def test_fx_132_0_0_fr(self, render_mock):
        """Should use whatsnew-fx132-eu.html template for fr locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "fr"
        self.view(req, version="132.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx132-eu.html"]

    @override_settings(DEV=True)
    def test_fx_132_0_0_other_locales(self, render_mock):
        """Should use default WNP template for other locales"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "es-ES"
        self.view(req, version="132.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    # end 132.0 whatsnew tests

    # begin 133.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_el_gr(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for el locale in GR"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="GR")
        req.locale = "el"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_en_ca_au(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for en-CA locale in AU"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="AU")
        req.locale = "en-CA"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_en_gb_au(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for en-GB locale in AU"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="AU")
        req.locale = "en-GB"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_en_us_au(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for en-US locale in AU"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="AU")
        req.locale = "en-US"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_es_es_co(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for es-ES locale in CO"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="CO")
        req.locale = "es-ES"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_es_cl_cl(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for es-CL locale in CL"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="CL")
        req.locale = "es-CL"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_es_mx_mx(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for es-MX locale in MX"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="MX")
        req.locale = "es-MX"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_fr_sn(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for fr locale in SN"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="SN")
        req.locale = "fr"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_id_id(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for id locale in ID"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="ID")
        req.locale = "id"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_ko_kr(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for ko locale in KR"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="KR")
        req.locale = "ko"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_pt_br_br(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for pt-BR locale in BR"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="BR")
        req.locale = "pt-BR"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_tr_tr(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for tr locale in TR"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="TR")
        req.locale = "tr"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_uk_ua(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for uk locale in UA"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="UA")
        req.locale = "uk"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_vi_vn(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for vi locale in VN"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="VN")
        req.locale = "vi"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_vpn_zh_tw_tw(self, render_mock):
        """Should use whatsnew-fx133-vpn.html template for zh-TW locale in TW"""
        req = self.rf.get("/firefox/whatsnew/", HTTP_CF_IPCOUNTRY="TW")
        req.locale = "zh-TW"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-vpn.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_fr_fr_v1(self, render_mock):
        """Should use whatsnew-fx133-eu-newsletter.html template for fr locale in FR and v=1"""
        req = self.rf.get("/firefox/whatsnew/?v=1", HTTP_CF_IPCOUNTRY="FR")
        req.locale = "fr"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-eu-newsletter.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_fr_fr_v2(self, render_mock):
        """Should use whatsnew-fx133-donation-eu.html template for fr locale in FR and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="FR")
        req.locale = "fr"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation-eu.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_fr_fr_v3(self, render_mock):
        """Should use whatsnew-fx133-donation-eu.html template for fr locale in FR and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="FR")
        req.locale = "fr"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation-eu.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_de_de_v1(self, render_mock):
        """Should use whatsnew-fx133-eu-newsletter.html template for de locale in DE and v=1"""
        req = self.rf.get("/firefox/whatsnew/?v=1", HTTP_CF_IPCOUNTRY="DE")
        req.locale = "de"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-eu-newsletter.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_de_de_v2(self, render_mock):
        """Should use whatsnew-fx133-donation-eu.html template for de locale in DE and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="DE")
        req.locale = "de"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation-eu.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_de_de_v3(self, render_mock):
        """Should use whatsnew-fx133-donation-eu.html template for de locale in DE and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="DE")
        req.locale = "de"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation-eu.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_gb_gb_v1(self, render_mock):
        """Should use whatsnew-fx133-eu-newsletter.html template for de locale in GB and v=1"""
        req = self.rf.get("/firefox/whatsnew/?v=1", HTTP_CF_IPCOUNTRY="GB")
        req.locale = "en-GB"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-eu-newsletter.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_gb_gb_v2(self, render_mock):
        """Should use whatsnew-fx133-donation-eu.html template for en_GB locale in GB and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="GB")
        req.locale = "en-GB"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation-eu.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_gb_gb_v3(self, render_mock):
        """Should use whatsnew-fx133-donation-eu.html template for en_GB locale in GB and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="GB")
        req.locale = "en-GB"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation-eu.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_us_us_v1(self, render_mock):
        """Should use whatsnew-fx133-na-fakespot.html template for en_US locale in US and v=1"""
        req = self.rf.get("/firefox/whatsnew/?v=1", HTTP_CF_IPCOUNTRY="US")
        req.locale = "en-US"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-na-fakespot.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_us_us_v2(self, render_mock):
        """Should use whatsnew-fx133-donation-na.html template for en_US locale in US and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="US")
        req.locale = "en-US"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation-na.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_us_us_v3(self, render_mock):
        """Should use whatsnew-fx133-donation-na.html template for en_US locale in US and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="US")
        req.locale = "en-US"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation-na.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_ca_ca_v1(self, render_mock):
        """Should use firefox/whatsnew/whatsnew-fx133-na-mobile.html template for en_CA locale in CA and v=1"""
        req = self.rf.get("/firefox/whatsnew/?v=1", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "en-CA"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-na-mobile.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_ca_ca_v2(self, render_mock):
        """Should use whatsnew-fx133-donation-na.html template for en_CA locale in CA and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "en-CA"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation-na.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_ca_ca_v3(self, render_mock):
        """Should use whatsnew-fx133-donation-na.html template for en_CA locale in CA and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "en-CA"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation-na.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_fr_ca_v2(self, render_mock):
        """Should use whatsnew-fx133-donation.html template for fr locale in CA and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "fr"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_fr_ca_v3(self, render_mock):
        """Should use whatsnew-fx133-donatio.html template for fr locale in CA and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "fr"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_de_ca_v2(self, render_mock):
        """Should use whatsnew-fx133-donation.html template for de locale in CA and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "de"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_de_ca_v3(self, render_mock):
        """Should use whatsnew-fx133-donatio.html template for de locale in CA and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "de"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_it_ca_v2(self, render_mock):
        """Should use whatsnew-fx133-donation.html template for it locale in CA and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "it"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_it_ca_v3(self, render_mock):
        """Should use whatsnew-fx133-donatio.html template for it locale in CA and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "it"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_pl_ca_v2(self, render_mock):
        """Should use whatsnew-fx133-donation.html template for pl locale in CA and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "pl"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_pl_ca_v3(self, render_mock):
        """Should use whatsnew-fx133-donatio.html template for pl locale in CA and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "pl"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_es_es_ca_v2(self, render_mock):
        """Should use whatsnew-fx133-donation.html template for es-ES locale in CA and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "es-ES"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_es_es_ca_v3(self, render_mock):
        """Should use whatsnew-fx133-donatio.html template for es-ES locale in CA and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "es-ES"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_gb_ca_v2(self, render_mock):
        """Should use whatsnew-fx133-donation.html template for en-GB locale in CA and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "en-GB"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_gb_ca_v3(self, render_mock):
        """Should use whatsnew-fx133-donatio.html template for en-GB locale in CA and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "en-GB"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_us_fr_v2(self, render_mock):
        """Should use whatsnew-fx133-donation.html template for en-US locale in FR and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="FR")
        req.locale = "en-US"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_us_fr_v3(self, render_mock):
        """Should use whatsnew-fx133-donatio.html template for en-US locale in FR and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="FR")
        req.locale = "en-US"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_ca_fr_v2(self, render_mock):
        """Should use whatsnew-fx133-donation.html template for en-CA locale in FR and v=2"""
        req = self.rf.get("/firefox/whatsnew/?v=2", HTTP_CF_IPCOUNTRY="FR")
        req.locale = "en-CA"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    @override_settings(DEV=True)
    def test_fx_133_0_0_newsletter_en_ca_fr_v3(self, render_mock):
        """Should use whatsnew-fx133-donatio.html template for en-CA locale in FR and v=3"""
        req = self.rf.get("/firefox/whatsnew/?v=3", HTTP_CF_IPCOUNTRY="FR")
        req.locale = "en-CA"
        self.view(req, version="133.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx133-donation.html"]

    # end 133.0 whatsnew tests

    # begin 134.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_134_0_0_en_us(self, render_mock):
        """Should use whatsnew-fx134-us.html template for en-US"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="134.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx134-us.html"]

    @override_settings(DEV=True)
    def test_fx_134_0_0_en_ca(self, render_mock):
        """Should use whatsnew-fx134-ca.html template for en-CA"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-CA"
        self.view(req, version="134.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx134-ca.html"]

    @override_settings(DEV=True)
    def test_fx_134_0_0_en_gb(self, render_mock):
        """Should use whatsnew-fx134-gb.html template for en-GB"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-GB"
        self.view(req, version="134.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx134-gb.html"]

    @override_settings(DEV=True)
    def test_fx_134_0_0_de(self, render_mock):
        """Should use whatsnew-fx134-de.html template for de"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="134.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx134-de.html"]

    @override_settings(DEV=True)
    def test_fx_134_0_0_fr(self, render_mock):
        """Should use whatsnew-fx134-fr.html template for fr"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "fr"
        self.view(req, version="134.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx134-fr.html"]

    @override_settings(DEV=True)
    def test_fx_134_0_0_es_es(self, render_mock):
        """Should use default WNP template for other locales"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "es-ES"
        self.view(req, version="134.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    # end 134.0 whatsnew tests

    # begin 135.0 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_135_0_0_fr(self, render_mock):
        """Should use whatsnew-fx135-eu.html template for fr locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "fr"
        self.view(req, version="135.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx135-eu.html"]

    @override_settings(DEV=True)
    def test_fx_135_0_0_de(self, render_mock):
        """Should use whatsnew-fx135-eu.html template for de locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="135.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx135-eu.html"]

    @override_settings(DEV=True)
    def test_fx_135_0_0_en_gb(self, render_mock):
        """Should use whatsnew-fx135-eu.html template for en-GB locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-GB"
        self.view(req, version="135.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx135-eu.html"]

    @override_settings(DEV=True)
    def test_fx_135_0_0_es_es(self, render_mock):
        """Should use default WNP template for other locales"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "es-ES"
        self.view(req, version="135.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/index.html"]

    # end 135.0 whatsnew tests

    # begin 136 whatsnew tests

    @override_settings(DEV=True)
    def test_fx_136_0_0_en_US(self, render_mock):
        """Should use whatsnew-fx136-na-pip template for en-US locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-US"
        self.view(req, version="136.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx136-na-pip.html"]

    @override_settings(DEV=True)
    def test_fx_136_0_0_en_CA(self, render_mock):
        """Should use whatsnew-fx136-na-pip template for en-CA locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-CA"
        self.view(req, version="136.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx136-na-pip.html"]

    def test_fx_136_0_0_de(self, render_mock):
        """Should use whatsnew-fx136-eu-pip template for de locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "de"
        self.view(req, version="136.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx136-eu-pip.html"]

    def test_fx_136_0_0_fr(self, render_mock):
        """Should use whatsnew-fx136-eu-pip template for fr locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "fr"
        self.view(req, version="136.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx136-eu-pip.html"]

    def test_fx_136_0_0_en_gb(self, render_mock):
        """Should use whatsnew-fx136-eu-pip template for en-GB locale"""
        req = self.rf.get("/firefox/whatsnew/")
        req.locale = "en-GB"
        self.view(req, version="136.0")
        template = render_mock.call_args[0][1]
        assert template == ["firefox/whatsnew/whatsnew-fx136-eu-pip.html"]

    # end 136.0 whatsnew tests


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
