# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.http.response import HttpResponse
from django.test import override_settings
from django.test.client import RequestFactory

from bedrock.base.urlresolvers import reverse
from bedrock.mozorg import views
from bedrock.mozorg.models import WebvisionDoc
from bedrock.mozorg.tests import TestCase


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
        response = self.client.get("/robots.txt", headers={"host": "www.mozilla.org"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context_data["disallow_all"])
        self.assertEqual(response.get("Content-Type"), "text/plain")


class TestSecurityDotTxt(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.view = views.SecurityDotTxt()

    def test_no_redirect(self):
        response = self.client.get("/.well-known/security.txt", headers={"host": "www.mozilla.org"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get("Content-Type"), "text/plain")
        self.assertContains(response, "security@mozilla.org")


@override_settings(DEV=False)
@patch("bedrock.mozorg.views.l10n_utils.render", return_value=HttpResponse())
class TestHomePageLocales(TestCase):
    def test_post(self, render_mock):
        req = RequestFactory().post("/")
        req.locale = "en-US"
        view = views.HomeView.as_view()
        resp = view(req)
        assert resp.status_code == 405

    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_m24_homepage_template(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "en-US"
        view = views.HomeView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["mozorg/home/home-m24.html"]

    def test_new_homepage_template(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "en-US"
        with patch.object(views, "ftl_file_is_active") as active_mock:
            active_mock.side_effect = [False, True]
            view = views.HomeView.as_view()
            view(req)
            template = render_mock.call_args[0][1]
            assert template == ["mozorg/home/home-new.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: False)
    def test_old_homepage_template(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "en-US"
        view = views.HomeView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["mozorg/home/home-old.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_m24_homepage_template_global(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "es-ES"
        view = views.HomeView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["mozorg/home/home-m24.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: True)
    def test_new_homepage_template_global(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "es-ES"
        with patch.object(views, "ftl_file_is_active") as active_mock:
            active_mock.side_effect = [False, True]
            view = views.HomeView.as_view()
            view(req)
            template = render_mock.call_args[0][1]
            assert template == ["mozorg/home/home-new.html"]

    @patch.object(views, "ftl_file_is_active", lambda *x: False)
    def test_old_homepage_template_global(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "es-ES"
        view = views.HomeView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ["mozorg/home/home-old.html"]

    def test_no_post(self, render_mock):
        req = RequestFactory().post("/")
        req.locale = "en-US"
        home_view = views.HomeView.as_view()
        resp = home_view(req)
        self.assertEqual(resp.status_code, 405)


class TestWebvisionDocView(TestCase):
    def test_doc(self):
        WebvisionDoc.objects.create(name="summary", content={"title": "<h1>Summary</h1>"})
        resp = self.client.get(reverse("mozorg.about.webvision.summary"), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["doc"], {"title": "<h1>Summary</h1>"})

    def test_missing_doc_is_404(self):
        resp = self.client.get(reverse("mozorg.about.webvision.full"), follow=True)
        self.assertEqual(resp.status_code, 404)


class TestMozorgRedirects(TestCase):
    """Test redirects that are in bedrock.mozorg.nonlocale_urls"""

    def test_projects_calendar_redirect(self):
        resp = self.client.get("/projects/calendar/", follow=True)
        # Note that we now 301 straight to the lang-prefixed version of the destination of the redirect
        self.assertEqual(resp.redirect_chain[0], ("https://www.thunderbird.net/calendar/", 301))

    def test_paris_office_redirect(self):
        resp = self.client.get("/contact/spaces/paris/", follow=True, headers={"accept-language": "en"})
        # Note that we now 301 straight to the lang-prefixed version of the destination of the redirect
        self.assertEqual(resp.redirect_chain[0], ("/contact/spaces/", 301))
        self.assertEqual(resp.redirect_chain[1], ("/en-US/contact/spaces/", 302))

    def test_diversity_redirect(self):
        for path in ("/diversity/", "/diversity"):
            with self.subTest(path):
                resp = self.client.get(path, follow=True, headers={"accept-language": "en"})
                # Note that we now 301 straight to the lang-prefixed version of the destination of the redirect
                self.assertEqual(resp.redirect_chain[0], ("/diversity/2022/", 301))
                self.assertEqual(resp.redirect_chain[1], ("/en-US/diversity/2022/", 302))

    def test_webvision_redirect(self):
        # Since the webvision URL requires a WebvisionDoc to exist, we test this
        # here instead of in the redirects tests.
        WebvisionDoc.objects.create(name="summary", content="")

        for path in ("/webvision/", "/webvision"):
            with self.subTest(path):
                resp = self.client.get(path, follow=True, headers={"accept-language": "en"})
                self.assertEqual(resp.redirect_chain[0], ("/about/webvision/", 301))
                self.assertEqual(resp.redirect_chain[1], ("/en-US/about/webvision/", 302))
