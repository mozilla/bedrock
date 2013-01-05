from django.conf import settings
from django.test import Client

from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_

from mozorg.tests import TestCase


class TabzillaViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_tabzilla_content_type(self):
        """ Content-Type header should be text/javascript. """
        with self.activate('en-US'):
            resp = self.client.get(reverse('tabzilla'))
        self.assertEqual(resp['content-type'], 'text/javascript')


@patch.object(settings, 'DEV_LANGUAGES', ['en-US', 'de'])
@patch.object(settings, 'PROD_LANGUAGES', ['en-US', 'de'])
class TabzillaRedirectTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_locale_preserved(self):
        """The old tabzilla URL should preserve the locale through redirects."""
        resp = self.client.get('/de/tabzilla/media/js/tabzilla.js')
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp['Location'],
                         'http://testserver/de/tabzilla/tabzilla.js')

    @patch.object(settings, 'MEDIA_URL', '//example.com/')
    @patch.object(settings, 'TEMPLATE_DEBUG', False)
    def test_tabzilla_css_redirect(self):
        """
        Tabzilla css redirect should use MEDIA_URL setting and switch
        based on TEMPLATE_DEBUG setting.
        Bug 826866.
        """
        tabzilla_css_url = '/en-US/tabzilla/media/css/tabzilla.css'
        with self.activate('en-US'):
            response = self.client.get(tabzilla_css_url)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'http://example.com/css/tabzilla-min.css')

        with patch.object(settings, 'TEMPLATE_DEBUG', True):
            with self.activate('en-US'):
                response = self.client.get(tabzilla_css_url)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'http://example.com/css/tabzilla.less.css')
