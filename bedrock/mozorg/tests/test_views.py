# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from unittest.mock import patch

from django.core import mail
from django.http.response import HttpResponse
from django.test import override_settings
from django.test.client import RequestFactory

from bedrock.base.urlresolvers import reverse
from bedrock.mozorg import views
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
    def test_new_homepage_template(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "en-US"
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
    def test_new_homepage_template_global(self, render_mock):
        req = RequestFactory().get("/")
        req.locale = "es-ES"
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


class TestMozorgRedirects(TestCase):
    """Test redirects that are in bedrock.mozorg.nonlocale_urls"""

    def test_paris_office_redirect(self):
        resp = self.client.get("/contact/spaces/paris/", follow=True, headers={"accept-language": "en"})
        # Note that we now 301 straight to the lang-prefixed version of the destination of the redirect
        self.assertEqual(resp.redirect_chain[0], ("/contact/spaces/", 301))
        self.assertEqual(resp.redirect_chain[1], ("/en-US/contact/spaces/", 302))


class TestMiecoEmail(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = views.mieco_email_form
        with self.activate_locale("en-US"):
            self.url = reverse("mozorg.email_mieco")

        self.data = {
            "name": "The Dude",
            "email": "foo@bar.com",
            "interests": "abiding, bowling",
            "description": "The rug really tied the room together.",
        }

    def tearDown(self):
        mail.outbox = []

    def test_not_post(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, b'{"error": 400, "message": "Only POST requests are allowed"}')
        self.assertIn("Access-Control-Allow-Origin", resp.headers)
        self.assertIn("Access-Control-Allow-Headers", resp.headers)

    def test_bad_json(self):
        resp = self.client.post(self.url, content_type="application/json", data='{{"bad": "json"}')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, b'{"error": 400, "message": "Error decoding JSON"}')
        self.assertIn("Access-Control-Allow-Origin", resp.headers)
        self.assertIn("Access-Control-Allow-Headers", resp.headers)

    def test_invalid_email(self):
        resp = self.client.post(self.url, content_type="application/json", data='{"email": "foo@bar"}')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, b'{"error": 400, "message": "Invalid form data"}')
        self.assertIn("Access-Control-Allow-Origin", resp.headers)
        self.assertIn("Access-Control-Allow-Headers", resp.headers)

    def test_invalid_message_id(self):
        self.data["message_id"] = "the-dude"
        resp = self.client.post(self.url, content_type="application/json", data=json.dumps(self.data))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, b'{"error": 400, "message": "Invalid form data"}')
        self.assertIn("Access-Control-Allow-Origin", resp.headers)
        self.assertIn("Access-Control-Allow-Headers", resp.headers)

    @patch("bedrock.mozorg.views.render_to_string", return_value="rendered")
    @patch("bedrock.mozorg.views.EmailMessage")
    def test_success(self, mock_emailMessage, mock_render_to_string):
        resp = self.client.post(self.url, content_type="application/json", data=json.dumps(self.data))

        self.assertEqual(resp.status_code, 200)
        mock_emailMessage.assert_called_once_with(
            views.MIECO_EMAIL_SUBJECT["mieco"], "rendered", views.MIECO_EMAIL_SENDER, views.MIECO_EMAIL_TO["mieco"]
        )
        self.assertEqual(resp.content, b'{"status": "ok"}')
        self.assertIn("Access-Control-Allow-Origin", resp.headers)
        self.assertIn("Access-Control-Allow-Headers", resp.headers)

    @patch("bedrock.mozorg.views.render_to_string", return_value="rendered")
    @patch("bedrock.mozorg.views.EmailMessage")
    def test_success_mieco(self, mock_emailMessage, mock_render_to_string):
        self.data["message_id"] = "mieco"
        resp = self.client.post(self.url, content_type="application/json", data=json.dumps(self.data))

        self.assertEqual(resp.status_code, 200)
        mock_emailMessage.assert_called_once_with(
            views.MIECO_EMAIL_SUBJECT["mieco"], "rendered", views.MIECO_EMAIL_SENDER, views.MIECO_EMAIL_TO["mieco"]
        )
        self.assertEqual(resp.content, b'{"status": "ok"}')
        self.assertIn("Access-Control-Allow-Origin", resp.headers)
        self.assertIn("Access-Control-Allow-Headers", resp.headers)

    @patch("bedrock.mozorg.views.render_to_string", return_value="rendered")
    @patch("bedrock.mozorg.views.EmailMessage")
    def test_success_innovations(self, mock_emailMessage, mock_render_to_string):
        self.data["message_id"] = "innovations"
        resp = self.client.post(self.url, content_type="application/json", data=json.dumps(self.data))

        self.assertEqual(resp.status_code, 200)
        mock_emailMessage.assert_called_once_with(
            views.MIECO_EMAIL_SUBJECT["innovations"], "rendered", views.MIECO_EMAIL_SENDER, views.MIECO_EMAIL_TO["innovations"]
        )
        self.assertEqual(resp.content, b'{"status": "ok"}')
        self.assertIn("Access-Control-Allow-Origin", resp.headers)
        self.assertIn("Access-Control-Allow-Headers", resp.headers)

    def test_outbox(self):
        resp = self.client.post(self.url, content_type="application/json", data=json.dumps(self.data))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertIn(f"Name: {self.data['name']}", email.body)
        self.assertIn(f"E-mail: {self.data['email']}", email.body)
        self.assertIn(f"Interests: {self.data['interests']}", email.body)
        self.assertIn(f"Message:\n{self.data['description']}", email.body)
