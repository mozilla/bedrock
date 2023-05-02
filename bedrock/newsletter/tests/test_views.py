# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import uuid
from unittest.mock import patch

from django.http import HttpResponse
from django.test.client import RequestFactory

import basket
from pyquery import PyQuery as pq

from bedrock.base.urlresolvers import reverse
from bedrock.mozorg.tests import TestCase
from bedrock.newsletter.views import (
    general_error,
    invalid_email_address,
    newsletter_all_json,
    newsletter_strings_json,
)


class TestConfirmView(TestCase):
    def setUp(self):
        self.token = str(uuid.uuid4())
        self.url = reverse("newsletter.confirm", kwargs={"token": self.token})

    def test_normal(self):
        """Confirm works with a valid token"""
        with patch("basket.confirm") as confirm:
            confirm.return_value = {"status": "ok"}
            rsp = self.client.get(self.url)
            self.assertEqual(302, rsp.status_code)
            self.assertTrue(rsp["Location"].endswith(f"{reverse('newsletter.existing.token', kwargs={'token': self.token})}?confirm=1"))

    def test_normal_with_query_params(self):
        """Confirm works with a valid token"""
        with patch("basket.confirm") as confirm:
            confirm.return_value = {"status": "ok"}
            rsp = self.client.get(self.url + "?utm_tracking=oh+definitely+yes&utm_source=malibu")
            self.assertEqual(302, rsp.status_code)
            self.assertTrue(
                rsp["Location"].endswith(
                    f"{reverse('newsletter.existing.token', kwargs={'token': self.token})}"
                    "?confirm=1&utm_tracking=oh+definitely+yes&utm_source=malibu"
                )
            )

    def test_basket_down(self):
        """If basket is down, we report the appropriate error"""
        with patch("basket.confirm") as confirm:
            confirm.side_effect = basket.BasketException()
            rsp = self.client.get(self.url)
            self.assertEqual(302, rsp.status_code)
            confirm.assert_called_with(self.token)
            self.assertTrue(rsp["Location"].endswith(f"{reverse('newsletter.confirm.thanks')}?error=1"))

    def test_bad_token(self):
        """If the token is bad, we report the appropriate error"""
        with patch("basket.confirm") as confirm:
            confirm.side_effect = basket.BasketException(status_code=403, code=basket.errors.BASKET_UNKNOWN_TOKEN)
            rsp = self.client.get(self.url)
            self.assertEqual(302, rsp.status_code)
            confirm.assert_called_with(self.token)
            self.assertTrue(rsp["Location"].endswith(f"{reverse('newsletter.confirm.thanks')}?error=2"))


