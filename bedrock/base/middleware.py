# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Taken from zamboni.amo.middleware.

This is django-localeurl, but with mozilla style capital letters in
the locale codes.
"""

import base64
import contextlib
import hmac
import inspect
import logging
import time
from functools import wraps

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.middleware.locale import LocaleMiddleware as DjangoLocaleMiddleware
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import trans_real

from commonware.middleware import FrameOptionsHeader as OldFrameOptionsHeader
from csp.contrib.rate_limiting import RateLimitedCSPMiddleware

from bedrock.base import metrics
from bedrock.base.exceptions import Http410
from bedrock.base.i18n import (
    check_for_bedrock_language,
    get_language_from_headers,
    normalize_language,
    path_needs_lang_code,
    split_path_and_normalize_language,
)
from lib.l10n_utils import is_root_path_with_no_language_clues

logger = logging.getLogger(__name__)


class BedrockLangCodeFixupMiddleware(MiddlewareMixin):
    """Middleware focused on prepping a viable, Bedrock-compatible language code
    in the URL, ready for the rest of the i18n logic.

    It:

    1) Redirects to a new language-coded path if we detect the lang=XX querystring.
    This is basically a no-JS way for us to handle language switching.

    2) Normalises language codes that are in the path - eg en-us -> en-US and also
    goes to a prefix code if we don't have support (eg de-AT -> de)

    3) If no redirect is needed, sets request.locale to be the normalized
    lang code we've got from the URL

    Querystrings are preserved in GET redirects.

    """

    def _redirect(self, request, lang_code, subpath):
        dest = f"/{lang_code}/{subpath}"

        # log the redirect without querystrings, in case there's a token or similar we don't want to end up in Markus
        metrics.incr("bedrock.langfixup.redirect", tags=[f"from:{request.path}", f"to:{dest}"])

        if request.GET:
            dest += f"?{request.GET.urlencode()}"

        response = HttpResponseRedirect(dest)
        response["Vary"] = "Accept-Language"
        return response

    def process_request(self, request):
        # Initially see if we can separate a lang code from the rest of the URL
        # path, along with a hint about whether the lang code changed, which
        # suggests we will need to redirect using `lang_code` as a new prefix.

        lang_code, subpath, lang_code_changed = split_path_and_normalize_language(request.path)

        # Check for any no-JS language - doing this eagerly is good, as any further
        # fixups due to the actual lang code in the lang=XX querystring will be
        # handled by the rest of this function when we come back to it.
        # Also fixes https://github.com/mozilla/bedrock/issues/5931
        lang_via_querystring = request.GET.get("lang", None)
        if lang_via_querystring is not None:
            cleaned_lang_via_querystring = normalize_language(lang_via_querystring)
            # Drop the lang querystring to avoid a redirect loop;
            # request.GET is immutable so we have to edit a copy
            if not cleaned_lang_via_querystring:
                cleaned_lang_via_querystring = settings.LANGUAGE_CODE
            qs = request.GET.copy()
            del qs["lang"]
            request.GET = qs
            return self._redirect(request, cleaned_lang_via_querystring, subpath)

        # If we're not redirecting based on a querystring, do we need to find
        # a language code? If so, find from the headers and redirect.
        if not lang_code and path_needs_lang_code(request.path) and not is_root_path_with_no_language_clues(request):
            lang_code = get_language_from_headers(request)
            return self._redirect(request, lang_code, subpath)

        # Or if we have a lang code, but it's not the one that was in the
        # original URL path – e.g. fixing es-mx to es-MX - we also need to redirect
        if lang_code and lang_code_changed:
            return self._redirect(request, lang_code, subpath)

        # If we get this far, the path contains a validly formatted lang code
        # OR the path does not need a lang code. We annotate the request appropriately
        request.locale = lang_code if lang_code else ""


class BedrockLocaleMiddleware(DjangoLocaleMiddleware):
    """Middleware that usually* wraps Django's own i18n middleware in order to
    ensure we normalize language codes - i..e. we ensure they are in
    mixed case we use, rather than Django's internal all-lowercase codes.

    *for one specific situation, though, we skip Django's LocaleMiddleware entirely:
    we have a special SEO-helping page that gets returned to robots/spiders that
    don't declare an accept-language header, showing a list of locales to pick.

    It needs to be kept super-light so that it doesn't diverge too far from
    the stock LocaleMiddleware, lest we wake up dragons when we use
    wagtail-localize, which squarely depends on django's LocaleMiddleware.

    Note: this is not SUMO's LocaleMiddleware, this just a tribute.
    (https://github.com/escattone/kitsune/blob/main/kitsune/sumo/middleware.py#L128)
    """

    def process_request(self, request):
        if is_root_path_with_no_language_clues(request):
            # Skip using Django's LocaleMiddleware
            metrics.incr(
                "bedrock.localemiddleware.skipdjangolocalemiddleware",
                tags=[f"path:{request.path}"],
            )
        else:
            with normalized_get_language():
                with simplified_check_for_language():
                    return super().process_request(request)

    def process_response(self, request, response):
        if is_root_path_with_no_language_clues(request):
            # Skip using Django's LocaleMiddleware on the response cycle too
            return response

        with normalized_get_language():
            with simplified_check_for_language():
                return super().process_response(request, response)


@contextlib.contextmanager
def normalized_get_language():
    """
    Ensures that any use of django.utils.translation.get_language()
    within its context will return a normalized language code. This
    context manager only works when the "get_language" function is
    acquired from the "django.utils.translation" module at call time,
    so for example, if it's called like "translation.get_language()".

    Note that this does not cover every call to translation.get_language()
    as there are calls to it on Django startup and more, but this gives us an
    extra layer of (idempotent) fixing up within the request/response cycle.
    """
    get_language = translation.get_language

    @wraps(get_language)
    def get_normalized_language():
        return normalize_language(get_language())

    translation.get_language = get_normalized_language

    try:
        yield
    finally:
        translation.get_language = get_language


@contextlib.contextmanager
def simplified_check_for_language():
    """Ensures that calls to trans_real.check_for_language within
    its context will not check for the existence of files in
    `appname/LANG_CODE/locale` and therefore avoid a false negative about
    the langs we support (our lang files are in ./data/l10n-team/LANG_CODE)
    but check_for_language is opinionated and expects only the Django directory
    pattern for lang files."""

    check_for_language = trans_real.check_for_language

    @wraps(check_for_language)
    def simpler_check_for_language(lang_code):
        return check_for_bedrock_language(lang_code)

    trans_real.check_for_language = simpler_check_for_language

    try:
        yield
    finally:
        trans_real.check_for_language = check_for_language


class SyntheticServerErrorMiddleware:
    """Returns a synthetic 500 when a request carries a matching magic header.

    Purpose is to test failure paths (specifically Fastly's origin failover
    cascade) by producing a controlled 5xx from Bedrock without breaking
    anything real.

    The middleware is a no-op when the SYNTHETIC_5XX_TOKEN env var is unset
    (raises MiddlewareNotUsed so Django drops it from the chain). It also
    refuses to arm if the configured token is not exactly TOKEN_LENGTH
    ASCII chars (see below for why length is pinned, and why ASCII).

    When armed, a request carrying the token in the X-Mozilla-Ops-Canary
    header receives HTTP 500 with a synthetic body; other requests pass
    through.

    Healthcheck paths (/healthz/, /readiness/, /healthz-cron/) are always
    passed through so Fastly's probe stays green during a cascade test,
    which is precisely the scenario the cascade is designed to catch
    (site broken but /healthz/ says 200).

    Token comparison uses hmac.compare_digest for constant-time content
    comparison, gated by a strict length check. Python's docs note that
    compare_digest can leak string lengths via timing when the operands
    differ in length; by requiring provided == TOKEN_LENGTH before calling
    compare_digest, we ensure both operands are always the same length when
    the comparison runs. The pinned length (64 chars = openssl rand -hex 32
    = 256 bits of entropy) is public info by design, so any timing signal
    from the length check itself leaks nothing an attacker doesn't already
    know.

    Both operands are compared as bytes, not str. compare_digest raises
    TypeError when given str operands containing non-ASCII characters, so a
    str-based compare would let anyone send a 64-char header full of
    non-ASCII and trigger an uncontrolled 500 without knowing the token.
    Comparing UTF-8 encoded bytes makes that impossible, and the configured
    token is additionally required to be pure ASCII so its byte length is
    guaranteed to equal TOKEN_LENGTH.

    A header that is present but empty is treated as a (failed) probe, not
    as absent, so it shows up in the header_present_no_match metric.

    Two metrics are emitted for observability:
    - synthetic5xx.triggered (with path tag) on every successful match.
      Legit tests = a few hits. Leaked-token abuse = many.
    - synthetic5xx.header_present_no_match on every request that carries
      the header with a wrong value or wrong length. A spike here is the
      early-warning signal for token probing before a guesser succeeds.

    The synthetic 500 response is a plain text body with no Cache-Control or
    Surrogate-Control override. Setting `Cache-Control: no-store` (which was
    tempting as belt-and-braces against caching a 500) empirically caused
    Fastly to enter pass state BEFORE our failover cascade in vcl_fetch got
    a look, suppressing the restart. Fastly's default behaviour already
    avoids caching 5xx, so the belt-and-braces was low-value and worth
    dropping for the cascade to fire correctly.

    Trigger by curling with:

        curl -H "X-Mozilla-Ops-Canary: <64-char-token>" https://<host>/some-path
    """

    HEADER_NAME = "X-Mozilla-Ops-Canary"
    HEALTHCHECK_PATHS = ("/healthz/", "/readiness/", "/healthz-cron/")
    # openssl rand -hex 32 → 64 hex chars, 256 bits of entropy.
    TOKEN_LENGTH = 64

    def __init__(self, get_response):
        token = settings.SYNTHETIC_5XX_TOKEN
        if not token:
            raise MiddlewareNotUsed
        if len(token) != self.TOKEN_LENGTH:
            # Fail loud at startup rather than silently accept a weak/misconfigured
            # token. `openssl rand -hex 32` is the intended generator.
            logger.warning(
                "SyntheticServerErrorMiddleware disabled: SYNTHETIC_5XX_TOKEN must be exactly %d chars, got %d",
                self.TOKEN_LENGTH,
                len(token),
            )
            raise MiddlewareNotUsed
        if not token.isascii():
            # Non-ASCII would make the UTF-8 byte length differ from the char
            # length, so no request could ever match. Refuse rather than arm a
            # middleware that can never fire.
            logger.warning("SyntheticServerErrorMiddleware disabled: SYNTHETIC_5XX_TOKEN must be ASCII")
            raise MiddlewareNotUsed
        self.get_response = get_response
        self._token = token.encode("utf-8")

    def __call__(self, request):
        if request.path in self.HEALTHCHECK_PATHS:
            return self.get_response(request)

        # Named `provided_token` (not `provided`) deliberately: Sentry captures
        # frame locals, and the `token` entry in SENSITIVE_FIELDS_TO_MASK_ENTIRELY
        # substring-matches this name, so the value is masked if anything below
        # raises after a successful match.
        provided_token = request.headers.get(self.HEADER_NAME)
        if provided_token is None:
            return self.get_response(request)

        # Compare as bytes: compare_digest raises TypeError on non-ASCII str,
        # which would otherwise be an unauthenticated route to a 500 (see
        # docstring). Length short-circuit ensures compare_digest is only ever
        # called with equal-length operands. Any header value present but not
        # matching (empty, wrong length OR wrong value) counts as a probe
        # attempt so we get observability on token-guessing BEFORE anyone
        # succeeds.
        provided_token = provided_token.encode("utf-8")
        if len(provided_token) != self.TOKEN_LENGTH or not hmac.compare_digest(provided_token, self._token):
            metrics.incr("synthetic5xx.header_present_no_match")
            return self.get_response(request)

        # Successful match.
        metrics.incr("synthetic5xx.triggered", tags=[f"path:{request.path}"])
        # Note: we deliberately do NOT set Cache-Control: no-store or
        # Surrogate-Control here, even as belt-and-braces against a synthetic
        # 500 getting cached. Empirically, Fastly reacts to those headers by
        # switching the response into pass state BEFORE our cascade block in
        # vcl_fetch gets a look, which suppresses the failover restart we
        # want to trigger. Fastly's default behaviour already avoids caching
        # 5xx responses, so the belt-and-braces was low-value; the cascade
        # firing correctly is not. See PR #1567 discussion (2026-07-02).
        return HttpResponse(
            "synthetic 500 for cascade test",
            content_type="text/plain",
            status=500,
        )


class BasicAuthMiddleware:
    """
    Middleware to protect the entire site with a single basic-auth username and password.
    Set the BASIC_AUTH_CREDS environment variable to enable.
    """

    def __init__(self, get_response):
        if not settings.BASIC_AUTH_CREDS:
            raise MiddlewareNotUsed

        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)

    def process_request(self, request):
        required_auth = settings.BASIC_AUTH_CREDS
        if required_auth:
            if "Authorization" in request.headers:
                auth = request.headers["Authorization"].split()
                if len(auth) == 2 and auth[0].lower() == "basic":
                    # A client can send anything here, so treat a header we can't
                    # decode as simply the wrong credentials rather than a 500.
                    with contextlib.suppress(ValueError):
                        provided_auth = base64.b64decode(auth[1]).decode()
                        if provided_auth == required_auth:
                            # we're good. continue on.
                            return None

            response = HttpResponse(status=401, content="<h1>Unauthorized. This site is in private demo mode.</h1>")
            realm = settings.APP_NAME or "bedrock-demo"
            response["WWW-Authenticate"] = f'Basic realm="{realm}"'
            return response


class FrameOptionsHeader(OldFrameOptionsHeader, MiddlewareMixin):
    pass


class MetricsStatusMiddleware(MiddlewareMixin):
    """Send status code counts to statsd"""

    def _record(self, status_code):
        metrics.incr("response.status", tags=[f"status_code:{status_code}"])

    def process_response(self, request, response):
        self._record(response.status_code)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            self._record(404)
        elif isinstance(exception, Http410):
            self._record(410)
        else:
            self._record(500)


class MetricsViewTimingMiddleware(MiddlewareMixin):
    """Send request timing to statsd"""

    def __init__(self, get_response):
        if not settings.ENABLE_METRICS_VIEW_TIMING_MIDDLEWARE:
            raise MiddlewareNotUsed

        super().__init__(get_response)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if inspect.isfunction(view_func):
            view = view_func
        else:
            view = view_func.__class__

        request._start_time = time.time()
        request._view_module = getattr(view, "__module__", "none")
        request._view_name = getattr(view, "__name__", "none")

    def _record_timing(self, request, status_code):
        if hasattr(request, "_start_time") and hasattr(request, "_view_module") and hasattr(request, "_view_name"):
            # View times.
            view_time = int((time.time() - request._start_time) * 1000)
            metrics.timing(
                "view.timings",
                view_time,
                tags=[
                    f"view_path:{request._view_module}.{request._view_name}.{request.method}",
                    f"module:{request._view_module}.{request.method}",
                    f"method:{request.method}",
                    f"status_code:{status_code}",
                ],
            )

    def process_response(self, request, response):
        self._record_timing(request, response.status_code)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            self._record_timing(request, 404)
        elif isinstance(exception, Http410):
            self._record_timing(request, 410)
        else:
            self._record_timing(request, 500)


class CSPMiddlewareByPathPrefix(RateLimitedCSPMiddleware):
    """
    A subclass of CSPMiddleware that allows for different CSP policies based path prefix.

    This is useful for allowing different CSP policies for different parts of the site, such as the
    wagtail admin interface.

    The paths and policies are defined in the settings.CSP_PATH_OVERRIDES dictionary, where the key
    is the path prefix and the value is the CSP policy as expected by django-csp.
    """

    def process_response(self, request, response):
        if CSP_PATH_OVERRIDES := getattr(settings, "CSP_PATH_OVERRIDES", None):
            for prefix, config in CSP_PATH_OVERRIDES.items():
                if request.path.startswith(prefix):
                    response._csp_config = config.get("DIRECTIVES", {})
                    break

        if CSP_PATH_OVERRIDES_RO := getattr(settings, "CSP_PATH_OVERRIDES_REPORT_ONLY", None):
            for prefix, config in CSP_PATH_OVERRIDES_RO.items():
                if request.path.startswith(prefix):
                    response._csp_config_ro = config.get("DIRECTIVES", {})
                    break

        return super().process_response(request, response)
