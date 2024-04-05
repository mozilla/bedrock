# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest import mock

from bedrock.mozorg.tests import TestCase
from bedrock.newsletter.forms import (
    BooleanTabularRadioSelect,
    NewsletterFooterForm,
    NewsletterForm,
)
from bedrock.newsletter.tests import newsletters

newsletters_mock = mock.Mock()
newsletters_mock.return_value = newsletters


class TestRenderers(TestCase):
    def test_str_true(self):
        """renderer starts with True selected if value given is True"""
        widget = BooleanTabularRadioSelect()
        output = widget.render("name", value=True)

        # The True choice should be checked
        self.assertIn('value="true" checked', output)

    def test_str_false(self):
        """renderer starts with False selected if value given is False"""
        widget = BooleanTabularRadioSelect()
        output = widget.render("name", value=False)

        # The False choice should be checked
        self.assertIn('value="false" checked', output)

    def test_boolean_true(self):
        """renderer starts with True selected if value given is True"""
        widget = BooleanTabularRadioSelect()
        output = widget.render("name", value=True)

        # The True choice should be checked
        self.assertIn('value="true" checked', output)

    def test_boolean_false(self):
        """renderer starts with False selected if value given is False"""
        widget = BooleanTabularRadioSelect()
        output = widget.render("name", value=False)

        # The False choice should be checked
        self.assertIn('value="false" checked', output)


@mock.patch("bedrock.newsletter.utils.get_newsletters", newsletters_mock)
class TestNewsletterForm(TestCase):
    def test_form(self):
        """test NewsletterForm"""
        # not much to test, but at least construct one
        title = "Newsletter title"
        newsletter = "newsletter-a"
        initial = {
            "title": title,
            "newsletter": newsletter,
            "subscribed_radio": True,
            "subscribed_check": True,
        }
        form = NewsletterForm(initial=initial)
        rendered = str(form)
        self.assertIn(newsletter, rendered)
        self.assertIn(title, rendered)
        # And validate one
        form = NewsletterForm(data=initial)
        self.assertTrue(form.is_valid())
        self.assertEqual(title, form.cleaned_data["title"])


