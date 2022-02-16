# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import os
from unittest.mock import ANY, patch
from urllib.parse import parse_qs

from django.http import HttpResponse
from django.test import override_settings
from django.test.client import RequestFactory

import querystringsafe_base64
from pyquery import PyQuery as pq

from bedrock.firefox import views
from bedrock.mozorg.tests import TestCase


@override_settings(
    STUB_ATTRIBUTION_HMAC_KEY="achievers",
    STUB_ATTRIBUTION_RATE=1,
    STUB_ATTRIBUTION_MAX_LEN=600,
)
class TestStubAttributionCode(TestCase):
    def _get_request(self, params):
        rf = RequestFactory()
        return rf.get(
            "/",
            params,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            HTTP_ACCEPT="application/json",
        )

    def test_not_ajax_request(self):
        req = RequestFactory().get("/", {"source": "malibu"})
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 400)
        assert "cache-control" not in resp
        data = json.loads(resp.content)
        self.assertEqual(data["error"], "Resource only available via XHR")

    def test_no_valid_param_names(self):
        final_params = {
            "source": "www.mozilla.org",
            "medium": "(none)",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "(not set)",
            "visit_id": "(not set)",
        }
        req = self._get_request({"dude": "abides"})
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp["cache-control"] == "max-age=300"
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data["attribution_code"].encode()).decode())
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data["attribution_sig"],
            "135b2245f6b70978bc8142a91521facdb31d70a1bfbdefdc1bd1dee92ce21a22",
        )

    def test_no_valid_param_data(self):
        params = {
            "utm_source": "br@ndt",
            "utm_medium": "ae<t>her",
            "experiment": "dfb</p>s",
            "variation": "ef&bvcv",
            "visit_id": "14</p>4538.1610<t>957",
        }
        final_params = {
            "source": "www.mozilla.org",
            "medium": "(none)",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "(not set)",
            "visit_id": "(not set)",
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp["cache-control"] == "max-age=300"
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data["attribution_code"].encode()).decode())
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data["attribution_sig"],
            "135b2245f6b70978bc8142a91521facdb31d70a1bfbdefdc1bd1dee92ce21a22",
        )

    def test_some_valid_param_data(self):
        params = {"utm_source": "brandt", "utm_content": "ae<t>her"}
        final_params = {
            "source": "brandt",
            "medium": "(direct)",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "(not set)",
            "visit_id": "(not set)",
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp["cache-control"] == "max-age=300"
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data["attribution_code"].encode()).decode())
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data["attribution_sig"],
            "b53097f17741b75cdd5b737d3c8ba03349a6093148adeada2ee69adf4fe87322",
        )

    def test_campaign_data_too_long(self):
        """If the code is too long then the utm_campaign value should be truncated"""
        params = {
            "utm_source": "brandt",
            "utm_medium": "aether",
            "utm_content": "A144_A000_0000000",
            "utm_campaign": "The%7cDude%7cabides%7cI%7cdont%7cknow%7cabout%7cyou%7cbut%7cI%7ctake%7ccomfort%7cin%7cthat" * 6,
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "chrome",
            "visit_id": "1456954538.1610960957",
        }
        final_params = {
            "source": "brandt",
            "medium": "aether",
            "campaign": "The|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in"
            "|thatThe|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in|thatThe"
            "|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in|thatThe|Dude|abides"
            "|I|dont|know|about|you|but|I|take|comfort|in|thatThe|Dude|abides|I|dont|know"
            "|about|you|but|I|take|comfort|in|thatT_",
            "content": "A144_A000_0000000",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "chrome",
            "visit_id": "1456954538.1610960957",
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp["cache-control"] == "max-age=300"
        data = json.loads(resp.content)
        # will it blend?
        code = querystringsafe_base64.decode(data["attribution_code"].encode()).decode()
        assert len(code) <= 600
        attrs = parse_qs(code)
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data["attribution_sig"],
            "3c1611db912c51a96418eb7806fbaf1400b8d05fbf6ee4f2f1fb3c0ba74a89f4",
        )

    def test_other_data_too_long_not_campaign(self):
        """If the code is too long but not utm_campaign return error"""
        params = {
            "utm_source": "brandt",
            "utm_campaign": "dude",
            "utm_content": "A144_A000_0000000",
            "utm_medium": "The%7cDude%7cabides%7cI%7cdont%7cknow%7cabout%7cyou%7cbut%7cI%7ctake%7ccomfort%7cin%7cthat" * 6,
        }
        final_params = {"error": "Invalid code"}
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 400)
        assert resp["cache-control"] == "max-age=300"
        data = json.loads(resp.content)
        self.assertDictEqual(data, final_params)

    def test_returns_valid_data(self):
        params = {
            "utm_source": "brandt",
            "utm_medium": "aether",
            "experiment": "firefox-new",
            "variation": "1",
            "ua": "chrome",
            "visit_id": "1456954538.1610960957",
        }
        final_params = {
            "source": "brandt",
            "medium": "aether",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "firefox-new",
            "variation": "1",
            "ua": "chrome",
            "visit_id": "1456954538.1610960957",
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp["cache-control"] == "max-age=300"
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data["attribution_code"].encode()).decode())
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data["attribution_sig"],
            "b2dc555b2914fdec9f9a1247d244520392e4f888961a6fb57a74a1cdf041261f",
        )

    def test_handles_referrer(self):
        params = {"utm_source": "brandt", "referrer": "https://duckduckgo.com/privacy"}
        final_params = {
            "source": "brandt",
            "medium": "(direct)",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "(not set)",
            "visit_id": "(not set)",
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp["cache-control"] == "max-age=300"
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data["attribution_code"].encode()).decode())
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data["attribution_sig"],
            "b53097f17741b75cdd5b737d3c8ba03349a6093148adeada2ee69adf4fe87322",
        )

    def test_handles_referrer_no_source(self):
        params = {
            "referrer": "https://example.com:5000/searchin",
            "utm_medium": "aether",
        }
        final_params = {
            "source": "example.com:5000",
            "medium": "referral",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "(not set)",
            "visit_id": "(not set)",
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp["cache-control"] == "max-age=300"
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data["attribution_code"].encode()).decode())
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data["attribution_sig"],
            "d075cbcbae3bcef5bda3650a259863151586e3a4709d53886ab3cc83a6963d00",
        )

    def test_handles_referrer_utf8(self):
        """Should ignore non-ascii domain names.

        We were getting exceptions when the view was trying to base64 encode
        non-ascii domain names in the referrer. The allowed list for bouncer
        doesn't include any such domains anyway, so we should just ignore them.
        """
        params = {"referrer": "http://youtubê.com/sorry/"}
        final_params = {
            "source": "www.mozilla.org",
            "medium": "(none)",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "(not set)",
            "visit_id": "(not set)",
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp["cache-control"] == "max-age=300"
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data["attribution_code"].encode()).decode())
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data["attribution_sig"],
            "135b2245f6b70978bc8142a91521facdb31d70a1bfbdefdc1bd1dee92ce21a22",
        )

    @override_settings(STUB_ATTRIBUTION_RATE=0.2)
    def test_rate_limit(self):
        params = {"utm_source": "brandt", "utm_medium": "aether"}
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp["cache-control"] == "max-age=300"

    @override_settings(STUB_ATTRIBUTION_RATE=0)
    def test_rate_limit_disabled(self):
        params = {"utm_source": "brandt", "utm_medium": "aether"}
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 429)
        assert resp["cache-control"] == "max-age=300"

    @override_settings(STUB_ATTRIBUTION_HMAC_KEY="")
    def test_no_hmac_key_set(self):
        params = {"utm_source": "brandt", "utm_medium": "aether"}
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 403)
        assert resp["cache-control"] == "max-age=300"


