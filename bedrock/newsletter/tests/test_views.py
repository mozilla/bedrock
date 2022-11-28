# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import uuid
from unittest.mock import DEFAULT, patch

from django.http import HttpResponse
from django.test.client import RequestFactory
from django.test.utils import override_settings

import basket
from pyquery import PyQuery as pq

from bedrock.base.urlresolvers import reverse
from bedrock.mozorg.tests import TestCase
from bedrock.newsletter.tests import newsletters
from bedrock.newsletter.views import general_error, invalid_email_address, updated


class TestViews(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    @patch("bedrock.newsletter.views.l10n_utils.render")
    def test_updated_allows_good_tokens(self, mock_render):
        token = str(uuid.uuid4())
        req = self.rf.get("/", {"token": token, "unsub": 1})
        updated(req)
        self.assertEqual(mock_render.call_args[0][2]["token"], token)

    @patch("bedrock.newsletter.views.l10n_utils.render")
    def test_updated_disallows_bad_tokens(self, mock_render):
        token = "the-dude"
        req = self.rf.get("/", {"token": token, "unsub": 1})
        updated(req)
        assert mock_render.call_args[0][2]["token"] is None

        token = "'>\"><img src=x onerror=alert(1)>"
        req = self.rf.get("/", {"token": token, "unsub": 1})
        updated(req)
        assert mock_render.call_args[0][2]["token"] is None


# Always mock basket.request to be sure we never actually call basket
# during tests.
@override_settings(BASKET_API_KEY="basket_key")
@patch("basket.base.request")
class TestExistingNewsletterView(TestCase):
    def setUp(self):
        self.token = str(uuid.uuid4())
        self.user = {
            "newsletters": ["mozilla-and-you"],
            "token": self.token,
            "email": "user@example.com",
            "lang": "pt",
            "country": "br",
            "format": "T",
        }
        # By default, data matches user's existing data; change it
        # in the test as desired. Also, user has accepted privacy
        # checkbox.
        self.data = {
            "form-MAX_NUM_FORMS": 4,
            "form-INITIAL_FORMS": 4,
            "form-TOTAL_FORMS": 4,
            "email": self.user["email"],
            "lang": self.user["lang"],
            "country": self.user["country"],
            "format": self.user["format"],
            "privacy": "on",
            "form-0-newsletter": "mozilla-and-you",
            "form-0-subscribed_radio": "true",
            "form-1-newsletter": "mobile",
            "form-1-subscribed_radio": "false",
            "form-2-newsletter": "firefox-tips",
            "form-2-subscribed_check": "false",
            "form-3-newsletter": "join-mozilla",
            "form-3-subscribed_check": "false",
            "submit": "Save Preferences",
        }
        super().setUp()

    @patch("bedrock.newsletter.utils.get_newsletters")
    def test_will_show_confirm_copy(self, get_newsletters, mock_basket_request):
        # After successful confirm, ensure proper context var is set to display
        # confirmation-specific copy.
        get_newsletters.return_value = newsletters
        url = f"{reverse('newsletter.existing.token', args=(self.token,))}?confirm=1"
        # noinspection PyUnresolvedReferences
        with patch.multiple("basket", request=DEFAULT) as basket_patches:
            with patch("lib.l10n_utils.render") as render:
                basket_patches["request"].return_value = self.user
                render.return_value = HttpResponse("")
                self.client.get(url)
        request, template_name, context = render.call_args[0]
        self.assertEqual(context["did_confirm"], True)

    @patch("bedrock.newsletter.utils.get_newsletters")
    def test_get_token(self, get_newsletters, mock_basket_request):
        # If user gets page with valid token in their URL, they
        # see their data, and no privacy checkbox is presented
        get_newsletters.return_value = newsletters
        url = reverse("newsletter.existing.token", args=(self.token,))
        # noinspection PyUnresolvedReferences
        with patch.multiple("basket", update_user=DEFAULT, subscribe=DEFAULT, unsubscribe=DEFAULT, request=DEFAULT) as basket_patches:
            with patch("lib.l10n_utils.render") as render:
                basket_patches["request"].return_value = self.user
                render.return_value = HttpResponse("")
                self.client.get(url)
        request, template_name, context = render.call_args[0]
        form = context["form"]
        self.assertNotIn("privacy", form.fields)
        self.assertEqual(self.user["lang"], form.initial["lang"])

    @patch("bedrock.newsletter.utils.get_newsletters")
    def test_show(self, get_newsletters, mock_basket_request):
        # Newsletters are only listed if the user is subscribed to them,
        # or they are marked 'show' and 'active' in the settings
        get_newsletters.return_value = newsletters
        # Find a newsletter without 'show' and subscribe the user to it
        for newsletter, data in newsletters.items():
            if not data.get("show", False):
                self.user["newsletters"] = [newsletter]
                break
        url = reverse("newsletter.existing.token", args=(self.token,))
        with patch.multiple("basket", update_user=DEFAULT, subscribe=DEFAULT, unsubscribe=DEFAULT, request=DEFAULT) as basket_patches:
            with patch("lib.l10n_utils.render") as render:
                basket_patches["request"].return_value = self.user
                render.return_value = HttpResponse("")
                self.client.get(url)
        request, template_name, context = render.call_args[0]
        forms = context["formset"].initial_forms

        shown = {form.initial["newsletter"] for form in forms}
        inactive = {newsletter for newsletter, data in newsletters.items() if not data.get("active", False)}
        to_show = {newsletter for newsletter, data in newsletters.items() if data.get("show", False)} - inactive
        subscribed = set(self.user["newsletters"])

        # All subscribed newsletters except inactive ones are shown
        self.assertEqual(set(), subscribed - inactive - shown)
        # All 'show' newsletters are shown
        self.assertEqual(set(), to_show - shown)
        # No other newsletters are shown
        self.assertEqual(set(), shown - subscribed - to_show)

    def test_get_no_token(self, mock_basket_request):
        # No token in URL - should redirect to recovery
        url = reverse("newsletter.existing.token", args=("",))
        rsp = self.client.get(url)
        self.assertEqual(302, rsp.status_code)
        self.assertTrue(rsp["Location"].endswith(reverse("newsletter.recovery")))

    def test_get_user_not_found(self, mock_basket_request):
        # Token in URL but not a valid token - should redirect to recovery
        rand_token = str(uuid.uuid4())
        url = reverse("newsletter.existing.token", args=(rand_token,))
        with patch.multiple("basket", request=DEFAULT) as basket_patches:
            with patch("lib.l10n_utils.render") as render:
                render.return_value = HttpResponse("")
                with patch("django.contrib.messages.add_message") as add_msg:
                    basket_patches["request"].side_effect = basket.BasketException
                    rsp = self.client.get(url)
        # Should have given a message
        self.assertEqual(1, add_msg.call_count, msg=repr(add_msg.call_args_list))
        # Should have been redirected to recovery page
        self.assertEqual(302, rsp.status_code)
        self.assertTrue(rsp["Location"].endswith(reverse("newsletter.recovery")))

    def test_invalid_token(self, mock_basket_request):
        # "Token" in URL is not syntactically a UUID - should redirect to
        # recovery *without* calling Exact Target
        token = "not a token"
        url = reverse("newsletter.existing.token", args=(token,))
        with patch.multiple("basket", request=DEFAULT) as basket_patches:
            with patch("django.contrib.messages.add_message") as add_msg:
                rsp = self.client.get(url, follow=False)
        self.assertEqual(0, basket_patches["request"].call_count)
        self.assertEqual(1, add_msg.call_count)
        self.assertEqual(302, rsp.status_code)
        self.assertTrue(rsp["Location"].endswith(reverse("newsletter.recovery")))

    def test_post_user_not_found(self, mock_basket_request):
        # User submits form and passed token, but no user was found
        # Should issue message and redirect to recovery
        rand_token = str(uuid.uuid4())
        url = reverse("newsletter.existing.token", args=(rand_token,))
        with patch.multiple("basket", update_user=DEFAULT, subscribe=DEFAULT, unsubscribe=DEFAULT, request=DEFAULT) as basket_patches:
            with patch("lib.l10n_utils.render") as render:
                render.return_value = HttpResponse("")
                with patch("django.contrib.messages.add_message") as add_msg:
                    basket_patches["request"].side_effect = basket.BasketException
                    rsp = self.client.post(url, self.data)
        # Shouldn't call basket except for the attempt to find the user
        self.assertEqual(0, basket_patches["update_user"].call_count)
        self.assertEqual(0, basket_patches["unsubscribe"].call_count)
        self.assertEqual(0, basket_patches["subscribe"].call_count)
        # Should have given a message
        self.assertEqual(1, add_msg.call_count, msg=repr(add_msg.call_args_list))
        # Should have been redirected to recovery page
        self.assertEqual(302, rsp.status_code)
        self.assertTrue(rsp["Location"].endswith(reverse("newsletter.recovery")))

    @patch("bedrock.newsletter.utils.get_newsletters")
    def test_subscribing(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        # They subscribe to firefox-tips
        self.data["form-2-subscribed_check"] = "true"
        # in English - and that's their language too
        self.user["lang"] = "en"
        self.data["lang"] = "en"
        url = reverse("newsletter.existing.token", args=(self.token,))
        with patch.multiple("basket", update_user=DEFAULT, subscribe=DEFAULT, unsubscribe=DEFAULT, request=DEFAULT) as basket_patches:
            with patch("django.contrib.messages.add_message") as add_msg:
                with patch("lib.l10n_utils.render"):
                    basket_patches["request"].return_value = self.user
                    rsp = self.client.post(url, self.data)
        # Should have given no messages
        self.assertEqual(0, add_msg.call_count, msg=repr(add_msg.call_args_list))
        # Should have called update_user with subscription list
        self.assertEqual(1, basket_patches["update_user"].call_count)
        kwargs = basket_patches["update_user"].call_args[1]
        self.assertEqual(set(kwargs), {"api_key", "newsletters", "lang"})
        self.assertEqual(kwargs["lang"], "en")
        self.assertEqual(set(kwargs["newsletters"].split(",")), {"mozilla-and-you", "firefox-tips"})
        # Should not have called unsubscribe
        self.assertEqual(0, basket_patches["unsubscribe"].call_count)
        # Should not have called subscribe
        self.assertEqual(0, basket_patches["subscribe"].call_count)
        # Should redirect to the 'updated' view
        url = reverse("newsletter.updated")
        assert rsp["Location"] == url

    @patch("bedrock.newsletter.utils.get_newsletters")
    def test_unsubscribing(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        # They unsubscribe from the one newsletter they're subscribed to
        self.data["form-0-subscribed_radio"] = "False"
        url = reverse("newsletter.existing.token", args=(self.token,))
        with patch.multiple("basket", update_user=DEFAULT, subscribe=DEFAULT, unsubscribe=DEFAULT, request=DEFAULT) as basket_patches:
            with patch("lib.l10n_utils.render"):
                basket_patches["request"].return_value = self.user
                rsp = self.client.post(url, self.data)
        # Should have called update_user with list of newsletters
        self.assertEqual(1, basket_patches["update_user"].call_count)
        kwargs = basket_patches["update_user"].call_args[1]
        self.assertEqual({"api_key": "basket_key", "newsletters": "", "lang": "pt"}, kwargs)
        # Should not have called subscribe
        self.assertEqual(0, basket_patches["subscribe"].call_count)
        # Should not have called unsubscribe
        self.assertEqual(0, basket_patches["unsubscribe"].call_count)
        # Should redirect to the 'updated' view
        url = reverse("newsletter.updated")
        assert rsp["Location"] == url

    @patch("bedrock.newsletter.utils.get_newsletters")
    def test_remove_all(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        self.data["remove_all"] = "on"  # any value should do

        url = reverse("newsletter.existing.token", args=(self.token,))
        with patch.multiple("basket", update_user=DEFAULT, subscribe=DEFAULT, unsubscribe=DEFAULT, request=DEFAULT) as basket_patches:
            with patch("lib.l10n_utils.render"):
                basket_patches["request"].return_value = self.user
                rsp = self.client.post(url, self.data)
        # Should not have updated user details at all
        self.assertEqual(0, basket_patches["update_user"].call_count)
        # Should have called unsubscribe
        self.assertEqual(1, basket_patches["unsubscribe"].call_count)
        # and said user opts out
        args, kwargs = basket_patches["unsubscribe"].call_args
        self.assertEqual((self.token, self.user["email"]), args)
        self.assertTrue(kwargs["optout"])
        # Should redirect to the 'updated' view with unsub=1 and token
        url = f"{reverse('newsletter.updated')}?unsub=1&token={self.token}"
        assert rsp["Location"] == url

    @patch("bedrock.newsletter.utils.get_newsletters")
    def test_change_lang_country(self, get_newsletters, mock_basket_request):
        get_newsletters.return_value = newsletters
        self.data["lang"] = "en"
        self.data["country"] = "us"

        with self.activate("en-US"):
            url = reverse("newsletter.existing.token", args=(self.token,))

        with patch.multiple("basket", update_user=DEFAULT, subscribe=DEFAULT, request=DEFAULT) as basket_patches:
            with patch("lib.l10n_utils.render"):
                with patch("django.contrib.messages.add_message") as add_msg:
                    basket_patches["request"].return_value = self.user
                    rsp = self.client.post(url, self.data)

        # We have an existing user with a change to their email data,
        # but none to their subscriptions.
        # 'subscribe' should not be called
        self.assertEqual(0, basket_patches["subscribe"].call_count)
        # update_user should be called once
        self.assertEqual(1, basket_patches["update_user"].call_count)
        # with the new lang and country and the newsletter list
        kwargs = basket_patches["update_user"].call_args[1]
        self.assertEqual({"api_key": "basket_key", "lang": "en", "country": "us", "newsletters": "mozilla-and-you"}, kwargs)
        # No messages should be emitted
        self.assertEqual(0, add_msg.call_count, msg=repr(add_msg.call_args_list))
        # Should redirect to the 'updated' view
        url = reverse("newsletter.updated")
        assert rsp["Location"] == url

    @patch("bedrock.newsletter.utils.get_newsletters")
    def test_newsletter_ordering(self, get_newsletters, mock_basket_request):
        # Newsletters are listed in 'order' order, if they have an 'order'
        # field
        get_newsletters.return_value = newsletters
        url = reverse("newsletter.existing.token", args=(self.token,))
        self.user["newsletters"] = ["mozilla-and-you", "firefox-tips", "beta"]
        with patch.multiple("basket", update_user=DEFAULT, subscribe=DEFAULT, unsubscribe=DEFAULT, request=DEFAULT) as basket_patches:
            with patch("lib.l10n_utils.render") as render:
                basket_patches["request"].return_value = self.user
                render.return_value = HttpResponse("")
                self.client.get(url)
        request, template_name, context = render.call_args[0]
        forms = context["formset"].initial_forms

        newsletters_in_order = [form.initial["newsletter"] for form in forms]
        self.assertEqual(["firefox-tips", "mozilla-and-you"], newsletters_in_order)

    @patch("bedrock.newsletter.utils.get_newsletters")
    def test_newsletter_no_order(self, get_newsletters, mock_basket_request):
        """Newsletter views should work if we get no order from basket."""
        orderless_newsletters = {}
        for key, val in newsletters.items():
            nl_copy = val.copy()
            del nl_copy["order"]
            orderless_newsletters[key] = nl_copy

        get_newsletters.return_value = orderless_newsletters
        url = reverse("newsletter.existing.token", args=(self.token,))
        self.user["newsletters"] = ["mozilla-and-you", "firefox-tips", "beta"]
        with patch.multiple("basket", update_user=DEFAULT, subscribe=DEFAULT, unsubscribe=DEFAULT, request=DEFAULT) as basket_patches:
            with patch("lib.l10n_utils.render") as render:
                basket_patches["request"].return_value = self.user
                render.return_value = HttpResponse("")
                self.client.get(url)
        request, template_name, context = render.call_args[0]
        forms = context["formset"].initial_forms

        newsletters_in_order = [form.initial["newsletter"] for form in forms]
        self.assertEqual(["mozilla-and-you", "firefox-tips"], newsletters_in_order)


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
            with patch("lib.l10n_utils.render") as mock_render:
                mock_render.return_value = HttpResponse("")
                rsp = self.client.get(self.url, follow=True)
            self.assertEqual(200, rsp.status_code)
            confirm.assert_called_with(self.token)
            context = mock_render.call_args[0][2]
            self.assertFalse(context["success"])
            self.assertTrue(context["generic_error"])
            self.assertFalse(context["token_error"])

    def test_bad_token(self):
        """If the token is bad, we report the appropriate error"""
        with patch("basket.confirm") as confirm:
            confirm.side_effect = basket.BasketException(status_code=403, code=basket.errors.BASKET_UNKNOWN_TOKEN)
            with patch("lib.l10n_utils.render") as mock_render:
                mock_render.return_value = HttpResponse("")
                rsp = self.client.get(self.url, follow=True)
            self.assertEqual(200, rsp.status_code)
            confirm.assert_called_with(self.token)
            context = mock_render.call_args[0][2]
            self.assertFalse(context["success"])
            self.assertFalse(context["generic_error"])
            self.assertTrue(context["token_error"])


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
