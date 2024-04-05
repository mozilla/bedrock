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
from warnings import warn

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import Http404, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from commonware.middleware import FrameOptionsHeader as OldFrameOptionsHeader

from bedrock.base import metrics
from lib.l10n_utils import translation

from . import urlresolvers


class LocaleURLMiddleware:
    """
    This middleware adjusts the `path_info` for reverse URL resolving.

    We split `request.path_info` into `locale` and `path`. The `path` portion
    is saved back to `request.path_info` for reverse URL resolving, while the
    `locale` will either be one we support or empty string.

    """

        if not settings.USE_L10N:
            warn(
                """
                The `USE_L10N` setting is False but LocaleURLMiddleware is
                loaded. Consider removing bedrock.base.middleware.LocaleURLMiddleware
                from your MIDDLEWARE setting.
                """.strip()
            )
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)

    def process_request(self, request):
        prefixer = urlresolvers.Prefixer(request)
        urlresolvers.set_url_prefix(prefixer)

        request.path_info = f"/{prefixer.shortened_path}"
        request.locale = prefixer.locale
        translation.activate(prefixer.locale or settings.LANGUAGE_CODE)


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
