# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from unittest.mock import ANY, Mock, patch

from django.http.response import HttpResponse
from django.test.client import RequestFactory

import pytest

from bedrock.base.urlresolvers import reverse
from bedrock.mozorg import views
from bedrock.mozorg.models import WebvisionDoc
from bedrock.mozorg.tests import TestCase


class TestViews(TestCase):
    @patch.dict(os.environ, FUNNELCAKE_5_LOCALES="en-US", FUNNELCAKE_5_PLATFORMS="win")
    def test_download_button_funnelcake(self):
        """The download button should have the funnelcake ID."""
        with self.activate("en-US"):
            resp = self.client.get(reverse("mozorg.home"), {"f": "5"})
            assert b"product=firefox-stub-f5&" in resp.content

    def test_download_button_bad_funnelcake(self):
        """The download button should not have a bad funnelcake ID."""
        with self.activate("en-US"):
            resp = self.client.get(reverse("mozorg.home"), {"f": "5dude"})
            assert b"product=firefox-stub&" in resp.content
            assert b"product=firefox-stub-f5dude&" not in resp.content

            resp = self.client.get(reverse("mozorg.home"), {"f": "999999999"})
            assert b"product=firefox-stub&" in resp.content
            assert b"product=firefox-stub-f999999999&" not in resp.content


class TestRobots(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.view = views.Robots()

    def test_production_disallow_all_is_false(self):
        self.view.request = self.rf.get("/", HTTP_HOST="www.mozilla.org")
        self.assertFalse(self.view.get_context_data()["disallow_all"])

    def test_non_production_disallow_all_is_true(self):
        self.view.request = self.rf.get("/", HTTP_HOST="www.allizom.org")
        self.assertTrue(self.view.get_context_data()["disallow_all"])

    def test_robots_no_redirect(self):
        response = self.client.get("/robots.txt", HTTP_HOST="www.mozilla.org")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context_data["disallow_all"])
        self.assertEqual(response.get("Content-Type"), "text/plain")


@patch("bedrock.mozorg.views.l10n_utils.render")
class TestHomePage(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_home_en_template(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "en-US"
        views.home_view(req)
        render_mock.assert_called_once_with(req, "mozorg/home/home.html", ANY)

    def test_home_de_template(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "de"
        views.home_view(req)
        render_mock.assert_called_once_with(req, "mozorg/home/home-de.html", ANY)

    def test_home_fr_template(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "fr"
        views.home_view(req)
        render_mock.assert_called_once_with(req, "mozorg/home/home-fr.html", ANY)

    def test_home_locale_template(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "es"
        views.home_view(req)
        render_mock.assert_called_once_with(req, "mozorg/home/home.html", ANY)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "content_id, page_data, expected_template",
    (
        (
            "abc",
            {"page_type": "pageHome", "info": {"theme": "mozilla"}},
            "mozorg/home/home-contentful.html",
        ),
        (
            "def",
            {"page_type": "pagePageResourceCenter", "info": {"theme": "mozilla"}},
            "products/vpn/resource-center/article.html",
        ),
        (
            "ghi",
            {"page_type": "OTHER", "info": {"theme": "firefox"}},
            "firefox/contentful-all.html",
        ),
        (
            "jkl",
            {"page_type": "OTHER", "info": {"theme": "mozilla"}},
            "mozorg/contentful-all.html",
        ),
        (
            "jkl",
            {"page_type": "OTHER", "info": {"theme": "OTHER"}},
            "mozorg/contentful-all.html",
        ),
    ),
)
@patch("bedrock.mozorg.views.l10n_utils.render")
@patch("bedrock.mozorg.views.ContentfulPage")
# Trying to hot-reload the URLconf with settings.DEV = True was not
# viable when the tests were being run in CI or via Makefile, so
# instead we're explicitly including the urlconf that is loaded
# when settings.DEV is True
@pytest.mark.urls("bedrock.mozorg.dev_urls")
def test_contentful_preview_view(
    contentfulpage_mock,
    render_mock,
    client,
    content_id,
    page_data,
    expected_template,
):

    mock_page_data = Mock(name="mock_page_data")
    mock_page_data.get_content.return_value = page_data
    contentfulpage_mock.return_value = mock_page_data

    render_mock.return_value = HttpResponse("dummy")

    url = reverse("contentful.preview", kwargs={"content_id": content_id})

    client.get(url, follow=True)
    assert render_mock.call_count == 1
    assert render_mock.call_args_list[0][0][1] == expected_template


class TestWebvisionDocView(TestCase):
    def test_doc(self):
        WebvisionDoc.objects.create(name="summary", content='{"title":"<h1>Summary</h1>"}')
        resp = self.client.get(reverse("mozorg.about.webvision.summary"), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["doc"], {"title": "<h1>Summary</h1>"})

    def test_missing_doc_is_404(self):
        resp = self.client.get(reverse("mozorg.about.webvision.full"))
        self.assertEqual(resp.status_code, 404)
