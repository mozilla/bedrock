# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from contextlib import suppress

from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse

import pytest
from jinja2.exceptions import UndefinedError
from markus.testing import MetricsMock

from bedrock.base.middleware import BedrockLangCodeFixupMiddleware


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


@pytest.mark.parametrize(
    "request_path, expected_status_code, expected_dest, expected_request_locale",
    (
        ("/", 302, "/en-US/", None),
        ("/en-us/", 302, "/en-US/", None),
        ("/en-US/", 200, None, "en-US"),
        ("/de/", 200, None, "de"),
        ("/en-US/i/am/a/path/", 200, None, "en-US"),
        ("/de/i/am/a/path/", 200, None, "de"),
        ("/en-us/path/to/thing/", 302, "/en-US/path/to/thing/", None),
        ("/de-AT/path/to/thing/", 302, "/de/path/to/thing/", None),
        ("/es-mx/path/here?to=thing&test=true", 302, "/es-MX/path/here?to=thing&test=true", None),
        ("/en-us/path/to/an/éclair/", 302, "/en-US/path/to/an/%C3%A9clair/", None),
        ("/it/path/to/an/éclair/", 200, None, "it"),
        ("/ach/", 200, None, "ach"),
    ),
    ids=[
        "Bare root path",
        "Lowercase lang code for root path",
        "No change needed for root path with good locale 1",
        "No change needed for root path with good locale 2",
        "No change needed for deep path with good locale 1",
        "No change needed for deep path with good locale 2",
        "Lowercase lang code for deeper path",
        "Unsuported lang goes to root supported lang code",
        "Querystrings are preserved during fixup",
        "Unicode preserved during fixup",
        "Unicode preserved during pass-through",
        "Three-letter locale acceptable",
    ],
)
def test_BedrockLangCodeFixupMiddleware(
    request_path,
    expected_status_code,
    expected_dest,
    expected_request_locale,
    rf,
):
    request = rf.get(request_path)

    middleware = BedrockLangCodeFixupMiddleware()

    resp = middleware.process_request(request)

    if resp:
        assert resp.status_code == 302
        assert resp.headers["location"] == expected_dest
    else:
        # the request will have been annotated by the middleware
        assert request.locale == expected_request_locale
