import datetime
from email.utils import formatdate
import time

from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware

import basket
from django_statsd.middleware import GraphiteRequestTimingMiddleware

from mozorg.forms import NewsletterForm


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


class NewsletterMiddleware(object):
    """Processes newsletter subscriptions"""
    def process_request(self, request):
        success = False
        form = NewsletterForm(request.POST or None)

        is_footer_form = (request.method == 'POST' and
                          'newsletter-footer' in request.POST)
        if is_footer_form:
            if form.is_valid():
                newsletter = request.POST['newsletter']
                data = form.cleaned_data

                try:
                    basket.subscribe(data['email'], newsletter,
                                     format=data['fmt'])
                    success = True
                except basket.BasketException:
                    msg = ("We are sorry, but there was a problem with our system. "
                           "Please try again later!")
                    form.errors['__all__'] = form.error_class([msg])

        request.newsletter_form = form
        request.newsletter_success = success
