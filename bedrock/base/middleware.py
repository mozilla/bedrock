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
import inspect
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
                if len(auth) == 2:
                    if auth[0].lower() == "basic":
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
