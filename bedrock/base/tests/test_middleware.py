# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from contextlib import suppress
from unittest import mock

from django.http import HttpResponse
from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse

import pytest
from jinja2.exceptions import UndefinedError
from markus.testing import MetricsMock
from pytest_django.asserts import assertTemplateUsed

from bedrock.base.middleware import (
    BedrockLangCodeFixupMiddleware,
    BedrockLocaleMiddleware,
)


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
        (
            "/",
            302,
            "/de/",  # because accept-language header has de as default lang,
            None,
        ),
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
        ("/sco/", 200, None, "sco"),
        ("/de/path/to/thing/?lang=fr", 302, "/fr/path/to/thing/", None),
        ("/de/path/to/thing/?lang=vv", 302, "/en-US/path/to/thing/", None),
        ("/de/path/to/thing/?lang", 302, "/en-US/path/to/thing/", None),
        ("/de/path/to/thing/?lang=fr&test=true&foo=bar", 302, "/fr/path/to/thing/?test=true&foo=bar", None),
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
        "Unicode escaped during fixup",
        "Unicode accepted during pass-through",
        "Three-letter locale acceptable",
        "?lang querystring for valid locale",
        "?lang querystring for invalid locale",
        "?lang querystring with no value",
        "?lang querystring for valid locale and further querystrings",
    ],
)
def test_BedrockLangCodeFixupMiddleware(
    request_path,
    expected_status_code,
    expected_dest,
    expected_request_locale,
    rf,
):
    request = rf.get(
        request_path,
        HTTP_ACCEPT_LANGUAGE="de-DE,en-GB;q=0.4,en-US;q=0.2",
    )

    middleware = BedrockLangCodeFixupMiddleware(get_response=HttpResponse)

    resp = middleware.process_request(request)

    if resp:
        assert resp.status_code == 302
        assert resp.headers["location"] == expected_dest
    else:
        # the request will have been annotated by the middleware
        assert request.locale == expected_request_locale


@pytest.mark.django_db
def test_BedrockLangCodeFixupMiddleware__no_lang_info_gets_locale_page__end_to_end(client):
    """Quick end-to-end test confirming the custom 404-locale template is rendered
    at the / path when there is no accept-language header"""

    resp = client.get("/", follow=False)
    assert "HTTP_ACCEPT_LANGUAGE" not in resp.request
    assert resp.status_code == 200
    # this template use actually happens in lib.l10n_utils.render
    assertTemplateUsed(resp, "404-locale.html")


@mock.patch("django.middleware.locale.LocaleMiddleware.process_request")
@mock.patch("django.middleware.locale.LocaleMiddleware.process_response")
def test_BedrockLocaleMiddleware_skips_super_call_if_path_is_for_root_and_has_no_lang_clues(
    mock_django_localemiddleware_process_response,
    mock_django_localemiddleware_process_request,
    rf,
):
    fake_request = rf.get("/")
    assert "HTTP_ACCEPT_LANGUAGE" not in fake_request
    middleware = BedrockLocaleMiddleware(fake_request)
    middleware.process_request(fake_request)
    assert not mock_django_localemiddleware_process_request.called

    fake_response = mock.Mock(name="fake response")
    middleware.process_response(fake_request, fake_response)
    assert not mock_django_localemiddleware_process_response.called
