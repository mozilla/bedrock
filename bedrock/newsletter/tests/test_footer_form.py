# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test.utils import override_settings

from mock import patch
from pyquery import PyQuery as pq

from bedrock.base.urlresolvers import reverse
from bedrock.mozorg.tests import TestCase


@patch("bedrock.newsletter.forms.get_lang_choices", lambda *x: [["en", "English"], ["fr", "French"], ["pt", "Portuguese"]])
class TestNewsletterFooter(TestCase):
    def setUp(self):
        self.view_name = "newsletter.subscribe"

    @override_settings(DEV=True)
    def test_country_selected(self):
        """
        The correct country for the locale should be initially selected.
        """
        with self.activate("en-US"):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        assert doc('#id_country option[selected="selected"]').val() == "us"

        # no country in locale, no country selected
        with self.activate("fr"):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        assert doc('#id_country option[selected="selected"]').val() == ""

        with self.activate("pt-BR"):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        assert doc('#id_country option[selected="selected"]').val() == "br"

    @override_settings(DEV=True)
    def test_language_selected(self):
        """
        The correct language for the locale should be initially selected or
        'en' if it's not an option.
        """
        with self.activate("fr"):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        assert doc('#id_lang option[selected="selected"]').val() == "fr"

        # with hyphenated regional locale, should have only lang
        with self.activate("pt-BR"):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        assert doc('#id_lang option[selected="selected"]').val() == "pt"

        # not supported. should default to ''
        with self.activate("af"):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        assert doc('#id_lang option[selected="selected"]').val() == ""
