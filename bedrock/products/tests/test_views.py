# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from django.http import HttpResponse
from django.test import override_settings
from django.test.client import RequestFactory
from django.urls import reverse

from mock import Mock, patch

from bedrock.mozorg.tests import TestCase
from bedrock.products import views


@patch("bedrock.newsletter.forms.get_lang_choices", lambda *x: [["en", "English"]])
class TestVPNInviteWaitlist(TestCase):
    def setUp(self):
        patcher = patch("bedrock.products.views.basket.subscribe")
        self.mock_subscribe = patcher.start()
        self.addCleanup(patcher.stop)

    def _request(self, data, expected_status=200, locale="en-US"):
        req = RequestFactory().post("/", data)
        req.locale = locale
        resp = views.vpn_invite_waitlist(req)
        assert resp.status_code == expected_status
        return json.loads(resp.content)

    def test_form_success(self):
        resp_data = self._request(
            {"newsletters": "guardian-vpn-waitlist", "email": "test@example.com", "country": "us", "privacy": True, "fmt": "H", "lang": "en"}
        )
        assert resp_data["success"]
        self.mock_subscribe.assert_called_with(
            email="test@example.com", fpn_country="us", fpn_platform="", lang="en", newsletters="guardian-vpn-waitlist"
        )

    def test_invalid_email(self):
        resp_data = self._request(
            {"newsletters": "guardian-vpn-waitlist", "email": "invalid.email", "country": "us", "privacy": True, "fmt": "H", "lang": "en"}
        )
        assert not resp_data["success"]
        assert "Please enter a valid email address" in resp_data["errors"]
        assert not self.mock_subscribe.called

    def test_invalid_country(self):
        resp_data = self._request(
            {"newsletters": "guardian-vpn-waitlist", "email": "test@example.com", "country": "zzzz", "privacy": True, "fmt": "H", "lang": "en"}
        )
        assert not resp_data["success"]
        assert "Select a valid choice. zzzz is not one of the available choices." in resp_data["errors"]
        assert not self.mock_subscribe.called

    def test_platforms(self):
        resp_data = self._request(
            {
                "newsletters": "guardian-vpn-waitlist",
                "email": "test@example.com",
                "country": "us",
                "platforms": ["windows", "android"],
                "privacy": True,
                "fmt": "H",
                "lang": "en",
            }
        )
        assert resp_data["success"]
        self.mock_subscribe.assert_called_with(
            email="test@example.com", fpn_country="us", fpn_platform="windows,android", lang="en", newsletters="guardian-vpn-waitlist"
        )


@patch("bedrock.products.views.l10n_utils.render", return_value=HttpResponse())
class TestVPNLandingPage(TestCase):
    def test_vpn_landing_page_template(self, render_mock):
        req = RequestFactory().get("/products/vpn/")
        req.locale = "en-US"
        view = views.vpn_landing_page
        view(req)
        template = render_mock.call_args[0][1]
        assert template == "products/vpn/landing.html"

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


class TestVPNResourceCenterHelpers(TestCase):
    def _build_mock_entry(self, entry_category_name):
        entry = Mock(name=entry_category_name)
        entry.category = entry_category_name
        return entry

    def test__build_category_list(self):
        root_url = reverse("products.vpn.resource-center.landing")
        cases = [
            {
                "entry_list": [
                    self._build_mock_entry("Category one"),
                    self._build_mock_entry("category TWO"),
                    self._build_mock_entry("Category three"),
                ],
                "expected": [
                    # Alphabetical based on category name
                    {
                        "name": "Category one",
                        "url": f"{root_url}?category=Category+one",
                    },
                    {
                        "name": "Category three",
                        "url": f"{root_url}?category=Category+three",
                    },
                    {
                        "name": "category TWO",
                        "url": f"{root_url}?category=category+TWO",
                    },
                ],
            },
            {
                "entry_list": [
                    self._build_mock_entry("Category one"),
                    self._build_mock_entry("category TWO"),
                    self._build_mock_entry("Category three"),
                    self._build_mock_entry("category TWO"),
                    self._build_mock_entry("Category three"),
                ],
                "expected": [
                    {
                        "name": "Category one",
                        "url": f"{root_url}?category=Category+one",
                    },
                    {
                        "name": "Category three",
                        "url": f"{root_url}?category=Category+three",
                    },
                    {
                        "name": "category TWO",
                        "url": f"{root_url}?category=category+TWO",
                    },
                ],
            },
            {
                "entry_list": [
                    self._build_mock_entry("Category one"),
                    self._build_mock_entry("Category one"),
                    self._build_mock_entry("Category one"),
                    self._build_mock_entry("Category one"),
                    self._build_mock_entry("Category one"),
                    self._build_mock_entry("Category one"),
                ],
                "expected": [
                    {
                        "name": "Category one",
                        "url": f"{root_url}?category=Category+one",
                    },
                ],
            },
            {
                "entry_list": [],
                "expected": [],
            },
        ]
        for case in cases:
            with self.subTest(case=case):
                output = views._build_category_list(
                    case["entry_list"],
                )
                self.assertEqual(output, case["expected"])
