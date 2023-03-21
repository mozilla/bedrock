# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from unittest.mock import ANY, patch
from urllib.parse import parse_qs

from django.conf import settings
from django.http import HttpResponse
from django.test import override_settings
from django.test.client import RequestFactory
from django.urls import reverse

import querystringsafe_base64
from pyquery import PyQuery as pq
from twilio.base.exceptions import TwilioRestException

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
            "client_id": "(not set)",
            "session_id": "(not set)",
            "dlsource": "(not set)",
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
            "d09a7d09fa80872d3835161b0b3072332ec773753e6481306c1a7c4f1ef77216",
        )

    def test_no_valid_param_data(self):
        params = {
            "utm_source": "br@ndt",
            "utm_medium": "ae<t>her",
            "experiment": "dfb</p>s",
            "variation": "ef&bvcv",
            "client_id": "14</p>4538.1610<t>957",
            "session_id": "2w</br>123bg<u>957",
            "dlsource": "fs<a>44fn</a>",
        }
        final_params = {
            "source": "www.mozilla.org",
            "medium": "(none)",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "(not set)",
            "client_id": "(not set)",
            "session_id": "(not set)",
            "dlsource": "(not set)",
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
            "d09a7d09fa80872d3835161b0b3072332ec773753e6481306c1a7c4f1ef77216",
        )

    def test_some_valid_param_data(self):
        params = {"utm_source": "brandt", "utm_content": "ae<t>her", "dlsource": "mozorg"}
        final_params = {
            "source": "brandt",
            "medium": "(direct)",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "(not set)",
            "client_id": "(not set)",
            "session_id": "(not set)",
            "dlsource": "mozorg",
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
            "ed0705c22e56e7ed8152b08abd3df72a897ae00b30f7c802aa4a19e3a8c77503",
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
            "client_id": "1456954538.1610960957",
            "session_id": "1668161374",
            "dlsource": "mozorg",
        }
        final_params = {
            "source": "brandt",
            "medium": "aether",
            "campaign": "The|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in"
            "|thatThe|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in|thatThe"
            "|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in|thatThe|Dude|abides"
            "|I|dont|know|about|you|but|I|take|comfort|in|thatThe|Dude|abides|I|dont|know"
            "|about|you|b_",
            "content": "A144_A000_0000000",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "chrome",
            "client_id": "1456954538.1610960957",
            "session_id": "1668161374",
            "dlsource": "mozorg",
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
            "16010b2f9581e4ba48689125b7f35e4f4420399da1f0f245e814da071c726991",
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
            "client_id": "1456954538.1610960957",
            "session_id": "1668161374",
            "dlsource": "mozorg",
        }
        final_params = {
            "source": "brandt",
            "medium": "aether",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "firefox-new",
            "variation": "1",
            "ua": "chrome",
            "client_id": "1456954538.1610960957",
            "session_id": "1668161374",
            "dlsource": "mozorg",
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
            "98c68dcf0ff6086b9e546dda753a830127afc4981745a32a6b6c3dfe81295877",
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
            "client_id": "(not set)",
            "session_id": "(not set)",
            "dlsource": "(not set)",
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
            "9657ba3bdb383411ede4c7da300712624b893e3a8f7d69e804485bec4606628f",
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
            "client_id": "(not set)",
            "session_id": "(not set)",
            "dlsource": "(not set)",
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
            "14670eae778afebe5f68d8e844a87717630a9264a79861f3ebe048fac09431df",
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
            "client_id": "(not set)",
            "session_id": "(not set)",
            "dlsource": "(not set)",
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
            "d09a7d09fa80872d3835161b0b3072332ec773753e6481306c1a7c4f1ef77216",
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


@override_settings(DEV=False)
@patch("bedrock.firefox.views.l10n_utils.render", return_value=HttpResponse())
class TestFirefoxNew(TestCase):
    def test_post(self, render_mock):
        req = RequestFactory().post("/firefox/new/")
        req.locale = "en-US"
        view = views.NewView.as_view()
        resp = view(req)
        assert resp.status_code == 405

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


class TestFirefoxNewNoIndex(TestCase):
    def test_download_noindex(self):
        # Scene 1 of /firefox/new/ should never contain a noindex tag.
        response = self.client.get("/en-US/firefox/new/")
        doc = pq(response.content)
        robots = doc('meta[name="robots"]')
        assert robots.length == 0

    def test_thanks_canonical(self):
        # Scene 2 /firefox/download/thanks/ should always contain a noindex tag.
        response = self.client.get("/en-US/firefox/download/thanks/")
        doc = pq(response.content)
        robots = doc('meta[name="robots"]')
        assert robots.length == 1
        assert "noindex" in robots.attr("content")
        assert "follow" in robots.attr("content")


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


class TestFirefoxGA(TestCase):
    def assert_ga_attr(self, response):
        doc = pq(response.content)
        links = doc(".mzp-c-button")
        for link in links.items():
            cta_data = link.attr("data-cta-type")
            cta_link = link.attr("data-link-type")
            if cta_data:
                contains_cta = any(cta_data in item for item in ["link", "button"])
                assert contains_cta or "fxa-" in cta_data
            elif cta_link:
                cta_link_types = ["download", "button", "link"]
                assert cta_link in cta_link_types
            else:
                assert False, f"{link} does not contain attr cta-type or link-type"

    def test_firefox_home_GA(self):
        req = RequestFactory().get("/en-US/firefox/")
        view = views.FirefoxHomeView.as_view()
        response = view(req)
        self.assert_ga_attr(response)

    def test_firefox_new_GA(self):
        req = RequestFactory().get("/en-US/firefox/new/")
        view = views.NewView.as_view()
        response = view(req)
        self.assert_ga_attr(response)


class TestFirefoxWelcomePage1(TestCase):
    @patch("bedrock.firefox.views.l10n_utils.render")
    def test_firefox_welcome_page1(self, render_mock):
        req = RequestFactory().get("/firefox/welcome/1/")
        req.locale = "en-US"
        views.firefox_welcome_page1(req)
        render_mock.assert_called_once_with(req, "firefox/welcome/page1.html", ANY, ftl_files="firefox/welcome/page1")


@override_settings(
    TWILIO_ACCOUNT_SID="",
    TWILIO_AUTH_TOKEN="",
    TWILIO_MESSAGING_SERVICE_SID="",
)
class TestSMSSendToDevice(TestCase):
    def setUp(self):
        self.url = "/en-US" + reverse("firefox.sms-send-to-device-post")

    def _do_post(self, params):
        return self.client.post(
            self.url,
            data=params,
        )

    @patch("bedrock.firefox.views.TWILIO_CLIENT")
    def test_no_data(self, mock_client):
        resp = self._do_post({})
        assert resp.status_code == 200
        data = resp.json()
        assert not data["success"]
        assert data["errors"] == ["Invalid phone number"]

    @patch("bedrock.firefox.views.TWILIO_CLIENT")
    def test_invalid_number(self, mock_client):
        resp = self._do_post({"phone_number": "abcdef"})
        assert resp.status_code == 200
        data = resp.json()
        assert not data["success"]
        assert data["errors"] == ["Invalid phone number"]

    @patch("bedrock.firefox.views.TWILIO_CLIENT")
    def test_invalid_number_for_region(self, mock_client):
        resp = self._do_post({"phone_number": "98 555 1212"})
        assert resp.status_code == 200
        data = resp.json()
        assert not data["success"]
        assert data["errors"] == ["Invalid phone number for region: US"]

    @patch("bedrock.firefox.views.TWILIO_CLIENT")
    def test_valid_number(self, mock_client):
        valid_numbers = ["4155551212", "(415) 555-1212", "415.555.1212", "415-555-1212"]
        for number in valid_numbers:
            resp = self._do_post({"phone_number": number})
            assert resp.status_code == 200
            data = resp.json()
            assert data["success"] is True
            mock_client.messages.create.assert_called_once_with(
                to="+14155551212",
                body="Download the Firefox mobile browser for automatic protection on all your devices. https://app.adjust.com/48k9twc",
                messaging_service_sid=settings.TWILIO_MESSAGING_SERVICE_SID,
            )
            mock_client.reset_mock()

    @patch("bedrock.firefox.views.TWILIO_CLIENT")
    def test_twilio_exception(self, mock_client):
        mock_client.messages.create.side_effect = TwilioRestException(status=500, uri="/", msg="Some error")
        resp = self._do_post({"phone_number": "415 555 1212"})
        assert resp.status_code == 200
        data = resp.json()
        assert not data["success"]
        assert data["errors"] == ["Message failed to send"]

    def test_missing_twilio_settings(self):
        resp = self._do_post({"phone_number": "415 555 1212"})
        assert resp.status_code == 200
        data = resp.json()
        assert not data["success"]
        assert data["errors"] == ["SMS not configured"]


@override_settings(DEV=False)
@patch("bedrock.firefox.views.l10n_utils.render", return_value=HttpResponse())
class TestFirefoxMobile(TestCase):
    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_landing_template(self, render_mock):
        req = RequestFactory().get("/firefox/browsers/mobile/")
        req.locale = "en-US"
        view = views.FirefoxMobileView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/browsers/mobile/index.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: False)
    def test_legacy_template(self, render_mock):
        req = RequestFactory().get("/firefox/browsers/mobile/")
        req.locale = "en-US"
        view = views.FirefoxMobileView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/mobile/index.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_legacy_template_param(self, render_mock):
        req = RequestFactory().get("/firefox/browsers/mobile/?xv=legacy")
        req.locale = "en-US"
        view = views.FirefoxMobileView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/mobile/index.html"]
