# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
from email.utils import formatdate
import time

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.utils.cache import add_never_cache_headers

from django_statsd.middleware import GraphiteRequestTimingMiddleware


class CacheMiddleware:

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        return self.process_response(self.get_response(request))

    def process_response(self, request, response):
        cache = (request.method != 'POST' and
                 response.status_code != 404 and
                 'Cache-Control' not in response)
        if cache:
            d = datetime.datetime.now() + datetime.timedelta(minutes=10)
            stamp = time.mktime(d.timetuple())

            response['Cache-Control'] = 'max-age=600'
            response['Expires'] = formatdate(timeval=stamp, localtime=False,
                                             usegmt=True)
        return response


class MozorgRequestTimingMiddleware(GraphiteRequestTimingMiddleware):

    def process_view(self, request, view, view_args, view_kwargs):
        if hasattr(view, 'page_name'):
            request._view_module = 'page'
            request._view_name = view.page_name.replace('/', '.')
            request._start_time = time.time()
        else:
            f = super(MozorgRequestTimingMiddleware, self)
            f.process_view(request, view, view_args, view_kwargs)


class ClacksOverheadMiddleware:
    # bug 1144901

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        return self.process_response(self.get_response(request))

    @staticmethod
    def process_response(request, response):
        if response.status_code == 200:
            response['X-Clacks-Overhead'] = 'GNU Terry Pratchett'
        return response


class HostnameMiddleware:
    def __init__(self, get_response=None):
        if not settings.ENABLE_HOSTNAME_MIDDLEWARE:
            raise MiddlewareNotUsed

        values = [getattr(settings, x) for x in ['HOSTNAME', 'CLUSTER_NAME']]
        self.backend_server = '.'.join(x for x in values if x)

        self.get_response = get_response

    def __call__(self, request):
        return self.process_response(self.get_response(request))

    def process_response(self, request, response):
        response['X-Backend-Server'] = self.backend_server
        return response


class VaryNoCacheMiddleware:
    def __init__(self, get_response=None):
        if not settings.ENABLE_VARY_NOCACHE_MIDDLEWARE:
            raise MiddlewareNotUsed
        self.get_response = get_response

    def __call__(self, request):
        return self.process_response(self.get_response(request))

    @staticmethod
    def process_response(request, response):
        if 'vary' in response:
            path = request.path
            if path != '/' and not any(path.startswith(x) for x in
                                       settings.VARY_NOCACHE_EXEMPT_URL_PREFIXES):
                del response['vary']
                del response['expires']
                add_never_cache_headers(response)

        return response
