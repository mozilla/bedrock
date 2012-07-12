import unittest

from django.test.client import Client

from funfactory.urlresolvers import reverse
from mozorg.tests import TestCase
from nose.plugins.skip import SkipTest
from nose.tools import eq_
from product_details import product_details
from platforms import load_devices


class TestLoadDevices(unittest.TestCase):

    def file(self):
        # where should the test file go?
        return 'TODO'

    def test_load_devices(self):
        raise SkipTest
        devices = load_devices(self, self.file(), cacheDevices=False)

        #todo


class TestWhatsnewRedirect(TestCase):
    def setUp(self):
        self.client = Client()
        with self.activate('en-US'):
            self.url = reverse('firefox.whatsnew', args=['13.0'])

    def test_non_firefox(self):
        user_agent = 'random'
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 302)
        eq_(response['Location'],
            'http://testserver%s' % reverse('firefox.new'))

    def test_old_firefox(self):
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) '
                      'Gecko/20100101 Firefox/13.0')
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 302)
        eq_(response['Location'],
            'http://testserver%s' % reverse('firefox.update'))

    def test_current_firefox(self):
        current = product_details.firefox_versions['LATEST_FIREFOX_VERSION']
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:%s) '
                      'Gecko/20100101 Firefox/%s' % (current, current))
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)

    def test_future_firefox(self):
        future = product_details.firefox_versions['FIREFOX_AURORA']
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:%s) '
                      'Gecko/20100101 Firefox/%s' % (future, future))
        response = self.client.get(self.url, HTTP_USER_AGENT=user_agent)
        eq_(response.status_code, 200)