class TestSendToDeviceView(TestCase):
    def setUp(self):
        patcher = patch("bedrock.firefox.views.basket.subscribe")
        self.mock_subscribe = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch("bedrock.firefox.views.basket.request")
        self.mock_send_sms = patcher.start()
        self.addCleanup(patcher.stop)

    def _request(self, data, expected_status=200, locale="en-US"):
        req = RequestFactory().post("/", data)
        req.locale = locale
        resp = views.send_to_device_ajax(req)
        assert resp.status_code == expected_status
        return json.loads(resp.content)

    def test_phone_or_email_required(self):
        resp_data = self._request({"platform": "android"})
        assert not resp_data["success"]
        assert "s2d-email" in resp_data["errors"]
        assert not self.mock_send_sms.called
        assert not self.mock_subscribe.called

    def test_send_android_email(self):
        resp_data = self._request(
            {
                "platform": "android",
                "s2d-email": "dude@example.com",
                "source-url": "https://nihilism.info",
            }
        )
        assert resp_data["success"]
        self.mock_subscribe.assert_called_with(
            "dude@example.com",
            views.SEND_TO_DEVICE_MESSAGE_SETS["default"]["email"]["android"],
            source_url="https://nihilism.info",
            lang="en-US",
        )

    def test_send_android_email_basket_error(self):
        self.mock_subscribe.side_effect = views.basket.BasketException
        resp_data = self._request(
            {
                "platform": "android",
                "s2d-email": "dude@example.com",
                "source-url": "https://nihilism.info",
            },
            400,
        )
        assert not resp_data["success"]
        assert "system" in resp_data["errors"]

    def test_send_android_bad_email(self):
        resp_data = self._request(
            {
                "platform": "android",
                "s2d-email": "@example.com",
                "source-url": "https://nihilism.info",
            }
        )
        assert not resp_data["success"]
        assert "email" in resp_data["errors"]
        assert not self.mock_subscribe.called

    # an invalid value for 'message-set' should revert to 'default' message set
    def test_invalid_message_set(self):
        resp_data = self._request(
            {
                "platform": "ios",
                "s2d-email": "dude@example.com",
                "message-set": "the-dude-is-not-in",
            }
        )
        assert resp_data["success"]
        self.mock_subscribe.assert_called_with(
            "dude@example.com",
            views.SEND_TO_DEVICE_MESSAGE_SETS["default"]["email"]["ios"],
            source_url=None,
            lang="en-US",
        )

    # /firefox/android/ embedded widget (bug 1221328)
    def test_android_embedded_email(self):
        resp_data = self._request(
            {
                "platform": "android",
                "s2d-email": "dude@example.com",
                "message-set": "fx-android",
            }
        )
        assert resp_data["success"]
        self.mock_subscribe.assert_called_with(
            "dude@example.com",
            views.SEND_TO_DEVICE_MESSAGE_SETS["fx-android"]["email"]["android"],
            source_url=None,
            lang="en-US",
        )

    # /firefox/mobile-download/desktop
    def test_fx_mobile_download_desktop_email(self):
        resp_data = self._request(
            {
                "s2d-email": "dude@example.com",
                "message-set": "fx-mobile-download-desktop",
            }
        )
        assert resp_data["success"]
        self.mock_subscribe.assert_called_with(
            "dude@example.com",
            views.SEND_TO_DEVICE_MESSAGE_SETS["fx-mobile-download-desktop"]["email"]["all"],
            source_url=None,
            lang="en-US",
        )


