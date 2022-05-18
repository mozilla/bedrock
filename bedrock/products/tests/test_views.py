# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import os
from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import override_settings
from django.test.client import RequestFactory
from django.urls import reverse

from bedrock.contentful.constants import (
    CONTENT_CLASSIFICATION_VPN,
    CONTENT_TYPE_PAGE_RESOURCE_CENTER,
)
from bedrock.contentful.models import ContentfulEntry
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

    @override_settings(DEV=False)
    @patch.dict(os.environ, SWITCH_VPN_AFFILIATE_ATTRIBUTION="True")
    def test_vpn_landing_page_geo_available_affiliate_flow_enabled(self, render_mock):
        req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY="us")
        req.locale = "en-US"
        view = views.vpn_landing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertTrue(ctx["vpn_available"])
        self.assertTrue(ctx["vpn_affiliate_attribution_enabled"])

    @override_settings(DEV=False)
    @patch.dict(os.environ, SWITCH_VPN_AFFILIATE_ATTRIBUTION="False")
    def test_vpn_landing_page_geo_available_affiliate_flow_disabled(self, render_mock):
        req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY="us")
        req.locale = "en-US"
        view = views.vpn_landing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertTrue(ctx["vpn_available"])
        self.assertFalse(ctx["vpn_affiliate_attribution_enabled"])

    @override_settings(DEV=False)
    @patch.dict(os.environ, SWITCH_VPN_AFFILIATE_ATTRIBUTION="True")
    def test_vpn_landing_page_geo_not_available_affiliate_flow_enabled(self, render_mock):
        req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY="cn")
        req.locale = "en-US"
        view = views.vpn_landing_page
        view(req)
        ctx = render_mock.call_args[0][2]
        self.assertFalse(ctx["vpn_available"])
        self.assertFalse(ctx["vpn_affiliate_attribution_enabled"])

    @override_settings(DEV=False)
    @patch.dict(os.environ, SWITCH_VPN_AFFILIATE_ATTRIBUTION="True")
    def test_vpn_landing_page_geo_available_affiliate_not_supported_in_country(self, render_mock):
        req = RequestFactory().get("/products/vpn/", HTTP_CF_IPCOUNTRY="it")
        req.locale = "en-US"
        view = views.vpn_landing_page
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
        self.assertEqual(ctx["android_download_url"], "https://play.google.com/store/apps/details?id=org.mozilla.firefox.vpn")
        self.assertEqual(ctx["ios_download_url"], "https://apps.apple.com/us/app/firefox-private-network-vpn/id1489407738")


class TestVPNResourceCenterHelpers(TestCase):
    def _build_mock_entry(self, entry_category_name):
        entry = Mock(name=entry_category_name)
        entry.category = entry_category_name
        return entry

    def test__filter_articles(self):

        articles = {
            "a": self._build_mock_entry("Category one"),
            "b": self._build_mock_entry("category TWO"),
            "c": self._build_mock_entry("Category three"),
            "d": self._build_mock_entry("category TWO"),
            "e": self._build_mock_entry("category TWO"),
            "f": self._build_mock_entry("category TWO"),
        }

        article_list = articles.values()
        self.assertEqual(
            views._filter_articles(article_list, "category TWO"),
            [
                articles["b"],
                articles["d"],
                articles["e"],
                articles["f"],
            ],
        )

        self.assertEqual(
            views._filter_articles(article_list, "Category one"),
            [
                articles["a"],
            ],
        )
        self.assertEqual(
            views._filter_articles(article_list, ""),
            article_list,
        )

        self.assertEqual(
            views._filter_articles(article_list, None),
            article_list,
        )

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


