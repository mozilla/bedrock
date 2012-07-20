import datetime
from email.utils import formatdate
import time

from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware

from django_statsd.middleware import GraphiteRequestTimingMiddleware

class CacheMiddleware(object):

    def process_response(self, request, response):
        cache = (request.method != 'POST' and
                 response.status_code != 404 and
                 'Cache-Control' not in response)
        if cache:
            d = datetime.datetime.now() + datetime.timedelta(minutes=10)
            stamp = time.mktime(d.timetuple())

            response['Cache-Control'] = 'max-age=600'
            response['Expires'] = formatdate(timeval=stamp, localtime=False, usegmt=True)
        return response


class NoVarySessionMiddleware(SessionMiddleware):
    """
    SessionMiddleware sets Vary: Cookie anytime request.session is accessed.
    request.session is accessed indirectly anytime request.user is touched.
    We always touch request.user to see if the user is authenticated, so every
    request would be sending vary, so we'd get no caching.
    """

    def process_response(self, request, response):
        if getattr(settings, 'READ_ONLY', False):
            return response
        # Let SessionMiddleware do its processing but prevent it from changing
        # the Vary header.
        vary = response.get('Vary', None)
        new_response = (super(NoVarySessionMiddleware, self)
                        .process_response(request, response))
        if vary:
            new_response['Vary'] = vary
        else:
            del new_response['Vary']
        return new_response

class MozorgRequestTimingMiddleware(GraphiteRequestTimingMiddleware):

    def process_view(self, request, view, view_args, view_kwargs):
        if hasattr(view, 'page_name'):
            request._view_module = 'page'
            request._view_name = view.page_name.replace('/', '.')
            request._start_time = time.time()
        else:
            f = super(MozorgRequestTimingMiddleware, self)
            f.process_view(request, view, view_args, view_kwargs)
