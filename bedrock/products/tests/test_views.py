# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.conf import settings
from django.http import HttpResponse
from django.test import override_settings
from django.test.client import RequestFactory

import pytest
from waffle.testutils import override_switch

from bedrock.mozorg.tests import TestCase
from bedrock.products import views


@pytest.mark.parametrize("country_code", settings.VPN_COUNTRY_CODES)
@override_settings(DEV=False)
def test_vpn_available(country_code):
    """Should return True for country codes where VPN is available"""
    req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY=country_code)
    req.locale = "en-US"
    assert views.vpn_available(req) is True


@pytest.mark.django_db
@pytest.mark.parametrize("country_code", settings.VPN_COUNTRY_CODES + settings.VPN_MOBILE_SUB_COUNTRY_CODES)
@override_settings(DEV=False)
def test_vpn_available_switch_active(country_code):
    """Should return True for VPN_COUNTRY_CODES plus VPN_MOBILE_SUB_COUNTRY_CODES countries"""
    req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY=country_code)
    req.locale = "en-US"
    assert views.vpn_available(req) is True


@pytest.mark.parametrize("country_code", settings.VPN_EXCLUDED_COUNTRY_CODES)
@override_settings(DEV=False)
def test_vpn_excluded_country_codes(country_code):
    """Should return False for country codes where VPN is excluded from availability"""
    req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY=country_code)
    req.locale = "en-US"
    assert views.vpn_available(req) is False


@pytest.mark.parametrize("country_code", settings.VPN_BLOCK_DOWNLOAD_COUNTRY_CODES)
@override_settings(DEV=False)
def test_vpn_blocked_download_country_codes(country_code):
    """Should return False for country codes where VPN downloads are also blocked"""
    req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY=country_code)
    req.locale = "en-US"
    assert views.vpn_available(req) is False


@pytest.mark.django_db
@pytest.mark.parametrize("country_code", settings.VPN_MOBILE_SUB_COUNTRY_CODES)
@override_settings(DEV=False)
def test_vpn_available_mobile_sub_only_switch_active(country_code):
    """Should return True for VPN_MOBILE_SUB_COUNTRY_CODES country codes"""
    req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY=country_code)
    req.locale = "en-US"
    assert views.vpn_available_mobile_sub_only(req) is True


@pytest.mark.django_db
@pytest.mark.parametrize("country_code", settings.VPN_MOBILE_SUB_ANDROID_ONLY_COUNTRY_CODES)
@override_settings(DEV=False)
def test_vpn_available_android_sub_only_switch_active(country_code):
    """Should return True for VPN_MOBILE_SUB_ANDROID_ONLY_COUNTRY_CODES country codes"""
    req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY=country_code)
    req.locale = "en-US"
    assert views.vpn_available_android_sub_only(req) is True


@patch("bedrock.products.views.l10n_utils.render", return_value=HttpResponse())
class TestVPNLandingPage(TestCase):
    def test_vpn_landing_page_template_us(self, render_mock):
        req = RequestFactory().get("/products/vpn/")
        req.locale = "en-US"
        view = views.vpn_landing_page
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "products/vpn/landing-refresh.html"

    def test_vpn_landing_page_template_gb(self, render_mock):
        req = RequestFactory().get("/products/vpn/")
        req.locale = "en-GB"
        view = views.vpn_landing_page
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "products/vpn/landing-refresh.html"

    def test_vpn_landing_page_template_de(self, render_mock):
        req = RequestFactory().get("/products/vpn/")
        req.locale = "de"
        view = views.vpn_landing_page
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "products/vpn/landing-refresh.html"

    @override_settings(DEV=False)
    def test_vpn_landing_page_geo_available(self, render_mock):
        req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY="de")
        req.locale = "en-US"
        view = views.vpn_landing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertTrue(ctx["vpn_available"])

    @override_settings(DEV=False)
    def test_vpn_landing_page_geo_not_available(self, render_mock):
        req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY="cn")
        req.locale = "en-US"
        view = views.vpn_landing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertFalse(ctx["vpn_available"])

    @override_settings(DEV=False)
    @override_switch("VPN_AFFILIATE_ATTRIBUTION", active=True)
    def test_vpn_landing_page_geo_available_affiliate_flow_enabled(self, render_mock):
        req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY="us")
        req.locale = "en-US"
        view = views.vpn_landing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertTrue(ctx["vpn_available"])
        self.assertTrue(ctx["vpn_affiliate_attribution_enabled"])

    @override_settings(DEV=False)
    @override_switch("VPN_AFFILIATE_ATTRIBUTION", active=False)
    def test_vpn_landing_page_geo_available_affiliate_flow_disabled(self, render_mock):
        req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY="us")
        req.locale = "en-US"
        view = views.vpn_landing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertTrue(ctx["vpn_available"])
        self.assertFalse(ctx["vpn_affiliate_attribution_enabled"])

    @override_settings(DEV=False)
    @override_switch("VPN_AFFILIATE_ATTRIBUTION", active=True)
    def test_vpn_landing_page_geo_not_available_affiliate_flow_enabled(self, render_mock):
        req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY="cn")
        req.locale = "en-US"
        view = views.vpn_landing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertFalse(ctx["vpn_available"])
        self.assertFalse(ctx["vpn_affiliate_attribution_enabled"])

    @override_settings(DEV=False)
    @override_switch("VPN_AFFILIATE_ATTRIBUTION", active=True)
    def test_vpn_landing_page_geo_available_affiliate_not_supported_in_country(self, render_mock):
        req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY="it")
        req.locale = "en-US"
        view = views.vpn_landing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertTrue(ctx["vpn_available"])
        self.assertFalse(ctx["vpn_affiliate_attribution_enabled"])