@override_settings(CONTENTFUL_LOCALE_ACTIVATION_PERCENTAGE=60)
@patch("bedrock.products.views.l10n_utils.render", return_value=HttpResponse())
class TestVPNResourceListingView(TestCase):
    def setUp(self):
        for i in range(8):
            for locale in ["en-US", "fr", "ja"]:
                ContentfulEntry.objects.create(
                    content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
                    category="Test Category",
                    classification=CONTENT_CLASSIFICATION_VPN,
                    locale=locale,
                    contentful_id=f"entry_{i+1}",
                    slug=f"slug-{i+1}",
                    # We only get back the .data field, so let's put something useful in here to look for
                    data={"slug_for_test": f"slug-{i+1}-{locale}"},
                )

    def _request(
        self,
        locale,
        path="/",
        expected_status=200,
    ):
        req = RequestFactory().get(path)
        req.locale = locale
        resp = views.resource_center_landing_view(req)
        assert resp.status_code == expected_status
        return resp

    def test_simple_get__for_valid_locale_with_enough_content(self, render_mock):

        self._request(locale="fr")
        passed_context = render_mock.call_args_list[0][0][2]

        self.assertEqual(passed_context["active_locales"], ["en-US", "fr", "ja"])
        self.assertEqual(
            passed_context["category_list"],
            [{"name": "Test Category", "url": "/products/vpn/resource-center/?category=Test+Category"}],
        )
        self.assertEqual(passed_context["selected_category"], "")
        self.assertEqual(
            [x["slug_for_test"] for x in passed_context["first_article_group"]],
            [
                "slug-1-fr",
                "slug-2-fr",
                "slug-3-fr",
                "slug-4-fr",
                "slug-5-fr",
                "slug-6-fr",
            ],
        )
        self.assertEqual(
            [x["slug_for_test"] for x in passed_context["second_article_group"]],
            [
                "slug-7-fr",
                "slug-8-fr",
            ],
        )

    def test_simple_get__for_unavailable_locale(self, render_mock):
        resp = self._request(locale="sk", expected_status=302, path="/test-path/")
        self.assertEqual(resp.headers["location"], "/en-US/test-path/")
        render_mock.assert_not_called()

    def test_simple_get__for_invalid_locale(self, render_mock):
        resp = self._request(locale="xx", expected_status=302, path="/test-path/")
        self.assertEqual(resp.headers["location"], "/en-US/test-path/")
        render_mock.assert_not_called()

    @override_settings(CONTENTFUL_LOCALE_ACTIVATION_PERCENTAGE=95)
    def test_simple_get__for_valid_locale_WITHOUT_enough_content(self, render_mock):
        # ie, if you go to the VRC for a language we're working on but which
        # isn't active yet because it doesn't meet the activation threshold
        # percentage, we should send you to the default locale by calling render() early
        ContentfulEntry.objects.filter(locale="fr").last().delete()
        assert ContentfulEntry.objects.filter(locale="fr").count() < ContentfulEntry.objects.filter(locale="en-US").count()

        resp = self._request(locale="fr", expected_status=302, path="/test-path/")
        self.assertEqual(resp.headers["location"], "/en-US/test-path/")
        render_mock.assert_not_called()

    def test_category_filtering(self, render_mock):

        first = ContentfulEntry.objects.filter(locale="en-US").first()
        first.category = "other category"
        first.save()

        last = ContentfulEntry.objects.filter(locale="en-US").last()
        last.category = "other category"
        last.save()

        self._request(locale="en-US", path="/?category=other+category")
        passed_context = render_mock.call_args_list[0][0][2]

        self.assertEqual(passed_context["active_locales"], ["en-US", "fr", "ja"])
        self.assertEqual(
            passed_context["category_list"],
            [
                {"name": "Test Category", "url": "/products/vpn/resource-center/?category=Test+Category"},
                {"name": "other category", "url": "/products/vpn/resource-center/?category=other+category"},
            ],
        )
        self.assertEqual(passed_context["selected_category"], "other category")
        self.assertEqual(
            [x["slug_for_test"] for x in passed_context["first_article_group"]],
            [
                "slug-1-en-US",
                "slug-8-en-US",
            ],
        )
        self.assertEqual(
            [x["slug_for_test"] for x in passed_context["second_article_group"]],
            [],
        )

    def test_active_locales_is_in_context(self, render_mock):
        self._request(locale="en-US")
        passed_context = render_mock.call_args_list[0][0][2]
        self.assertEqual(passed_context["active_locales"], ["en-US", "fr", "ja"])


@override_settings(CONTENTFUL_LOCALE_ACTIVATION_PERCENTAGE=60)
class TestVPNResourceArticleView(TestCase):
    def setUp(self):
        for i in range(8):
            for locale in ["en-US", "fr", "ja"]:
                ContentfulEntry.objects.create(
                    content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
                    category="Test Category",
                    classification=CONTENT_CLASSIFICATION_VPN,
                    locale=locale,
                    contentful_id=f"entry_{i+1}",
                    slug=f"slug-{i+1}",
                    # We only get back the .data field, so let's put something useful in here to look for
                    data={"slug_for_test": f"slug-{i+1}-{locale}"},
                )

    @patch("bedrock.products.views.l10n_utils.render", return_value=HttpResponse())
    def test_appropriate_active_locales_is_in_context(self, render_mock):
        # ie, not the full set of available locales, but the ones specific to this page

        # Zap an entry and show that it's not available as a locale option for its locale siblings
        ContentfulEntry.objects.get(locale="fr", slug="slug-4").delete()
        self.client.get("/en-US/products/vpn/resource-center/slug-4/")
        passed_context = render_mock.call_args_list[0][0][2]
        self.assertEqual(passed_context["active_locales"], ["en-US", "ja"])

        # Show that it is for other pages where all three locales are active
        render_mock.reset_mock()
        self.client.get("/en-US/products/vpn/resource-center/slug-2/")
        passed_context = render_mock.call_args_list[0][0][2]
        self.assertEqual(passed_context["active_locales"], ["en-US", "fr", "ja"])

    def test_simple_get__no_active_locales_for_slug_at_all__gives_404(self):
        # change all entries so that get_active_locales helper will return []
        ContentfulEntry.objects.all().update(classification="something-that-will-not-match-query")
        resp = self.client.get("/en-US/products/vpn/resource-center/slug-4/")
        assert resp.status_code == 404

    @patch("bedrock.products.views.l10n_utils.render", return_value=HttpResponse())
    def test_simple_get(self, render_mock):
        resp = self.client.get("/ja/products/vpn/resource-center/slug-2/")
        assert resp.status_code == 200  # From the Mock, but still not a 30x/40x
        passed_context = render_mock.call_args_list[0][0][2]
        self.assertEqual(passed_context["active_locales"], ["en-US", "fr", "ja"])
        self.assertEqual(passed_context["slug_for_test"], "slug-2-ja")
        self.assertEqual(passed_context["related_articles"], [])  # TODO: test independently

    @patch("bedrock.products.views.l10n_utils.render", return_value=HttpResponse())
    def test_simple_get__for_unavailable_locale(self, render_mock):
        resp = self.client.get("/de/products/vpn/resource-center/slug-2/")
        # Which will 404 as expected
        self.assertEqual(resp.headers["location"], "/en-US/products/vpn/resource-center/slug-2/")
        render_mock.assert_not_called()

    @patch("bedrock.products.views.l10n_utils.render", return_value=HttpResponse())
    def test_simple_get__for_invalid_locale(self, render_mock):
        resp = self.client.get("/xx/products/vpn/resource-center/slug-2/")
        # Which will 404 as expected
        self.assertEqual(resp.headers["location"], "/en-US/xx/products/vpn/resource-center/slug-2/")
        render_mock.assert_not_called()
