# -*- coding: utf-8 -*-

import os
from urlparse import parse_qs, urlparse

from django.conf import settings
from django.test.client import Client
from django.utils import unittest

from funfactory.urlresolvers import reverse
from mock import patch
from mozorg.tests import TestCase
from nose.tools import eq_, ok_
from platforms import load_devices
from pyquery import PyQuery as pq

from firefox import views as fx_views
from firefox.firefox_details import FirefoxDetails
from firefox.views import product_details


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
PROD_DETAILS_DIR = os.path.join(TEST_DATA_DIR, 'product_details_json')

with patch.object(settings, 'PROD_DETAILS_DIR', PROD_DETAILS_DIR):
    firefox_details = FirefoxDetails()


@patch.object(fx_views, 'firefox_details', firefox_details)
class TestFirefoxDetails(TestCase):

    def test_get_download_url(self):
        url = firefox_details.get_download_url('OS X', 'pt-BR', '17.0')
        self.assertDictEqual(parse_qs(urlparse(url).query),
                             {'lang': ['pt-BR'],
                              'os': ['osx'],
                              'product': ['firefox-17.0']})

    def test_filter_builds_by_locale_name(self):
        # search english
        builds = firefox_details.get_filtered_full_builds(
            firefox_details.latest_version('release'),
            'ujara'
        )
        eq_(len(builds), 1)
        eq_(builds[0]['name_en'], 'Gujarati')

        # search native
        builds = firefox_details.get_filtered_full_builds(
            firefox_details.latest_version('release'),
            u'જરા'
        )
        eq_(len(builds), 1)
        eq_(builds[0]['name_en'], 'Gujarati')


@patch.object(fx_views, 'firefox_details', firefox_details)
class TestFirefoxAll(TestCase):
    def setUp(self):
        self.client = Client()
        with self.activate('en-US'):
            self.url = reverse('firefox.all')

    def test_no_search_results(self):
        """
        Tables should be gone and not-found message should be shown when there
        are no search results.
        """
        resp = self.client.get(self.url + '?q=DOES_NOT_EXIST')
        doc = pq(resp.content)
        ok_(not doc('table.build-table'))
        ok_(not doc('.not-found.hide'))

    def test_no_search_query(self):
        """
        When not searching all builds should show.
        """
        resp = self.client.get(self.url)
        doc = pq(resp.content)
        eq_(len(doc('.build-table')), 2)
        eq_(len(doc('.not-found.hide')), 2)

        release = firefox_details.latest_version('release')
        num_builds = len(firefox_details.get_filtered_full_builds(release))
        num_builds += len(firefox_details.get_filtered_test_builds(release))
        eq_(len(doc('tr[data-search]')), num_builds)


class TestLoadDevices(unittest.TestCase):

    def file(self):
        # where should the test file go?
        return 'TODO'

    @unittest.skip('Please to write test')
    def test_load_devices(self):
        load_devices(self, self.file(), cacheDevices=False)

        #todo


@patch.object(fx_views, 'firefox_details', firefox_details)
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
