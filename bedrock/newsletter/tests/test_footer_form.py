from bedrock.base.urlresolvers import reverse
from mock import patch
from nose.tools import eq_
from pyquery import PyQuery as pq

from bedrock.mozorg.tests import TestCase


@patch('bedrock.newsletter.forms.get_lang_choices',
       lambda *x: [['en', 'English'], ['fr', 'French'], ['pt', 'Portuguese']])
@patch('lib.l10n_utils.translations_for_template',
       lambda *x: ['en-US', 'fr', 'pt-BR', 'af'])
class TestNewsletterFooter(TestCase):
    def setUp(self):
        self.view_name = 'newsletter.subscribe'

    def test_country_selected(self):
        """
        The correct country for the locale should be initially selected.
        """
        with self.activate('en-US'):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        eq_(doc('#id_country option[selected="selected"]').val(), 'us')

        # no country in locale, no country selected
        with self.activate('fr'):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        eq_(doc('#id_country option[selected="selected"]').val(), '')

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
        with self.activate('af'):
            resp = self.client.get(reverse(self.view_name))
        doc = pq(resp.content)
        eq_(doc('#id_lang option[selected="selected"]').val(), '')
