# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from contextlib import suppress

from django.test import Client, RequestFactory, TestCase
from django.test.utils import override_settings
from django.urls import reverse

from jinja2.exceptions import UndefinedError
from markus.testing import MetricsMock

from bedrock.base.middleware import LocaleURLMiddleware


@override_settings(DEV=True)
class TestLocaleURLMiddleware(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.middleware = LocaleURLMiddleware()

    @override_settings(DEV_LANGUAGES=("de", "fr"))
    def test_matching_locale(self):
        locale = "fr"
        path = "/the/dude/"
        full_path = f"/{locale}{path}"
        req = self.rf.get(full_path)
        self.middleware.process_request(req)
        self.assertEqual(req.path_info, path)
        self.assertEqual(req.locale, "fr")

    @override_settings(DEV_LANGUAGES=("de", "fr"))
    def test_non_matching_locale(self):
        locale = "zh"
        path = "/the/dude/"
        full_path = f"/{locale}{path}"
        req = self.rf.get(full_path)
        self.middleware.process_request(req)
        self.assertEqual(req.path_info, full_path)
        self.assertEqual(req.locale, "")

    @override_settings(DEV_LANGUAGES=("zh-CN", "zh-TW"))
    def test_matching_main_language_to_sub_language(self):
        locale = "zh"
        path = "/the/dude/"
        full_path = f"/{locale}{path}"
        req = self.rf.get(full_path)
        self.middleware.process_request(req)
        self.assertEqual(req.path_info, path)
        self.assertEqual(req.locale, "zh-CN")

    @override_settings(DEV_LANGUAGES=("es-ES", "fr"))
    def test_matching_canonical(self):
        locale = "es"
        path = "/the/dude/"
        full_path = f"/{locale}{path}"
        req = self.rf.get(full_path)
        self.middleware.process_request(req)
        self.assertEqual(req.path_info, path)
        self.assertEqual(req.locale, "es-ES")


@override_settings(
    MIDDLEWARE=["bedrock.base.middleware.MetricsStatusMiddleware"],
    ROOT_URLCONF="bedrock.base.tests.urls",
)
class TestMetricsMiddleware(TestCase):
    def test_200(self):
        with MetricsMock() as mm:
            resp = Client().get(reverse("index"))
            assert resp.status_code == 200
            mm.assert_incr_once("response.status", tags=["status_code:200"])

    def test_302(self):
        with MetricsMock() as mm:
            resp = Client().get(reverse("redirect"))
            assert resp.status_code == 302
            mm.assert_incr_once("response.status", tags=["status_code:302"])

    def test_returns_400(self):
        with MetricsMock() as mm:
            with suppress(UndefinedError):
                resp = Client().get(reverse("returns_400"))
                assert resp.status_code == 400
            mm.assert_incr_once("response.status", tags=["status_code:400"])

    def test_raises_400_bad_request(self):
        with MetricsMock() as mm:
            with suppress(UndefinedError):
                resp = Client().get(reverse("raises_400_bad_request"))
                assert resp.status_code == 400
            mm.assert_incr_once("response.status", tags=["status_code:400"])

    def test_raises_400_multipart_parser_error(self):
        with MetricsMock() as mm:
            with suppress(UndefinedError):
                resp = Client().get(reverse("raises_400_multipart_parser_error"))
                assert resp.status_code == 400
            mm.assert_incr_once("response.status", tags=["status_code:400"])

    def test_raises_400_suspicious_operation(self):
        with MetricsMock() as mm:
            with suppress(UndefinedError):
                resp = Client().get(reverse("raises_400_suspicious_operation"))
                assert resp.status_code == 400
            mm.assert_incr_once("response.status", tags=["status_code:400"])

    def test_raises_403_permission_denied(self):
        with MetricsMock() as mm:
            with suppress(UndefinedError):
                resp = Client().get(reverse("raises_403_permission_denied"))
                assert resp.status_code == 403
            mm.assert_incr_once("response.status", tags=["status_code:403"])

    def test_raises_404(self):
        with MetricsMock() as mm:
            with suppress(UndefinedError):
                resp = Client().get(reverse("raises_404"))
                assert resp.status_code == 404
            mm.assert_incr_once("response.status", tags=["status_code:404"])

    def test_returns_404(self):
        with MetricsMock() as mm:
            resp = Client().get(reverse("returns_404"))
            assert resp.status_code == 404
            mm.assert_incr_once("response.status", tags=["status_code:404"])

    def test_raises_500(self):
        with MetricsMock() as mm:
            with suppress(UndefinedError):
                resp = Client().get(reverse("raises_500"))
                assert resp.status_code == 500
            mm.assert_incr_once("response.status", tags=["status_code:500"])

    def test_returns_500(self):
        with MetricsMock() as mm:
            resp = Client().get(reverse("returns_500"))
            assert resp.status_code == 500
            mm.assert_incr_once("response.status", tags=["status_code:500"])
