# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Taken from zamboni.amo.middleware.

This is django-localeurl, but with mozilla style capital letters in
the locale codes.
"""

import base64
import inspect
import time

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation.trans_real import parse_accept_lang_header

from commonware.middleware import FrameOptionsHeader as OldFrameOptionsHeader

from bedrock.base import metrics
from bedrock.base.i18n import normalize_language, path_needs_lang_code, split_path_and_polish_lang


class BedrockLangCodeFixupMiddleware(MiddlewareMixin):
    """Middleware focused on prepping a viable, Bedrock-compatible language code
    in the URL, ready for the rest of the i18n logic.

    It:

    1) Prefixes 'bare' paths (e.g. /about/) with the most appropriate locale we
    can give at this point (it's possible the view will be unavailable in that
    lang, but we don't know this at this point unless we go through to basically
    l10n_utils.render())

    2) Normalises language codes that are in the path - eg en-us -> en-US and also
    goes to a prefix code if we don't have support (eg de-AT -> de)

    Querystrings are preserved in GET redirects.

    """

    def _redirect(self, request, lang_code, subpath):
        dest = f"/{lang_code}/{subpath}"
        if request.GET:
            dest += f"?{request.GET.urlencode()}"
        return HttpResponseRedirect(dest)

    def _get_normalized_lang_code_from_request(self, request):
        accept_language_header = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
        parsed_lang_list = parse_accept_lang_header(accept_language_header)
        return normalize_language(parsed_lang_list[0][0])

    def process_request(self, request):
        lang_code, subpath, lang_code_changed = split_path_and_polish_lang(request.path)

        # Add a lang code prefix if none exists, but only if we need one
        if not lang_code and path_needs_lang_code(subpath):
            # Set up a solid fallback
            new_lang_code = settings.LANGUAGE_CODE

            # Ideally, though, we'll get it from the header (and note that
            # we have no cookies, so don't need to check there.)
            if accepted_lang := self._get_normalized_lang_code_from_request(request):
                # Go with the browser's first/default lang - we don't check
                # here whether the page has content in that locale - that's
                # handled in the l10n_utils.render function
                new_lang_code = accepted_lang

            return self._redirect(request, new_lang_code, subpath)

        # 2) If the lang code needed to be fixed up redirect to the normalized one
        if lang_code and lang_code_changed:
            return self._redirect(request, lang_code, subpath)


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
        else:
            self._record(500)


class MetricsViewTimingMiddleware(MiddlewareMixin):
    """Send request timing to statsd"""

    def __init__(self, get_response):
        if not settings.ENABLE_METRICS_VIEW_TIMING_MIDDLEWARE:
            raise MiddlewareNotUsed

        self.get_response = get_response

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
        else:
            self._record_timing(request, 500)
