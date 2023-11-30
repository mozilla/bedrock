# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.test.utils import override_settings

from freezegun import freeze_time

from bedrock.mozorg.middleware import CacheMiddleware, ClacksOverheadMiddleware, HostnameMiddleware
from bedrock.mozorg.tests import TestCase


class TestCacheMiddleware(TestCase):
    def setUp(self):
        self.middleware = CacheMiddleware()
        self.request = HttpRequest()
        self.response = HttpResponse()

    @freeze_time("2023-01-01 00:00:00.123456")
    def test_good_response_has_headers(self):
        for method in ("GET", "HEAD"):
            for status in (200, 301, 302, 403, 404, 500):
                self.request.method = method
                self.response.status_code = status
                self.middleware.process_response(self.request, self.response)
                self.assertEqual(self.response["Cache-Control"], "max-age=600")
                self.assertEqual(self.response["Expires"], "Sun, 01 Jan 2023 00:10:00 GMT")

    def test_no_caching_methods(self):
        for method in ("POST", "PUT", "DELETE", "OPTIONS"):
            self.request.method = method
            self.response.status_code = 200
            self.middleware.process_response(self.request, self.response)
            self.assertNotIn("Cache-Control", self.response)
            self.assertNotIn("Expires", self.response)

    def test_no_caching_headers(self):
        self.request.method = "GET"
        self.response.status_code = 200
        self.response["Cache-Control"] = "no-cache"
        self.middleware.process_response(self.request, self.response)
        self.assertEqual(self.response["Cache-Control"], "no-cache")
        self.assertNotIn("Expires", self.response)

    def test_no_cache_streaming_response(self):
        self.request.method = "GET"
        self.response.status_code = 200
        self.response.streaming = True
        self.middleware.process_response(self.request, self.response)
        self.assertNotIn("Cache-Control", self.response)
        self.assertNotIn("Expires", self.response)


class TestClacksOverheadMiddleware(TestCase):
    def setUp(self):
        self.middleware = ClacksOverheadMiddleware()
        self.request = HttpRequest()
        self.response = HttpResponse()

    def test_good_response_has_header(self):
        self.response.status_code = 200
        self.middleware.process_response(self.request, self.response)
        self.assertEqual(self.response["X-Clacks-Overhead"], "GNU Terry Pratchett")

    def test_other_response_has_no_header(self):
        self.response.status_code = 301
        self.middleware.process_response(self.request, self.response)
        self.assertNotIn("X-Clacks-Overhead", self.response)

        self.response.status_code = 404
        self.middleware.process_response(self.request, self.response)
        self.assertNotIn("X-Clacks-Overhead", self.response)


@override_settings(ENABLE_HOSTNAME_MIDDLEWARE=True)
class TestHostnameMiddleware(TestCase):
    @override_settings(HOSTNAME="foobar", CLUSTER_NAME="oregon-b")
    def test_base(self):
        self.middleware = HostnameMiddleware()
        self.request = HttpRequest()
        self.response = HttpResponse()

        self.middleware.process_response(self.request, self.response)
        self.assertEqual(self.response["X-Backend-Server"], "foobar.oregon-b")

    @override_settings(
        MIDDLEWARE=(list(settings.MIDDLEWARE) + ["bedrock.mozorg.middleware.HostnameMiddleware"]),
        HOSTNAME="foobar",
        CLUSTER_NAME="el-dudarino",
    )
    def test_request(self):
        response = self.client.get("/en-US/")
        self.assertEqual(response["X-Backend-Server"], "foobar.el-dudarino")