class TestNewsletterSubscribe(TestCase):
    def setUp(self):
        self.url = reverse("newsletter.subscribe")

    def ajax_request(self, data, **kwargs):
        return self.request(data, HTTP_X_REQUESTED_WITH="XMLHttpRequest", **kwargs)

    def request(self, data=None, **kwargs):
        if data:
            return self.client.post(self.url, data, **kwargs)
        else:
            return self.client.get(self.url, **kwargs)

    @patch("bedrock.newsletter.views.basket")
    def test_returns_ajax_errors(self, basket_mock):
        """Incomplete data should return specific errors in JSON"""
        data = {
            "newsletters": ["flintstones"],
            "email": "fred@example.com",
            "fmt": "H",
        }
        resp = self.ajax_request(data)
        resp_data = json.loads(resp.content)
        self.assertFalse(resp_data["success"])
        self.assertEqual(len(resp_data["errors"]), 1)
        self.assertIn("privacy", resp_data["errors"][0])
        self.assertFalse(basket_mock.called)

    @patch("bedrock.newsletter.views.basket")
    def test_returns_sanitized_ajax_errors(self, basket_mock):
        """Error messages should be HTML escaped.

        Bug 1116754
        """
        data = {
            "newsletters": ["flintstones"],
            "email": "fred@example.com",
            "fmt": "H",
            "privacy": True,
            "country": '<svg/onload=alert("NEFARIOUSNESS")>',
        }
        resp = self.ajax_request(data)
        resp_data = json.loads(resp.content)
        self.assertFalse(resp_data["success"])
        self.assertEqual(len(resp_data["errors"]), 1)
        self.assertNotIn(data["country"], resp_data["errors"][0])
        self.assertIn("NEFARIOUSNESS", resp_data["errors"][0])
        self.assertIn("&lt;svg", resp_data["errors"][0])
        self.assertFalse(basket_mock.called)

    @patch("bedrock.newsletter.views.basket")
    def test_no_source_url_use_referrer(self, basket_mock):
        """Should set source_url to referrer if not sent"""
        data = {
            "newsletters": ["flintstones"],
            "email": "fred@example.com",
            "fmt": "H",
            "privacy": True,
        }
        source_url = "https://example.com/bambam"
        resp = self.ajax_request(data, HTTP_REFERER=source_url)
        resp_data = json.loads(resp.content)
        self.assertDictEqual(resp_data, {"success": True})
        basket_mock.subscribe.assert_called_with("fred@example.com", "flintstones", format="H", source_url=source_url)

    @patch("bedrock.newsletter.views.basket")
    def test_use_source_url_with_referer(self, basket_mock):
        """Should use source_url even if there's a good referrer"""
        source_url = "https://example.com/bambam"
        data = {"newsletters": ["flintstones"], "email": "fred@example.com", "fmt": "H", "privacy": True, "source_url": source_url}
        resp = self.ajax_request(data, HTTP_REFERER=source_url + "_WILMA")
        resp_data = json.loads(resp.content)
        self.assertDictEqual(resp_data, {"success": True})
        basket_mock.subscribe.assert_called_with("fred@example.com", "flintstones", format="H", source_url=source_url)

    @patch("bedrock.newsletter.views.basket")
    def test_returns_ajax_success(self, basket_mock):
        """Good post should return success JSON"""
        data = {
            "newsletters": ["flintstones"],
            "email": "fred@example.com",
            "fmt": "H",
            "privacy": True,
        }
        resp = self.ajax_request(data)
        resp_data = json.loads(resp.content)
        self.assertDictEqual(resp_data, {"success": True})
        basket_mock.subscribe.assert_called_with("fred@example.com", "flintstones", format="H")

    @patch.object(basket, "subscribe")
    def test_returns_ajax_invalid_email(self, subscribe_mock):
        """Invalid email AJAX post should return proper error."""
        subscribe_mock.side_effect = basket.BasketException(code=basket.errors.BASKET_INVALID_EMAIL)
        data = {
            "newsletters": ["flintstones"],
            "email": "fred@example.com",
            "fmt": "H",
            "privacy": True,
        }
        resp = self.ajax_request(data)
        resp_data = json.loads(resp.content)
        self.assertFalse(resp_data["success"])
        self.assertEqual(resp_data["errors"][0], str(invalid_email_address))

    @patch.object(basket, "subscribe")
    def test_returns_ajax_basket_error(self, subscribe_mock):
        """Basket error AJAX post should return proper error."""
        subscribe_mock.side_effect = basket.BasketException(code=basket.errors.BASKET_NETWORK_FAILURE)
        data = {
            "newsletters": ["flintstones"],
            "email": "fred@example.com",
            "fmt": "H",
            "privacy": True,
        }
        resp = self.ajax_request(data)
        resp_data = json.loads(resp.content)
        self.assertFalse(resp_data["success"])
        self.assertEqual(resp_data["errors"][0], str(general_error))

    def test_shows_form_multi(self):
        """The footer form subscribes to multiple newsletters."""
        resp = self.request()
        doc = pq(resp.content)
        self.assertTrue(doc("#newsletter-form"))
        self.assertTrue(doc('input[value="mozilla-foundation"]'))
        self.assertEqual(doc("#newsletter-submit")[0].attrib["data-cta-type"], "Newsletter-mozilla-firefox-multi")

    def test_shows_form_single(self):
        """The MPL page only subscribes to 'mozilla-foundation', so not a multi-newsletter form."""
        resp = self.client.get("/en-US/MPL/", follow=True)
        doc = pq(resp.content)
        self.assertTrue(doc("#newsletter-form"))
        self.assertTrue(doc('input[value="mozilla-foundation"]'))
        self.assertEqual(doc("#newsletter-submit")[0].attrib["data-cta-type"], "Newsletter-mozilla-foundation")

    @patch("bedrock.newsletter.views.basket")
    def test_returns_success(self, basket_mock):
        """Good non-ajax post should return thank-you page."""
        data = {
            "newsletters": ["flintstones"],
            "email": "fred@example.com",
            "fmt": "H",
            "privacy": True,
        }
        resp = self.request(data=data)
        doc = pq(resp.content)
        self.assertFalse(doc("#newsletter-submit"))
        self.assertFalse(doc('input[value="mozilla-and-you"]'))
        self.assertTrue(doc("#newsletter-thanks"))
        basket_mock.subscribe.assert_called_with("fred@example.com", "flintstones", format="H")

    @patch("bedrock.newsletter.views.basket")
    def test_returns_failure__invalid_newsletter(self, basket_mock):
        """
        Test non-ajax POST with invalid newsletter returns form with errors.

        An invalid newsletter is one with invalid characters, it doesn't check
        against a known list of newsletters.

        """
        data = {
            "newsletters": ["!nv@lid"],
            "email": "fred@example.com",
            "fmt": "H",
            "privacy": True,
        }
        resp = self.request(data=data)
        doc = pq(resp.content)
        self.assertTrue(doc("#newsletter-form"))
        self.assertFalse(doc('input[value="mozilla-and-you"]')[0].checked)
        self.assertFalse(doc("#email-form"))
        # Note: An invalid newsletter isn't shown as an error since these are
        # chosen from a checkbox or hidden field and isn't something the user
        # can correct themselves.
        self.assertFalse(basket_mock.subscribe.called)

    @patch("bedrock.newsletter.views.basket")
    def test_returns_failure__missing_privacy(self, basket_mock):
        """Test non-ajax POST with missing privacy acceptance."""
        data = {
            "newsletters": ["flintstones"],
            "email": "fred@example.com",
            "fmt": "H",
        }
        resp = self.request(data=data)
        doc = pq(resp.content)
        self.assertTrue(doc("#newsletter-form"))
        self.assertTrue(doc('input[value="flintstones"]')[0].checked)
        self.assertFalse(doc("#email-form"))
        self.assertIn("privacy", doc("#newsletter-errors").text())
        self.assertFalse(basket_mock.subscribe.called)


class TestNewsletterAllJson(TestCase):
    def test_newsletter_all_json(self):
        req = RequestFactory().get("/newsletter/newsletter-all.json")
        req.locale = "en-US"
        resp = newsletter_all_json(req)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue("newsletters" in data)


@patch("bedrock.newsletter.views.l10n_utils.render", return_value=HttpResponse())
class TestNewsletterStringsJson(TestCase):
    def test_newsletter_strings_json(self, render_mock):
        req = RequestFactory().get("/newsletter/newsletter-strings.json")
        req.locale = "en-US"
        newsletter_strings_json(req)
        template = render_mock.call_args[0][1]
        self.assertTrue(template == "newsletter/includes/newsletter-strings.json")
