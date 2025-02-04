# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from unittest.mock import patch
from urllib.parse import parse_qs

from django.http import HttpResponse
from django.test import override_settings
from django.test.client import RequestFactory

import querystringsafe_base64
from pyquery import PyQuery as pq

from bedrock.base.tests import TestCase
from bedrock.firefox import views


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
            "source": "www.firefox.com",
            "medium": "(none)",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "(not set)",
            "client_id_ga4": "(not set)",
            "session_id": "(not set)",
            "dlsource": "mozorg",
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
            "0180e18d6be618eff051b623dc35f57f4a09c46befdd593f5d7649d80751f981",
        )

    def test_no_valid_param_data(self):
        params = {
            "utm_source": "br@ndt",
            "utm_medium": "ae<t>her",
            "experiment": "dfb</p>s",
            "variation": "ef&bvcv",
            "client_id_ga4": "14</p>4538.1610<t>957",
            "session_id": "2w</br>123bg<u>957",
            "dlsource": "fs<a>44fn</a>",
        }
        final_params = {
            "source": "www.firefox.com",
            "medium": "(none)",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "(not set)",
            "client_id_ga4": "(not set)",
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
            "0180e18d6be618eff051b623dc35f57f4a09c46befdd593f5d7649d80751f981",
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
            "client_id_ga4": "(not set)",
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
            "4dcfffdd4e87c175700d04587d5fa42d613d158e967a282f51c4ea1bc0e9050c",
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
            "client_id_ga4": "2456954538.1610960957",
            "session_id": "1668161374",
            "dlsource": "mozorg",
        }
        final_params = {
            "source": "brandt",
            "medium": "aether",
            "campaign": "The|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in"
            "|thatThe|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in|thatThe"
            "|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in|thatThe|Dude|abides"
            "|I|dont|know|about|you|but|I|take|comfort|in|thatThe|Dude|abides|I|dont|know|about|you_",
            "content": "A144_A000_0000000",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "chrome",
            "client_id_ga4": "2456954538.1610960957",
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
            "6c8179cbe1393961ce310e610f2b49af699f6bc6d2c92d211bdc872a838c5f67",
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
            "experiment": "firefox-download",
            "variation": "1",
            "ua": "chrome",
            "client_id_ga4": "2456954538.1610960957",
            "session_id": "1668161374",
            "dlsource": "mozorg",
        }
        final_params = {
            "source": "brandt",
            "medium": "aether",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "firefox-download",
            "variation": "1",
            "ua": "chrome",
            "client_id_ga4": "2456954538.1610960957",
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
            "f510544be8630ce0b73646a973fa011dc860ace01c3fdb55140d1e7c01c2df60",
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
            "client_id_ga4": "(not set)",
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
            "4dcfffdd4e87c175700d04587d5fa42d613d158e967a282f51c4ea1bc0e9050c",
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
            "client_id_ga4": "(not set)",
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
            "31ce6969fb8131e2a798d0127c2d44fc0ac2d278a59bc793238df06f1e0ae8f5",
        )

    def test_handles_referrer_utf8(self):
        """Should ignore non-ascii domain names.

        We were getting exceptions when the view was trying to base64 encode
        non-ascii domain names in the referrer. The allowed list for bouncer
        doesn't include any such domains anyway, so we should just ignore them.
        """
        params = {"referrer": "http://youtubê.com/sorry/"}
        final_params = {
            "source": "www.firefox.com",
            "medium": "(none)",
            "campaign": "(not set)",
            "content": "(not set)",
            "experiment": "(not set)",
            "variation": "(not set)",
            "ua": "(not set)",
            "client_id_ga4": "(not set)",
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
            "0180e18d6be618eff051b623dc35f57f4a09c46befdd593f5d7649d80751f981",
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
class TestFirefoxDownload(TestCase):
    def test_post(self, render_mock):
        req = RequestFactory().post("/firefox/download/")
        req.locale = "en-US"
        view = views.DownloadView.as_view()
        resp = view(req)
        assert resp.status_code == 405

    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_download_template(self, render_mock):
        req = RequestFactory().get("/firefox/download/")
        req.locale = "en-US"
        view = views.DownloadView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/download/desktop/download.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_thanks_template(self, render_mock):
        req = RequestFactory().get("/firefox/download/thanks/")
        req.locale = "en-US"
        view = views.DownloadThanksView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/download/desktop/thanks.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: False)
    def test_download_basic_template(self, render_mock):
        req = RequestFactory().get("/firefox/download/")
        req.locale = "de"
        view = views.DownloadView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/download/basic/base_download.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: False)
    def test_thanks_basic_template(self, render_mock):
        req = RequestFactory().get("/firefox/download/thanks/")
        req.locale = "de"
        view = views.DownloadThanksView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/download/basic/thanks.html"]

    def test_thanks_redirect(self, render_mock):
        req = RequestFactory().get("/firefox/download/?scene=2&dude=abides")
        req.locale = "en-US"
        view = views.DownloadView.as_view()
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
        assert template == ["firefox/download/desktop/thanks_direct.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: False)
    def test_thanks_basic_direct(self, render_mock):
        req = RequestFactory().get("/firefox/download/thanks/?s=direct")
        req.locale = "el"
        view = views.DownloadThanksView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["firefox/download/basic/thanks_direct.html"]

    # end /thanks?s=direct URL - issue 10520


class TestFirefoxDownloadNoIndex(TestCase):
    def test_download_noindex(self):
        # Scene 1 of /firefox/download/ should never contain a noindex tag.
        response = self.client.get("/en-US/firefox/download/")
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


class TestFirefoxGA(TestCase):
    def assert_ga_attr(self, response):
        doc = pq(response.content)
        links = doc(".mzp-c-button")
        # test buttons all have appropriate attribute to trigger tracking in GA
        for link in links.items():
            cta_text = link.attr("data-cta-text")
            link_text = link.attr("data-link-text")
            if cta_text or link_text:
                assert True
            else:
                assert False, f"{link} does not contain attr data-cta-text or data-link-text"

    def test_firefox_home_GA(self):
        req = RequestFactory().get("/en-US/firefox/")
        view = views.FirefoxHomeView.as_view()
        response = view(req)
        self.assert_ga_attr(response)

    def test_firefox_download_GA(self):
        req = RequestFactory().get("/en-US/firefox/download/")
        view = views.DownloadView.as_view()
        response = view(req)
        self.assert_ga_attr(response)


# Issue 13253: Ensure that Firefox can continue to refer to this URL.
class TestFirefoxSetAsDefaultThanks(TestCase):
    def test_firefox_set_as_default_thanks(self):
        resp = self.client.get("/firefox/set-as-default/thanks/", follow=True)
        assert resp.status_code == 200, "Ensure this URL continues to work, see issue 13253"
        assert resp.templates[0].name == "firefox/set-as-default/thanks.html"
