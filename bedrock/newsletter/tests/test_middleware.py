from mock import patch
from django.test import Client
from funfactory.urlresolvers import reverse
from lib import l10n_utils
from bedrock.mozorg.tests import TestCase
from nose.tools import eq_
from pyquery import PyQuery as pq


@patch.object(l10n_utils, 'lang_file_is_active', lambda *x: True)
class TestNewsletterFooter(TestCase):
    def setUp(self):
        self.view_name = 'firefox.fx'
        self.client = Client()

    def test_country_selected(self):
        """
        The correct country for the locale should be initially selected.
        """
        with self.activate('en-US'):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        eq_(doc('#id_country option[selected="selected"]').val(), 'us')

        with self.activate('fr'):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        eq_(doc('#id_country option[selected="selected"]').val(), 'fr')

        with self.activate('pt-BR'):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        eq_(doc('#id_country option[selected="selected"]').val(), 'br')

    def test_language_selected(self):
        """
        The correct language for the locale should be initially selected or
        'en' if it's not an option.
        """
        with self.activate('fr'):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        eq_(doc('#id_lang option[selected="selected"]').val(), 'fr')

        # with hyphenated regional locale, should have only lang
        with self.activate('pt-BR'):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        eq_(doc('#id_lang option[selected="selected"]').val(), 'pt')

        # not supported. should default to ''
        with self.activate('ak'):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        eq_(doc('#id_lang option[selected="selected"]').val(), '')
