# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
from email.utils import formatdate
import time

import basket
from django_statsd.middleware import GraphiteRequestTimingMiddleware

from l10n_utils.dotlang import _lazy
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
        form = NewsletterForm(request.locale, request.POST or None)

        is_footer_form = (request.method == 'POST' and
                          'newsletter-footer' in request.POST)
        if is_footer_form:
            if form.is_valid():
                data = form.cleaned_data
                kwargs = {
                    'format': data['fmt'],
                }
                # add optional data
                kwargs.update(dict((k, data[k]) for k in ['country',
                                                          'lang',
                                                          'source_url']
                                   if data[k]))
                try:
                    basket.subscribe(data['email'], data['newsletter'],
                                     **kwargs)
                    success = True
                except basket.BasketException:
                    msg = _lazy("We are sorry, but there was a problem "
                                "with our system. Please try again later!")
                    form.errors['__all__'] = form.error_class([msg])

        request.newsletter_form = form
        request.newsletter_success = success
