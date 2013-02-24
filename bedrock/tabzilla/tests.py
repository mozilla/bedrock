from math import floor
import time
from hashlib import md5

from django.conf import settings
from django.test import Client
from django.utils.http import parse_http_date

from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_

from bedrock.mozorg.tests import TestCase


class TabzillaViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_tabzilla_content_type(self):
        """ Content-Type header should be text/javascript. """
        with self.activate('en-US'):
            resp = self.client.get(reverse('tabzilla'))
        self.assertEqual(resp['content-type'], 'text/javascript')

    def test_cache_headers(self):
        """
        Should have appropriate Cache-Control, Expires, and ETag headers.
        """
        with self.activate('en-US'):
            resp = self.client.get(reverse('tabzilla'))
        self.assertEqual(resp['cache-control'], 'max-age=43200')  # 12h

        now_date = floor(time.time())
        exp_date = parse_http_date(resp['expires'])
        self.assertAlmostEqual(now_date + 43200, exp_date, delta=2)

        etag = '"%s"' % md5(resp.content).hexdigest()
        self.assertEqual(resp['etag'], etag)


@patch.object(settings, 'DEV_LANGUAGES', ['en-US', 'de'])
@patch.object(settings, 'PROD_LANGUAGES', ['en-US', 'de'])
class TabzillaRedirectTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_locale_preserved(self):
        """The tabzilla URL should preserve the locale through redirects."""
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
        eq_(response['Location'], 'http://example.com/css/tabzilla/tabzilla-min.css')

        with patch.object(settings, 'TEMPLATE_DEBUG', True):
            with self.activate('en-US'):
                response = self.client.get(tabzilla_css_url)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'http://example.com/css/tabzilla/tabzilla.less.css')

    @patch('jingo_minify.helpers.build_less')
    def test_tabzilla_css_less_processing(self, less_mock):
        """
        The tabzilla.less file should be compiled by the redirect if
        settings.LESS_PREPROCESS is True.
        """
        tabzilla_css_url = '/en-US/tabzilla/media/css/tabzilla.css'
        with patch.object(settings, 'LESS_PREPROCESS', False):
            with self.activate('en-US'):
                self.client.get(tabzilla_css_url)
        eq_(less_mock.call_count, 0)

        with patch.object(settings, 'LESS_PREPROCESS', True):
            with self.activate('en-US'):
                self.client.get(tabzilla_css_url)
        eq_(less_mock.call_count, 1)
