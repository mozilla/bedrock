# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from django.test.client import RequestFactory

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
