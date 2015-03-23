# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
from email.utils import formatdate
import re
import time

from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware

from django_statsd.middleware import GraphiteRequestTimingMiddleware


class ConditionalAuthMiddleware(object):
    def process_request(self, request):
        if any(request.path.startswith(prefix)
               for prefix in settings.AUTHENTICATED_URL_PREFIXES):
            AuthenticationMiddleware().process_request(request)


class CacheMiddleware(object):

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


class CrossOriginResourceSharingMiddleware(object):

    def process_response(self, request, response):
        """
        If the URL pattern for the request matches one of those
        in the CORS_URLS setting, apply the matching
        Access-Control-Allow-Origin header to the response.
        """
        for pattern, origin in settings.CORS_URLS.items():
            if re.search(pattern, request.path):
                response['Access-Control-Allow-Origin'] = origin
        return response


class ClacksOverheadMiddleware(object):
    # bug 1144901
    @staticmethod
    def process_response(request, response):
        if response.status_code == 200:
            response['X-Clacks-Overhead'] = 'GNU Terry Pratchett'
        return response
