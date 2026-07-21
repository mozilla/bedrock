# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.conf import settings
from django.test.utils import override_settings

from pyquery import PyQuery as pq
from waffle.testutils import override_switch

from bedrock.base.urlresolvers import reverse
from bedrock.mozorg.tests import TestCase
from bedrock.newsletter.forms import get_lang_choices


@patch("bedrock.newsletter.forms.get_lang_choices", lambda *args, **kwargs: [["en", "English"], ["fr", "French"], ["pt", "Portuguese"]])
class TestNewsletterFooter(TestCase):
    def setUp(self):
        self.view_name = "newsletter.subscribe"

    @override_settings(DEV=True)
    def test_country_selected(self):
        """
        The correct country for the locale should be initially selected.
        """
        with self.activate_locale("en-US"):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        assert doc('#id_country option[selected="selected"]').val() == "us"

        # no country in locale, no country selected
        with self.activate_locale("fr"):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        assert doc('#id_country option[selected="selected"]').val() == ""

        with self.activate_locale("pt-BR"):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        assert doc('#id_country option[selected="selected"]').val() == "br"

    @override_settings(DEV=True)
    def test_language_selected(self):
        """
        The correct language for the locale should be initially selected or
        'en' if it's not an option.
        """
        for foundation_separate_newsletter_enabled in (True, False):
            with self.subTest(foundation_separate_newsletter_enabled=foundation_separate_newsletter_enabled):
                with override_switch("FOUNDATION_SEPARATE_NEWSLETTER", active=foundation_separate_newsletter_enabled):
                    with self.activate_locale("fr"):
                        resp = self.client.get(reverse(self.view_name))
                    doc = pq(resp.content)
                    assert doc('#id_lang option[selected="selected"]').val() == "fr"

                    # with hyphenated regional locale, should have only lang
                    with self.activate_locale("pt-BR"):
                        resp = self.client.get(reverse(self.view_name))
                    doc = pq(resp.content)
                    assert doc('#id_lang option[selected="selected"]').val() == "pt"

                    # not supported. should default to ''
                    with self.activate_locale("af"):
                        resp = self.client.get(reverse(self.view_name))
                    doc = pq(resp.content)
                    assert doc('#id_lang option[selected="selected"]').val() == ""

    @override_settings(DEV=True)
    def test_newsletter_action(self):
        """
        Newsletter points to correct POST URL.
        """

        with override_switch("FOUNDATION_SEPARATE_NEWSLETTER", active=True):
            with self.activate_locale("en-US"):
                resp = self.client.get(reverse(self.view_name))
            doc = pq(resp.content)
            assert doc("#newsletter-form").attr("action") == settings.FOUNDATION_SUBSCRIBE_URL

        with override_switch("FOUNDATION_SEPARATE_NEWSLETTER", active=False):
            with self.activate_locale("en-US"):
                resp = self.client.get(reverse(self.view_name))
            doc = pq(resp.content)
            assert doc("#newsletter-form").attr("action") == settings.BASKET_SUBSCRIBE_URL


@patch(
    "bedrock.newsletter.utils.get_languages_for_newsletters",
    lambda x: ["en", "ru", "it"],
)
class TestNewsletterFormGetLangChoicesHelper(TestCase):
    def test_get_lang_choices__no_override(self):
        fake_newsletters_param = [1, 2, 3]
        lang_choices = get_lang_choices(fake_newsletters_param)
        self.assertEqual(lang_choices, [["en", "English"], ["it", "Italiano"], ["ru", "Русский"]])

    def test_get_lang_choices__with_override(self):
        fake_newsletters_param = [1, 2, 3]
        lang_choices = get_lang_choices(
            fake_newsletters_param,
            languages_override=["it", "pt-BR", "sv"],
        )
        self.assertEqual(lang_choices, [["it", "Italiano"], ["pt-BR", "Português"], ["sv", "Svenska"]])