@mock.patch("bedrock.newsletter.utils.get_newsletters", newsletters_mock)
class TestNewsletterFooterForm(TestCase):
    newsletter_name = "mozilla-and-you"

    def test_form(self):
        """Form works normally"""
        data = {
            "email": "foo@example.com",
            "lang": "fr",
            "first_name": "Walter",
            "last_name": "Sobchak",
            "privacy": True,
            "source_url": "https://accounts.firefox.com",
            "newsletters": [self.newsletter_name],
        }
        form = NewsletterFooterForm(self.newsletter_name, locale="en-US", data=data.copy())
        self.assertTrue(form.is_valid(), form.errors)
        cleaned_data = form.cleaned_data
        self.assertEqual(data["lang"], cleaned_data["lang"])
        self.assertEqual(data["source_url"], cleaned_data["source_url"])

    def test_source_url_non_url(self):
        """Form works normally"""
        data = {
            "email": "foo@example.com",
            "lang": "fr",
            "first_name": "Walter",
            "last_name": "Sobchak",
            "privacy": True,
            "source_url": "about:devtools?dude=abiding",
            "newsletters": [self.newsletter_name],
        }
        form = NewsletterFooterForm(self.newsletter_name, locale="en-US", data=data.copy())
        self.assertTrue(form.is_valid(), form.errors)
        cleaned_data = form.cleaned_data
        self.assertEqual(data["source_url"], cleaned_data["source_url"])

    def test_source_url_too_long(self):
        """Form works normally"""
        data = {
            "email": "foo@example.com",
            "lang": "fr",
            "first_name": "Walter",
            "last_name": "Sobchak",
            "privacy": True,
            "source_url": "about:devtools" * 20,
            "newsletters": [self.newsletter_name],
        }
        form = NewsletterFooterForm(self.newsletter_name, locale="en-US", data=data.copy())
        self.assertTrue(form.is_valid(), form.errors)
        cleaned_data = form.cleaned_data
        self.assertEqual(data["source_url"][:255], cleaned_data["source_url"])

    def test_country_default(self):
        """country defaults based on the locale.

        But only for country based locales (e.g. pt-BR)"""
        form = NewsletterFooterForm(self.newsletter_name, locale="fr")
        self.assertEqual("", form.fields["country"].initial)
        form = NewsletterFooterForm(self.newsletter_name, locale="pt-BR")
        self.assertEqual("br", form.fields["country"].initial)
        form = NewsletterFooterForm(self.newsletter_name, locale="zh-TW")
        self.assertEqual("tw", form.fields["country"].initial)

    def test_lang_choices_per_newsletter(self):
        """Lang choices should be based on the newsletter."""
        form = NewsletterFooterForm("beta", "en-US")
        choices = [lang[0] for lang in form.fields["lang"].choices]
        self.assertEqual(choices, ["en"])

        form = NewsletterFooterForm("join-mozilla", "en-US")
        choices = [lang[0] for lang in form.fields["lang"].choices]
        self.assertEqual(choices, ["en", "es"])

    def test_lang_choices_multiple_newsletters(self):
        """Lang choices should be based on all newsletters."""
        form = NewsletterFooterForm("join-mozilla,firefox-tips", "en-US")
        choices = [lang[0] for lang in form.fields["lang"].choices]
        self.assertEqual(choices, ["de", "en", "es", "fr", "pt", "ru"])

    def test_lang_default(self):
        """lang defaults based on the locale"""
        form = NewsletterFooterForm(self.newsletter_name, locale="pt-BR")
        self.assertEqual("pt", form.fields["lang"].initial)

    def test_lang_default_not_supported(self):
        """lang defaults to blank if not supported by newsletter."""
        form = NewsletterFooterForm("beta", locale="pt-BR")
        self.assertEqual("", form.fields["lang"].initial)

    def test_lang_not_required(self):
        """lang not required since field not always displayed"""
        data = {
            "email": "foo@example.com",
            "privacy": True,
            "newsletters": [self.newsletter_name],
        }
        form = NewsletterFooterForm(self.newsletter_name, locale="en-US", data=data.copy())
        self.assertTrue(form.is_valid(), form.errors)
        # Form returns '' for lang, so we don't accidentally change the user's
        # preferred language thinking they entered something here that they
        # didn't.
        self.assertEqual("", form.cleaned_data["lang"])

    def test_privacy_required(self):
        """they have to check the privacy box"""
        data = {
            "email": "foo@example.com",
            "privacy": False,
            "newsletters": [self.newsletter_name],
        }
        form = NewsletterFooterForm(self.newsletter_name, locale="en-US", data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("privacy", form.errors)

    def test_invalid_newsletter_is_error(self):
        """Invalid newsletter should not raise exception. Bug 1072302.

        Instead, an invalid newsletter name should manifest as a normal
        form error.
        """
        data = {
            "email": "fred@example.com",
            "lang": "fr",
            "privacy": True,
            "newsletters": [],
        }
        form = NewsletterFooterForm("", locale="en-US", data=data.copy())
        self.assertFalse(form.is_valid())
        self.assertIn("newsletters", form.errors)
        self.assertEqual(form.errors["newsletters"], ["This field is required."])

        invalid_newsletter = "!nv@l1d"
        data = {
            "email": "fred@example.com",
            "lang": "fr",
            "privacy": True,
            "newsletters": [invalid_newsletter],
        }
        form = NewsletterFooterForm(invalid_newsletter, locale="en-US", data=data.copy())
        self.assertFalse(form.is_valid())
        self.assertIn("newsletters", form.errors)
        self.assertTrue(form.errors["newsletters"][0].startswith("Select a valid choice."))

    def test_multiple_newsletters(self):
        newsletters = ["mozilla-and-you", "beta"]
        spacey_newsletters = [f" {n} " for n in newsletters]
        data = {
            "email": "dude@example.com",
            "lang": "en",
            "privacy": "Y",
            "newsletters": newsletters,
        }
        form = NewsletterFooterForm(newsletters, "en-US", data=data.copy())
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["newsletters"], newsletters)

        # whitespace shouldn't matter
        form = NewsletterFooterForm(spacey_newsletters, "en-US", data=data.copy())
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["newsletters"], newsletters)