@override_settings(DEV=False)
@patch("bedrock.firefox.views.l10n_utils.render", return_value=HttpResponse())
class TestFirefoxNew(TestCase):
    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_download_template(self, render_mock):
        req = RequestFactory().get("/firefox/new/")
        req.locale = "en-US"
        view = views.NewView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/desktop/download.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_thanks_template(self, render_mock):
        req = RequestFactory().get("/firefox/download/thanks/")
        req.locale = "en-US"
        view = views.DownloadThanksView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/desktop/thanks.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: False)
    def test_download_basic_template(self, render_mock):
        req = RequestFactory().get("/firefox/new/")
        req.locale = "de"
        view = views.NewView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/basic/base_download.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: False)
    def test_thanks_basic_template(self, render_mock):
        req = RequestFactory().get("/firefox/download/thanks/")
        req.locale = "de"
        view = views.DownloadThanksView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/basic/thanks.html"]

    def test_thanks_redirect(self, render_mock):
        req = RequestFactory().get("/firefox/new/?scene=2&dude=abides")
        req.locale = "en-US"
        view = views.NewView.as_view()
        resp = view(req)
        assert resp.status_code == 301
        assert resp["location"].endswith("/firefox/download/thanks/?scene=2&dude=abides")

    # begin /thanks?s=direct URL - issue 10520

    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_thanks_desktop_direct(self, render_mock):
        req = RequestFactory().get("/firefox/download/thanks/?s=direct")
        req.locale = "en-US"
        view = views.DownloadThanksView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/desktop/thanks_direct.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: False)
    def test_thanks_basic_direct(self, render_mock):
        req = RequestFactory().get("/firefox/download/thanks/?s=direct")
        req.locale = "el"
        view = views.DownloadThanksView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/basic/thanks_direct.html"]

    # end /thanks?s=direct URL - issue 10520

    # begin yandex - issue 5635 & 10607

    @patch.dict(os.environ, SWITCH_FIREFOX_YANDEX="True")
    def test_yandex_download(self, render_mock):
        req = RequestFactory().get("/firefox/new/", HTTP_CF_IPCOUNTRY="RU")
        req.locale = "ru"
        view = views.NewView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/desktop/download_yandex.html"]

    @patch.dict(os.environ, SWITCH_FIREFOX_YANDEX="True")
    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_yandex_show_to_ru(self, render_mock):
        req = RequestFactory().get("/firefox/new/", HTTP_CF_IPCOUNTRY="RU")
        req.locale = "ru"
        view = views.NewView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/desktop/download_yandex.html"]

    @patch.dict(os.environ, SWITCH_FIREFOX_YANDEX="True")
    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_yandex_hide_not_ru_country(self, render_mock):
        req = RequestFactory().get("/firefox/new/", HTTP_CF_IPCOUNTRY="CA")
        req.locale = "ru"
        view = views.NewView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/desktop/download.html"]

    @patch.dict(os.environ, SWITCH_FIREFOX_YANDEX="True")
    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_yandex_hide_not_ru_locale(self, render_mock):
        req = RequestFactory().get("/firefox/new/", HTTP_CF_IPCOUNTRY="RU")
        req.locale = "de"
        view = views.NewView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/desktop/download.html"]

    @patch.dict(os.environ, SWITCH_FIREFOX_YANDEX="False")
    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_yandex_hide_switch_off(self, render_mock):
        req = RequestFactory().get("/firefox/new/", HTTP_CF_IPCOUNTRY="RU")
        req.locale = "ru"
        view = views.NewView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/desktop/download.html"]

    # end yandex - issue 5635 & 10607

    @patch.dict(os.environ, EXP_CONFIG_FX_NEW="de:100")
    def test_experiment_redirect(self, render_mock):
        req = RequestFactory().get("/firefox/new/")
        req.locale = "de"
        view = views.NewView.as_view()
        resp = view(req)
        assert resp.status_code == 302
        assert resp["location"].endswith("/exp/firefox/new/")
        assert resp["cache-control"] == "max-age=0, no-cache, no-store, must-revalidate, private"
        req.locale = "en-US"
        resp = view(req)
        assert resp.status_code == 200
        assert "cache-control" not in resp

    @patch.dict(os.environ, EXP_CONFIG_FX_NEW="de:100")
    def test_experiment_redirect_query(self, render_mock):
        req = RequestFactory().get("/firefox/new/?dude=abide&walter=bowl")
        req.locale = "de"
        view = views.NewView.as_view()
        resp = view(req)
        assert resp.status_code == 302
        assert resp["location"].endswith("/exp/firefox/new/?dude=abide&walter=bowl")

    @patch.dict(os.environ, EXP_CONFIG_FX_NEW="de:100")
    def test_experiment_redirect_automation_param(self, render_mock):
        req = RequestFactory().get("/firefox/new/?automation=true")
        req.locale = "de"
        view = views.NewView.as_view()
        resp = view(req)
        assert resp.status_code == 200
        assert "cache-control" not in resp


