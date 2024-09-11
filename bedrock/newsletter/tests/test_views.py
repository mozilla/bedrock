# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import uuid
from unittest.mock import patch

from django.conf import settings

import basket
from pyquery import PyQuery as pq

from bedrock.base.urlresolvers import reverse
from bedrock.mozorg.tests import TestCase
from bedrock.newsletter.views import general_error, invalid_email_address


class TestConfirmView(TestCase):
    def setUp(self):
        self.token = str(uuid.uuid4())
        self.url = reverse("newsletter.confirm", kwargs={"token": self.token})

    @patch("basket.confirm")
    def test_normal(self, confirm):
        """Confirm works with a valid token"""
        confirm.return_value = {"status": "ok"}
        rsp = self.client.get(self.url)
        self.assertEqual(302, rsp.status_code)
        self.assertURLEqual(rsp["Location"], f"{reverse('newsletter.existing', kwargs={'token': self.token})}?confirm=1")

    @patch("basket.confirm")
    def test_normal_with_query_params(self, confirm):
        """Confirm works with a valid token"""
        confirm.return_value = {"status": "ok"}
        rsp = self.client.get(self.url + "?utm_tracking=oh+definitely+yes&utm_source=malibu")
        self.assertEqual(302, rsp.status_code)
        self.assertURLEqual(
            rsp["Location"],
            f"{reverse('newsletter.existing', kwargs={'token': self.token})}?confirm=1&utm_tracking=oh+definitely+yes&utm_source=malibu",
        )

    def test_no_token_404(self):
        """The confirm view requires a token"""
        url = self.url.replace(f"{self.token}/", "")
        rsp = self.client.get(url)
        self.assertEqual(rsp.status_code, 404)

    @patch("basket.confirm")
    def test_basket_down(self, confirm):
        """If basket is down, we report the appropriate error"""
        confirm.side_effect = basket.BasketException()
        rsp = self.client.get(self.url)
        self.assertEqual(302, rsp.status_code)
        confirm.assert_called_with(self.token)
        self.assertURLEqual(rsp["Location"], f"{reverse('newsletter.confirm.thanks')}?error=1")

    @patch("basket.confirm")
    def test_bad_token(self, confirm):
        """If the token is bad, we report the appropriate error"""
        confirm.side_effect = basket.BasketException(status_code=403, code=basket.errors.BASKET_UNKNOWN_TOKEN)
        rsp = self.client.get(self.url)
        self.assertEqual(302, rsp.status_code)
        confirm.assert_called_with(self.token)
        self.assertURLEqual(rsp["Location"], f"{reverse('newsletter.confirm.thanks')}?error=2")


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
        }
        resp = self.ajax_request(data)
        resp_data = resp.json()
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
            "privacy": True,
            "country": '<svg/onload=alert("NEFARIOUSNESS")>',
        }
        resp = self.ajax_request(data)
        resp_data = resp.json()
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
            "privacy": True,
        }
        source_url = "https://example.com/bambam"
        resp = self.ajax_request(data, HTTP_REFERER=source_url)
        resp_data = resp.json()
        self.assertDictEqual(resp_data, {"success": True})
        basket_mock.subscribe.assert_called_with("fred@example.com", "flintstones", source_url=source_url)

    @patch("bedrock.newsletter.views.basket")
    def test_use_source_url_with_referer(self, basket_mock):
        """Should use source_url even if there's a good referrer"""
        source_url = "https://example.com/bambam"
        data = {"newsletters": ["flintstones"], "email": "fred@example.com", "privacy": True, "source_url": source_url}
        resp = self.ajax_request(data, HTTP_REFERER=source_url + "_WILMA")
        resp_data = resp.json()
        self.assertDictEqual(resp_data, {"success": True})
        basket_mock.subscribe.assert_called_with("fred@example.com", "flintstones", source_url=source_url)

    @patch("bedrock.newsletter.views.basket")
    def test_returns_ajax_success(self, basket_mock):
        """Good post should return success JSON"""
        data = {
            "newsletters": ["flintstones"],
            "email": "fred@example.com",
            "privacy": True,
        }
        resp = self.ajax_request(data)
        resp_data = resp.json()
        self.assertDictEqual(resp_data, {"success": True})
        basket_mock.subscribe.assert_called_with("fred@example.com", "flintstones")

    @patch.object(basket, "subscribe")
    def test_returns_ajax_invalid_email(self, subscribe_mock):
        """Invalid email AJAX post should return proper error."""
        subscribe_mock.side_effect = basket.BasketException(code=basket.errors.BASKET_INVALID_EMAIL)
        data = {
            "newsletters": ["flintstones"],
            "email": "fred@example.com",
            "privacy": True,
        }
        resp = self.ajax_request(data)
        resp_data = resp.json()
        self.assertFalse(resp_data["success"])
        self.assertEqual(resp_data["errors"][0], str(invalid_email_address))

    @patch.object(basket, "subscribe")
    def test_returns_ajax_basket_error(self, subscribe_mock):
        """Basket error AJAX post should return proper error."""
        subscribe_mock.side_effect = basket.BasketException(code=basket.errors.BASKET_NETWORK_FAILURE)
        data = {
            "newsletters": ["flintstones"],
            "email": "fred@example.com",
            "privacy": True,
        }
        resp = self.ajax_request(data)
        resp_data = resp.json()
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
            "privacy": True,
        }
        resp = self.request(data=data)
        doc = pq(resp.content)
        self.assertFalse(doc("#newsletter-submit"))
        self.assertFalse(doc('input[value="mozilla-and-you"]'))
        self.assertTrue(doc("#newsletter-thanks"))
        basket_mock.subscribe.assert_called_with("fred@example.com", "flintstones")

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
        resp = self.client.get(reverse("newsletter.all"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("newsletters", resp.json())


class TestNewsletterStringsJson(TestCase):
    def test_newsletter_strings_json(self):
        resp = self.client.get(reverse("newsletter.strings"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "newsletter/includes/newsletter-strings.json")


class TestNewsletterExistingPage(TestCase):
    def setUp(self):
        self.token = str(uuid.uuid4())
        self.url = reverse("newsletter.existing", kwargs={"token": self.token})
        self.url_no_token = reverse("newsletter.existing.no-token")

    def test_with_token(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "newsletter/management.html")

    def test_template_context(self):
        resp = self.client.get(self.url)
        context = resp.context
        self.assertEqual(context["source_url"], reverse("newsletter.existing.no-token"))
        self.assertEqual(context["did_confirm"], False)

    def test_no_token_okay(self):
        resp = self.client.get(self.url_no_token)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "newsletter/management.html")


class TestNewsletterCountryPage(TestCase):
    def setUp(self):
        self.token = str(uuid.uuid4())
        self.url = reverse("newsletter.country", kwargs={"token": self.token})
        self.url_no_token = reverse("newsletter.country.no-token")

    def test_with_token(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "newsletter/country.html")

    def test_template_context(self):
        resp = self.client.get(self.url)
        context = resp.context
        self.assertEqual(context["action"], f"{settings.BASKET_URL}/news/user-meta/")
        self.assertEqual(context["recovery_url"], reverse("newsletter.recovery"))

    def test_no_token_okay(self):
        resp = self.client.get(self.url_no_token)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "newsletter/country.html")

    def test_country_form(self):
        resp = self.client.get(self.url + "?geo=fr")
        form = resp.context["form"]
        self.assertEqual(form.initial, {"country": "fr"})
        country_choices = dict(form.fields["country"].choices)
        # We always set the locale to 'en-US' in the form, thus why this isn't "États-Unis".
        self.assertEqual(country_choices["us"], "United States")
