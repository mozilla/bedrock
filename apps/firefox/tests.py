import unittest
from urlparse import parse_qs, urlparse

from django.test.client import Client

from funfactory.urlresolvers import reverse
from mock import patch
from mozorg.tests import TestCase
from nose.plugins.skip import SkipTest
from nose.tools import eq_
from platforms import load_devices

from firefox.firefox_details import firefox_details
from firefox.views import product_details


class TestFirefoxDetails(TestCase):
    def test_get_download_url(self):
        url = firefox_details.get_download_url('OS X', 'pt-BR', '17.0')
        self.assertDictEqual(parse_qs(urlparse(url).query),
                             {'lang': ['pt-BR'],
                              'os': ['osx'],
                              'product': ['firefox-17.0']})


class TestLoadDevices(unittest.TestCase):

    def file(self):
        # where should the test file go?
        return 'TODO'

    def test_load_devices(self):
        raise SkipTest
        devices = load_devices(self, self.file(), cacheDevices=False)

        #todo


class FxVersionRedirectsMixin(object):
    def test_non_firefox(self):
        user_agent = 'random'
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 301)
        eq_(response['Vary'], 'User-Agent')
        eq_(response['Location'],
            'http://testserver%s' % reverse('firefox.new'))

    def test_bad_firefox(self):
        user_agent = 'Mozilla/5.0 (SaferSurf) Firefox 1.5'
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 301)
        eq_(response['Vary'], 'User-Agent')
        eq_(response['Location'],
            'http://testserver%s' % reverse('firefox.update'))

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='14.0')
    def test_old_firefox(self):
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) '
                      'Gecko/20100101 Firefox/13.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 301)
        eq_(response['Vary'], 'User-Agent')
        eq_(response['Location'],
            'http://testserver%s' % reverse('firefox.update'))

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='13.0.5')
    def test_current_minor_version_firefox(self):
        """
        Should show current even if behind by a patch version
        """
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) '
                      'Gecko/20100101 Firefox/13.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='16.0')
    def test_current_firefox(self):
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:16.0) '
                      'Gecko/20100101 Firefox/16.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')

    @patch.dict(product_details.firefox_versions,
                LATEST_FIREFOX_VERSION='16.0')
    def test_future_firefox(self):
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:18.0) '
                      'Gecko/20100101 Firefox/18.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
        eq_(response['Vary'], 'User-Agent')


class TestWhatsnewRedirect(FxVersionRedirectsMixin, TestCase):
    def setUp(self):
        self.client = Client()
        with self.activate('en-US'):
            self.url = reverse('firefox.whatsnew', args=['13.0'])


class TestFirstrunRedirect(FxVersionRedirectsMixin, TestCase):
    def setUp(self):
        self.client = Client()
        with self.activate('en-US'):
            self.url = reverse('firefox.firstrun', args=['13.0'])