class TestFirefoxNewNoIndex(TestCase):
    def test_download_noindex(self):
        # Scene 1 of /firefox/new/ should never contain a noindex tag.
        req = RequestFactory().get("/firefox/new/")
        req.locale = "en-US"
        view = views.NewView.as_view()
        response = view(req)
        doc = pq(response.content)
        robots = doc('meta[name="robots"]')
        assert robots.length == 0

    def test_thanks_canonical(self):
        # Scene 2 /firefox/download/thanks/ should always contain a noindex tag.
        req = RequestFactory().get("/firefox/download/thanks/")
        req.locale = "en-US"
        view = views.DownloadThanksView.as_view()
        response = view(req)
        doc = pq(response.content)
        robots = doc('meta[name="robots"]')
        assert robots.length == 1
        assert "noindex" in robots.attr("content")


@override_settings(DEV=False)
@patch("bedrock.firefox.views.l10n_utils.render", return_value=HttpResponse())
class TestFirefoxPlatform(TestCase):
    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_linux_download_template(self, render_mock):
        req = RequestFactory().get("/firefox/linux/")
        req.locale = "en-US"
        view = views.PlatformViewLinux.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/basic/download_linux.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_mac_download_template(self, render_mock):
        req = RequestFactory().get("/firefox/mac/")
        req.locale = "en-US"
        view = views.PlatformViewMac.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/basic/download_mac.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_windows_download_template(self, render_mock):
        req = RequestFactory().get("/firefox/windows/")
        req.locale = "en-US"
        view = views.PlatformViewWindows.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/new/basic/download_windows.html"]


class TestFirefoxHome(TestCase):
    @patch("bedrock.firefox.views.l10n_utils.render")
    def test_firefox_home(self, render_mock):
        req = RequestFactory().get("/firefox/")
        req.locale = "en-US"
        view = views.FirefoxHomeView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/home/index-master.html"]


class TestFirefoxWelcomePage1(TestCase):
    @patch("bedrock.firefox.views.l10n_utils.render")
    def test_firefox_welcome_page1(self, render_mock):
        req = RequestFactory().get("/firefox/welcome/1/")
        req.locale = "en-US"
        views.firefox_welcome_page1(req)
        render_mock.assert_called_once_with(req, "firefox/welcome/page1.html", ANY, ftl_files="firefox/welcome/page1")
