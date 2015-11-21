# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.test.utils import override_settings

from bedrock.mozorg.middleware import (ClacksOverheadMiddleware,
                                       CrossOriginResourceSharingMiddleware,
                                       HostnameMiddleware)
from bedrock.mozorg.tests import TestCase


class TestClacksOverheadMiddleware(TestCase):
    def setUp(self):
        self.middleware = ClacksOverheadMiddleware()
        self.request = HttpRequest()
        self.response = HttpResponse()

    def test_good_response_has_header(self):
        self.response.status_code = 200
        self.middleware.process_response(self.request, self.response)
        self.assertEqual(self.response['X-Clacks-Overhead'], 'GNU Terry Pratchett')

    def test_other_response_has_no_header(self):
        self.response.status_code = 301
        self.middleware.process_response(self.request, self.response)
        self.assertNotIn('X-Clacks-Overhead', self.response)

        self.response.status_code = 404
        self.middleware.process_response(self.request, self.response)
        self.assertNotIn('X-Clacks-Overhead', self.response)


class TestCrossOriginResourceSharingMiddleware(TestCase):
    def setUp(self):
        self.middleware = CrossOriginResourceSharingMiddleware()
        self.request = HttpRequest()
        self.response = HttpResponse()

    def test_match(self):
        self.request.path = '/foo/bar/baz/'

        cors_urls = {r'^/foo/bar': '*'}
        with self.settings(CORS_URLS=cors_urls):
            self.middleware.process_response(self.request, self.response)
            self.assertEqual(self.response['Access-Control-Allow-Origin'], '*')

    def test_middle_match(self):
        # Ensure that matches in the middle of the URL work.
        self.request.path = '/foo/bar/baz/'

        cors_urls = {r'/bar': '*'}
        with self.settings(CORS_URLS=cors_urls):
            self.middleware.process_response(self.request, self.response)
            self.assertEqual(self.response['Access-Control-Allow-Origin'], '*')

    def test_no_match(self):
        self.request.path = '/foo/bar/baz/'

        cors_urls = {r'^/biff/bak': '*'}
        with self.settings(CORS_URLS=cors_urls):
            self.middleware.process_response(self.request, self.response)
            self.assertFalse('Access-Control-Allow-Origin' in self.response)


class TestHostnameMiddleware(TestCase):
    @override_settings(HOSTNAME='foobar', DEIS_APP='bedrock-dev', DEIS_DOMAIN='example.com')
    def test_base(self):
        self.middleware = HostnameMiddleware()
        self.request = HttpRequest()
        self.response = HttpResponse()

        self.middleware.process_response(self.request, self.response)
        self.assertEqual(self.response['X-Backend-Server'], 'foobar.bedrock-dev.example.com')

    @override_settings(MIDDLEWARE_CLASSES=(list(settings.MIDDLEWARE_CLASSES) +
                                           ['bedrock.mozorg.middleware.HostnameMiddleware']),
                       HOSTNAME='foobar', DEIS_APP='el-dudarino')
    def test_request(self):
        response = self.client.get('/en-US/')
        self.assertEqual(response['X-Backend-Server'], 'foobar.el-dudarino')