@patch("bedrock.products.views.l10n_utils.render", return_value=HttpResponse())
class TestVPNPricingPage(TestCase):
    def test_vpn_pricing_page_template_us(self, render_mock):
        req = RequestFactory().get("/products/vpn/pricing/")
        req.locale = "en-US"
        view = views.vpn_pricing_page
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "products/vpn/pricing-refresh.html"

    @override_settings(DEV=False)
    def test_vpn_pricing_page_geo_available(self, render_mock):
        req = RequestFactory().get("/products/vpn/pricing/", HTTP_CF_IPCOUNTRY="de")
        req.locale = "en-US"
        view = views.vpn_pricing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertTrue(ctx["vpn_available"])

    @override_settings(DEV=False)
    def test_vpn_pricing_page_geo_not_available(self, render_mock):
        req = RequestFactory().get("/products/vpn/pricing/", HTTP_CF_IPCOUNTRY="cn")
        req.locale = "en-US"
        view = views.vpn_pricing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertFalse(ctx["vpn_available"])

    @override_settings(DEV=False)
    @override_switch("VPN_AFFILIATE_ATTRIBUTION", active=True)
    def test_vpn_pricing_page_geo_available_affiliate_flow_enabled(self, render_mock):
        req = RequestFactory().get("/products/vpn/pricing/", HTTP_CF_IPCOUNTRY="us")
        req.locale = "en-US"
        view = views.vpn_pricing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertTrue(ctx["vpn_available"])
        self.assertTrue(ctx["vpn_affiliate_attribution_enabled"])

    @override_settings(DEV=False)
    @override_switch("VPN_AFFILIATE_ATTRIBUTION", active=False)
    def test_vpn_pricing_page_geo_available_affiliate_flow_disabled(self, render_mock):
        req = RequestFactory().get("/products/vpn/pricing/", HTTP_CF_IPCOUNTRY="us")
        req.locale = "en-US"
        view = views.vpn_pricing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertTrue(ctx["vpn_available"])
        self.assertFalse(ctx["vpn_affiliate_attribution_enabled"])

    @override_settings(DEV=False)
    @override_switch("VPN_AFFILIATE_ATTRIBUTION", active=True)
    def test_vpn_pricing_page_geo_not_available_affiliate_flow_enabled(self, render_mock):
        req = RequestFactory().get("/products/vpn/pricing/", HTTP_CF_IPCOUNTRY="cn")
        req.locale = "en-US"
        view = views.vpn_pricing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertFalse(ctx["vpn_available"])
        self.assertFalse(ctx["vpn_affiliate_attribution_enabled"])

    @override_settings(DEV=False)
    @override_switch("VPN_AFFILIATE_ATTRIBUTION", active=True)
    def test_vpn_pricing_page_geo_available_affiliate_not_supported_in_country(self, render_mock):
        req = RequestFactory().get("/products/vpn/pricing/", HTTP_CF_IPCOUNTRY="it")
        req.locale = "en-US"
        view = views.vpn_pricing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertTrue(ctx["vpn_available"])
        self.assertFalse(ctx["vpn_affiliate_attribution_enabled"])


@override_settings(VPN_ENDPOINT="https://vpn.mozilla.org/")
@patch("bedrock.products.views.l10n_utils.render", return_value=HttpResponse())
class TestVPNDownloadPage(TestCase):
    @override_settings(DEV=False)
    def test_vpn_downoad_page_links(self, render_mock):
        req = RequestFactory().get("/products/vpn/download/")
        req.locale = "en-US"
        view = views.vpn_download_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertEqual(ctx["windows_download_url"], "https://vpn.mozilla.org/r/vpn/download/windows")
        self.assertEqual(ctx["mac_download_url"], "https://vpn.mozilla.org/r/vpn/download/mac")
        self.assertEqual(ctx["linux_download_url"], "https://vpn.mozilla.org/r/vpn/download/linux")


@patch("bedrock.products.views.l10n_utils.render", return_value=HttpResponse())
class TestMonitorScanWaitlistPage(TestCase):
    @override_settings(DEV=False)
    def test_monitor_scan_waitlist_template(self, render_mock):
        req = RequestFactory().get("/products/monitor/waitlist-scan/")
        req.locale = "en-US"
        view = views.monitor_waitlist_scan_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertEqual(ctx["newsletter_id"], "monitor-waitlist")
        template = render_mock.call_args[0][1]
        assert template == "products/monitor/waitlist/scan.html"

    @override_settings(DEV=False)
    def test_monitor_plus_waitlist_template(self, render_mock):
        req = RequestFactory().get("/products/monitor/waitlist-plus/")
        req.locale = "en-US"
        view = views.monitor_waitlist_plus_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertEqual(ctx["newsletter_id"], "monitor-waitlist")
        template = render_mock.call_args[0][1]
        assert template == "products/monitor/waitlist/plus.html"
