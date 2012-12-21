from django.conf import settings
from django.test import Client

from funfactory.urlresolvers import reverse
from mock import patch

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
