# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from contextlib import suppress
from importlib import reload
from unittest import mock

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponse
from django.test import Client, RequestFactory, TestCase
from django.test.utils import override_settings
from django.urls import reverse

import csp.constants
import pytest
from jinja2.exceptions import UndefinedError
from markus.testing import MetricsMock
from pytest_django.asserts import assertTemplateUsed

from bedrock.base.middleware import (
    BasicAuthMiddleware,
    BedrockLangCodeFixupMiddleware,
    BedrockLocaleMiddleware,
    CSPMiddlewareByPathPrefix,
    SyntheticServerErrorMiddleware,
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

    def test_raises_410(self):
        with MetricsMock() as mm:
            with suppress(UndefinedError):
                resp = Client().get(reverse("raises_410"))
                assert resp.status_code == 410
            mm.assert_incr_once("response.status", tags=["status_code:410"])

    def test_returns_410(self):
        with MetricsMock() as mm:
            resp = Client().get(reverse("returns_410"))
            assert resp.status_code == 410
            mm.assert_incr_once("response.status", tags=["status_code:410"])

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

    def test_raises_410(self):
        with MetricsMock() as mm:
            with suppress(UndefinedError):
                resp = Client().get(reverse("raises_410"))
                assert resp.status_code == 410
            mm.assert_timing_once(
                "view.timings",
                tags=["view_path:bedrock.base.tests.urls.raises_410.GET", "module:bedrock.base.tests.urls.GET", "method:GET", "status_code:410"],
            )

    def test_returns_410(self):
        with MetricsMock() as mm:
            resp = Client().get(reverse("returns_410"))
            assert resp.status_code == 410
            mm.assert_timing_once(
                "view.timings",
                tags=["view_path:bedrock.base.tests.urls.returns_410.GET", "module:bedrock.base.tests.urls.GET", "method:GET", "status_code:410"],
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
        assert resp.headers["vary"].lower() == "accept-language"
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


@pytest.fixture
def csp_middleware():
    return CSPMiddlewareByPathPrefix(lambda req: HttpResponse())


@override_settings(
    CONTENT_SECURITY_POLICY={"DIRECTIVES": {"default-src": ["default.com"]}},
    CONTENT_SECURITY_POLICY_REPORT_ONLY=None,
)
def test_no_csp_path_overrides(csp_middleware):
    rf = RequestFactory()
    request = rf.get("/u/thedude/")
    response = csp_middleware.process_response(request, HttpResponse())
    assert not hasattr(response, "_csp_config")
    assert not hasattr(response, "_csp_config_ro")
    assert csp.constants.HEADER in response.headers
    assert csp.constants.HEADER_REPORT_ONLY not in response.headers
    assert response.headers[csp.constants.HEADER] == "default-src default.com"


@override_settings(
    CONTENT_SECURITY_POLICY={"DIRECTIVES": {"default-src": ["default.com"]}},
    CONTENT_SECURITY_POLICY_REPORT_ONLY=None,
    CSP_PATH_OVERRIDES={"/u/thedude": {"DIRECTIVES": {"default-src": ["override.com"]}}},
)
def test_csp_path_overrides(csp_middleware):
    rf = RequestFactory()
    request = rf.get("/u/thedude/")
    response = csp_middleware.process_response(request, HttpResponse())
    assert response._csp_config == {"default-src": ["override.com"]}
    assert not hasattr(response, "_csp_config_ro")
    assert csp.constants.HEADER in response.headers
    assert csp.constants.HEADER_REPORT_ONLY not in response.headers
    assert response.headers[csp.constants.HEADER] == "default-src override.com"


@override_settings(
    CONTENT_SECURITY_POLICY={"DIRECTIVES": {"default-src": ["default.com"]}},
    CONTENT_SECURITY_POLICY_REPORT_ONLY=None,
    CSP_PATH_OVERRIDES={"/u/thedude": {"DIRECTIVES": {}}},
)
def test_csp_path_overrides_nullify(csp_middleware):
    rf = RequestFactory()
    request = rf.get("/u/thedude/")
    response = csp_middleware.process_response(request, HttpResponse())
    assert response._csp_config == {}
    assert not hasattr(response, "_csp_config_ro")
    assert csp.constants.HEADER not in response.headers
    assert csp.constants.HEADER_REPORT_ONLY not in response.headers


@override_settings(
    CONTENT_SECURITY_POLICY={"DIRECTIVES": {"default-src": ["default.com"]}},
    CONTENT_SECURITY_POLICY_REPORT_ONLY={"DIRECTIVES": {"default-src": ["default.com", "other.com"]}},
    CSP_PATH_OVERRIDES_REPORT_ONLY={"/u/thedude": {"DIRECTIVES": {"default-src": ["override.com"]}}},
)
def test_csp_path_overrides_report_only(csp_middleware):
    rf = RequestFactory()
    request = rf.get("/u/thedude/")
    response = csp_middleware.process_response(request, HttpResponse())
    assert response._csp_config_ro == {"default-src": ["override.com"]}
    assert not hasattr(response, "_csp_config")
    assert csp.constants.HEADER in response.headers
    assert csp.constants.HEADER_REPORT_ONLY in response.headers
    assert response.headers[csp.constants.HEADER] == "default-src default.com"
    assert response.headers[csp.constants.HEADER_REPORT_ONLY] == "default-src override.com"


@override_settings(
    CONTENT_SECURITY_POLICY={"REPORT_PERCENTAGE": 0, "DIRECTIVES": {"default-src": ["default.com"]}},
    CONTENT_SECURITY_POLICY_REPORT_ONLY={"REPORT_PERCENTAGE": 100, "DIRECTIVES": {"default-src": ["default.com"], "report-uri": ["report.com"]}},
)
def test_csp_report_percentage_zero(csp_middleware):
    rf = RequestFactory()
    request = rf.get("/u/thedude/")
    response = csp_middleware.process_response(request, HttpResponse())
    assert csp.constants.HEADER in response.headers
    assert csp.constants.HEADER_REPORT_ONLY in response.headers
    assert "report-uri" not in response.headers[csp.constants.HEADER]
    assert "report-uri" in response.headers[csp.constants.HEADER_REPORT_ONLY]


@mock.patch.dict("os.environ", {"CSP_REPORT_PERCENTAGE": "0.5"})
def test_csp_report_percentage_can_be_float():
    # Test report percentage is cast to a float.
    from bedrock import settings

    # Force settings to reload pulling in the mocked environ
    reload(settings)

    assert settings.CONTENT_SECURITY_POLICY["REPORT_PERCENTAGE"] == 0.5
    assert settings.CONTENT_SECURITY_POLICY_REPORT_ONLY is None


@mock.patch.dict("os.environ", {"CSP_REPORT_URI": "/_the_csp_dude"}, clear=True)
def test_csp_report_uri():
    # Test if report-uri is set it is added to CSP config.
    from bedrock import settings

    # Force settings to reload pulling in the mocked environ
    reload(settings)

    assert settings.csp_report_uri == "/_the_csp_dude"
    assert settings.CONTENT_SECURITY_POLICY["DIRECTIVES"]["report-uri"] == "/_the_csp_dude"
    assert settings.csp_ro_report_uri is None
    assert settings.CONTENT_SECURITY_POLICY_REPORT_ONLY is None


@mock.patch.dict("os.environ", {"CSP_REPORT_URI": "/_the_csp_dude", "CSP_RO_REPORT_URI": "/_csp_ro"}, clear=True)
def test_csp_ro_report_uri():
    # Test if report-only report-uri is set it is added to CSP config.
    from bedrock import settings

    # Force settings to reload pulling in the mocked environ
    reload(settings)

    assert settings.csp_report_uri == "/_the_csp_dude"
    assert settings.CONTENT_SECURITY_POLICY["DIRECTIVES"]["report-uri"] == "/_the_csp_dude"
    assert settings.csp_ro_report_uri == "/_csp_ro"
    assert settings.CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["report-uri"] == "/_csp_ro"


# --- SyntheticServerErrorMiddleware ---------------------------------------

# A valid 64-char token for use in tests. Value itself is not sensitive; it's
# just something the length check will accept.
_VALID_TOKEN = "a" * 64


def _passthrough_response(request):
    return HttpResponse("real response", status=200)


def test_synthetic_500_middleware_no_op_when_token_unset(rf):
    with override_settings(SYNTHETIC_5XX_TOKEN=""):
        with pytest.raises(MiddlewareNotUsed):
            SyntheticServerErrorMiddleware(get_response=_passthrough_response)


def test_synthetic_500_middleware_refuses_short_configured_token(rf):
    # If the configured token isn't exactly 64 chars, the middleware refuses to
    # arm itself. Prevents accidental weak-token config from silently working.
    with override_settings(SYNTHETIC_5XX_TOKEN="short"):
        with pytest.raises(MiddlewareNotUsed):
            SyntheticServerErrorMiddleware(get_response=_passthrough_response)


def test_synthetic_500_middleware_refuses_long_configured_token(rf):
    with override_settings(SYNTHETIC_5XX_TOKEN="a" * 65):
        with pytest.raises(MiddlewareNotUsed):
            SyntheticServerErrorMiddleware(get_response=_passthrough_response)


def test_synthetic_500_middleware_refuses_non_ascii_configured_token(rf):
    # A 64-char token containing non-ASCII has a UTF-8 byte length != 64, so
    # no request could ever match it. Refuse to arm rather than run a
    # middleware that can never fire.
    with override_settings(SYNTHETIC_5XX_TOKEN="é" * 64):
        with pytest.raises(MiddlewareNotUsed):
            SyntheticServerErrorMiddleware(get_response=_passthrough_response)


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_fires_on_matching_header(rf):
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    request = rf.get("/en-US/", HTTP_X_MOZILLA_OPS_CANARY=_VALID_TOKEN)
    response = middleware(request)
    assert response.status_code == 500
    assert b"synthetic 500" in response.content


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_synthetic_response_has_no_cache_override(rf):
    # We deliberately do NOT set Cache-Control: no-store or Surrogate-Control on
    # the synthetic response, even as belt-and-braces against caching a 500.
    # In Dev testing, those headers caused Fastly to enter pass state before
    # our failover cascade in vcl_fetch got a look, suppressing the restart.
    # Fastly's default behaviour already avoids caching 5xx.
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    request = rf.get("/en-US/", HTTP_X_MOZILLA_OPS_CANARY=_VALID_TOKEN)
    response = middleware(request)
    assert response.status_code == 500
    assert "Cache-Control" not in response
    assert "Surrogate-Control" not in response


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_passthrough_without_header(rf):
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    request = rf.get("/en-US/")
    response = middleware(request)
    assert response.status_code == 200
    assert response.content == b"real response"


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_passthrough_with_wrong_value_header(rf):
    # Wrong value, correct length - passes through, no 500.
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    request = rf.get("/en-US/", HTTP_X_MOZILLA_OPS_CANARY="b" * 64)
    response = middleware(request)
    assert response.status_code == 200
    assert response.content == b"real response"


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_passthrough_with_wrong_length_header(rf):
    # Wrong length - shortcircuits before compare_digest is called and
    # passes through.
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    request = rf.get("/en-US/", HTTP_X_MOZILLA_OPS_CANARY="short")
    response = middleware(request)
    assert response.status_code == 200
    assert response.content == b"real response"


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_passthrough_with_non_ascii_header(rf):
    # Regression: hmac.compare_digest raises TypeError on non-ASCII str
    # operands. A 64-char header of non-ASCII would therefore have produced
    # an uncontrolled 500 without knowing the token. We compare bytes, so
    # this must pass through cleanly (and count as a probe).
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    # Django decodes WSGI header values as latin-1, so build the request
    # the same way a real non-ASCII header would arrive.
    non_ascii = "\xe9" * 64
    with MetricsMock() as mm:
        request = rf.get("/en-US/", HTTP_X_MOZILLA_OPS_CANARY=non_ascii)
        response = middleware(request)
    assert response.status_code == 200
    assert response.content == b"real response"
    mm.assert_incr_once("synthetic5xx.header_present_no_match")
    mm.assert_not_incr("synthetic5xx.triggered")


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_empty_header_counts_as_probe(rf):
    # A header that is present but empty is a (failed) probe, not an absent
    # header: it must pass through AND increment the probe metric.
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    with MetricsMock() as mm:
        request = rf.get("/en-US/", HTTP_X_MOZILLA_OPS_CANARY="")
        response = middleware(request)
    assert response.status_code == 200
    assert response.content == b"real response"
    mm.assert_incr_once("synthetic5xx.header_present_no_match")
    mm.assert_not_incr("synthetic5xx.triggered")


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
@pytest.mark.parametrize("path", ["/healthz/", "/readiness/", "/healthz-cron/"])
def test_synthetic_500_middleware_skips_healthcheck_paths(rf, path):
    # Even with the matching token, healthcheck paths pass through untouched
    # so Fastly's probe stays green during a cascade test.
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    request = rf.get(path, HTTP_X_MOZILLA_OPS_CANARY=_VALID_TOKEN)
    response = middleware(request)
    assert response.status_code == 200
    assert response.content == b"real response"


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_uses_constant_time_compare(rf):
    # Verify that hmac.compare_digest is actually used for token comparison,
    # not a plain == comparison. Timing-safe compare avoids leaking token
    # characters via response timing.
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    # Use a 64-char header so we pass the length gate and reach compare_digest.
    provided = "c" * 64
    with mock.patch("bedrock.base.middleware.hmac.compare_digest", return_value=True) as m:
        request = rf.get("/en-US/", HTTP_X_MOZILLA_OPS_CANARY=provided)
        response = middleware(request)
    # Operands are bytes, never str (str would TypeError on non-ASCII).
    m.assert_called_once_with(provided.encode("utf-8"), _VALID_TOKEN.encode("utf-8"))
    # Response is the synthetic 500 because we forced the compare to True.
    assert response.status_code == 500


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_emits_metric_on_match(rf):
    # Every successful token match increments synthetic5xx.triggered so we can
    # alert on unusual volume (legit tests are a handful of hits; a leaked-token
    # abuser would look very different). Tagged with path but never the token.
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    with MetricsMock() as mm:
        request = rf.get("/en-US/", HTTP_X_MOZILLA_OPS_CANARY=_VALID_TOKEN)
        response = middleware(request)
    assert response.status_code == 500
    mm.assert_incr_once("synthetic5xx.triggered", tags=["path:/en-US/"])


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_emits_probe_metric_on_wrong_value(rf):
    # Header present but wrong value = suspicious. Increments
    # synthetic5xx.header_present_no_match so we get visibility on probing
    # BEFORE anyone succeeds guessing the token.
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    with MetricsMock() as mm:
        request = rf.get("/en-US/", HTTP_X_MOZILLA_OPS_CANARY="b" * 64)
        response = middleware(request)
    assert response.status_code == 200
    mm.assert_incr_once("synthetic5xx.header_present_no_match")
    mm.assert_not_incr("synthetic5xx.triggered")


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_emits_probe_metric_on_wrong_length(rf):
    # Same probe metric fires when length is wrong (e.g. attacker sending a
    # prefix or guessing at a different length).
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    with MetricsMock() as mm:
        request = rf.get("/en-US/", HTTP_X_MOZILLA_OPS_CANARY="short")
        response = middleware(request)
    assert response.status_code == 200
    mm.assert_incr_once("synthetic5xx.header_present_no_match")
    mm.assert_not_incr("synthetic5xx.triggered")


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_no_metric_on_missing_header(rf):
    # No header at all = normal traffic, no metrics.
    middleware = SyntheticServerErrorMiddleware(get_response=_passthrough_response)
    with MetricsMock() as mm:
        request = rf.get("/en-US/")
        middleware(request)
    mm.assert_not_incr("synthetic5xx.triggered")
    mm.assert_not_incr("synthetic5xx.header_present_no_match")


def test_synthetic_500_middleware_position_in_settings():
    # Pin the configured placement in settings.MIDDLEWARE. The behavioural
    # test below proves the ordering *works*, but builds its own chain; this
    # one fails if someone reorders the real list.
    #
    # Must be AFTER BasicAuthMiddleware so a demo-mode site still demands
    # credentials before the canary can fire, and BEFORE every redirect /
    # locale middleware so the synthetic 500 pre-empts the 302s they issue
    # (otherwise `/` and other pre-locale paths could never be cascade-tested).
    mw = settings.MIDDLEWARE
    ours = mw.index("bedrock.base.middleware.SyntheticServerErrorMiddleware")

    assert mw.index("bedrock.base.middleware.BasicAuthMiddleware") < ours

    for must_come_after in (
        "bedrock.redirects.middleware.RedirectsMiddleware",
        "bedrock.base.middleware.BedrockLangCodeFixupMiddleware",
        "bedrock.base.middleware.BedrockLocaleMiddleware",
        "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    ):
        assert ours < mw.index(must_come_after), must_come_after


@override_settings(SYNTHETIC_5XX_TOKEN=_VALID_TOKEN)
def test_synthetic_500_middleware_fires_before_locale_redirect(rf):
    # Positioning proof: our middleware sits BEFORE
    # BedrockLangCodeFixupMiddleware in the MIDDLEWARE list (pinned by
    # test_synthetic_500_middleware_position_in_settings above), so a matching
    # request to `/` returns the synthetic 500 rather than the 302 to /en-US/
    # (or wherever) that LangCodeFixup would normally issue.
    #
    # This matters because the whole point of the middleware is to force
    # user-facing 5xx on Bedrock's actual pages. If LangCodeFixup ran
    # first, `/` (and any other pre-locale path) would 302 before the
    # synthetic 500 got a chance to fire, and we couldn't test the cascade
    # on those paths.
    # Build the chain in the same order as settings.MIDDLEWARE:
    # SyntheticServerErrorMiddleware wraps BedrockLangCodeFixupMiddleware
    # wraps a passthrough.
    inner = BedrockLangCodeFixupMiddleware(get_response=_passthrough_response)
    outer = SyntheticServerErrorMiddleware(get_response=inner)

    # `/` with an Accept-Language header WOULD normally trigger LangCodeFixup
    # to 302 to /en-GB/ (or /en-US/ etc). With our middleware in front and the
    # canary token present, we should see 500 instead.
    request = rf.get(
        "/",
        HTTP_ACCEPT_LANGUAGE="en-GB,en;q=0.9",
        HTTP_X_MOZILLA_OPS_CANARY=_VALID_TOKEN,
    )
    response = outer(request)

    # 500, not 302: our middleware short-circuited before LangCodeFixup could redirect
    assert response.status_code == 500
    assert b"synthetic 500" in response.content


def test_lang_code_fixup_would_redirect_root_without_our_middleware(rf):
    # Baseline / control: without our middleware in front, LangCodeFixup
    # DOES 302-redirect `/` on requests carrying an Accept-Language header.
    # Together with the test above, this proves that the 500 we get is
    # coming from our middleware pre-empting the redirect - not from `/`
    # simply not redirecting in this test setup.
    inner = BedrockLangCodeFixupMiddleware(get_response=_passthrough_response)

    request = rf.get(
        "/",
        HTTP_ACCEPT_LANGUAGE="en-GB,en;q=0.9",
    )
    response = inner.process_request(request)

    # 302 to a locale-prefixed URL
    assert response is not None
    assert response.status_code == 302
    assert response["Location"].startswith("/en-GB")


@pytest.mark.parametrize(
    "header",
    [
        # not valid base64 (length 1 mod 4)
        "Basic a",
        # valid base64, but the decoded bytes are not text
        "Basic //8=",
        # non-ASCII, which `b64decode` rejects with a plain `ValueError`
        "Basic éééé",
        # a scheme we don't implement
        "Bearer sometoken",
        # right scheme, wrong shape
        "Basic",
    ],
)
def test_basic_auth_malformed_authorization_header_returns_401(rf, header):
    # Whatever a client sends in the header, a password-protected demo site
    # must answer with a 401 challenge, not blow up with a 500 because the
    # header could not be decoded.
    with override_settings(BASIC_AUTH_CREDS="thedude:thewalrus"):
        middleware = BasicAuthMiddleware(get_response=_passthrough_response)
        response = middleware(rf.get("/en-US/", HTTP_AUTHORIZATION=header))

    assert response.status_code == 401


def test_basic_auth_correct_credentials_pass_through(rf):
    with override_settings(BASIC_AUTH_CREDS="thedude:thewalrus"):
        middleware = BasicAuthMiddleware(get_response=_passthrough_response)
        response = middleware(rf.get("/en-US/", HTTP_AUTHORIZATION="Basic dGhlZHVkZTp0aGV3YWxydXM="))

    assert response.status_code == 200
