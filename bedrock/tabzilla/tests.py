from django.test import Client

from funfactory.urlresolvers import reverse

from bedrock.mozorg.tests import TestCase


class TabzillaViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_tabzilla_content_type(self):
        """ Content-Type header should be text/javascript. """
        with self.activate('en-US'):
            resp = self.client.get(reverse('tabzilla'))
        self.assertEqual(resp['content-type'], 'text/javascript')
