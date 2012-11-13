from mozorg.tests import TestCase

from django.test.client import Client

from funfactory.urlresolvers import reverse
from nose.tools import eq_
from pyquery import PyQuery as pq


class TestNewsletter(TestCase):
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
        en-US if it's not an option.
        """
        with self.activate('fr'):
            resp = self.client.get(reverse(self.view_name))

        doc = pq(resp.content)
        eq_(doc('#id_lang option[selected="selected"]').val(), 'fr')

        with self.activate('pt-BR'):
            resp = self.client.get(reverse(self.view_name))

        doc = pq(resp.content)
        eq_(doc('#id_lang option[selected="selected"]').val(), 'pt-BR')

        with self.activate('ak'):
            resp = self.client.get(reverse(self.view_name))

        doc = pq(resp.content)
        eq_(doc('#id_lang option[selected="selected"]').val(), 'en-US')
