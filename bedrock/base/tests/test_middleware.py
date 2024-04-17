# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from contextlib import suppress

from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse

from jinja2.exceptions import UndefinedError
from markus.testing import MetricsMock


@override_settings(
    MIDDLEWARE=["bedrock.base.middleware.MetricsStatusMiddleware"],
    ROOT_URLCONF="bedrock.base.tests.urls",
)
class TestMetricsStatusMiddleware(TestCase):
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


@override_settings(
    MIDDLEWARE=["bedrock.base.middleware.MetricsViewTimingMiddleware"],
    ROOT_URLCONF="bedrock.base.tests.urls",
    ENABLE_METRICS_VIEW_TIMING_MIDDLEWARE=True,
)
class TestMetricsViewTimingMiddleware(TestCase):
    @override_settings(ENABLE_METRICS_VIEW_TIMING_MIDDLEWARE=False)
    def test_200_disabled(self):
        with MetricsMock() as mm:
            resp = Client().get(reverse("index"))
            assert resp.status_code == 200
            mm.assert_not_timing("view.timings")

    def test_200(self):
        with MetricsMock() as mm:
            resp = Client().get(reverse("index"))
            assert resp.status_code == 200
            mm.assert_timing_once(
                "view.timings",
                tags=["view_path:bedrock.base.tests.urls.index.GET", "module:bedrock.base.tests.urls.GET", "method:GET", "status_code:200"],
            )

    def test_302(self):
        with MetricsMock() as mm:
            resp = Client().get(reverse("redirect"))
            assert resp.status_code == 302
            mm.assert_timing_once(
                "view.timings",
                tags=["view_path:bedrock.base.tests.urls.redirect.GET", "module:bedrock.base.tests.urls.GET", "method:GET", "status_code:302"],
            )

    def test_raises_404(self):
        with MetricsMock() as mm:
            with suppress(UndefinedError):
                resp = Client().get(reverse("raises_404"))
                assert resp.status_code == 404
            mm.assert_timing_once(
                "view.timings",
                tags=["view_path:bedrock.base.tests.urls.raises_404.GET", "module:bedrock.base.tests.urls.GET", "method:GET", "status_code:404"],
            )

    def test_returns_404(self):
        with MetricsMock() as mm:
            resp = Client().get(reverse("returns_404"))
            assert resp.status_code == 404
            mm.assert_timing_once(
                "view.timings",
                tags=["view_path:bedrock.base.tests.urls.returns_404.GET", "module:bedrock.base.tests.urls.GET", "method:GET", "status_code:404"],
            )

    def test_raises_500(self):
        with MetricsMock() as mm:
            with suppress(UndefinedError):
                resp = Client().get(reverse("raises_500"))
                assert resp.status_code == 500
            mm.assert_timing_once(
                "view.timings",
                tags=["view_path:bedrock.base.tests.urls.raises_500.GET", "module:bedrock.base.tests.urls.GET", "method:GET", "status_code:500"],
            )

    def test_returns_500(self):
        with MetricsMock() as mm:
            resp = Client().get(reverse("returns_500"))
            assert resp.status_code == 500
            mm.assert_timing_once(
                "view.timings",
                tags=["view_path:bedrock.base.tests.urls.returns_500.GET", "module:bedrock.base.tests.urls.GET", "method:GET", "status_code:500"],
            )


class BedrockLangCodeFixupMiddlewareTests(TestCase):
    def test_reminder(self):
        # Ensure all methods of the middleware are tested
        self.fail("WRITE ME ONCE OVERALL FLOW IS STABLE AGAIN. MUST DO EVERYTHING THAT IS PROMISED IN THE DOCSTRING")

        self.fail("Ensure we have unicode tests too")


class BedrockLangPatchingLocaleMiddlewareTests(TestCase):
    def test_reminder(self):
        # Ensure all methods of the middleware are tested
        self.fail("WRITE ME ONCE OVERALL FLOW IS STABLE AGAIN")
