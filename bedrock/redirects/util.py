# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from urllib import urlencode

from django.core.urlresolvers import NoReverseMatch
from django.conf.urls.defaults import url
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

from funfactory.urlresolvers import reverse


def redirect(pattern, to, permanent=True, anchor=None, name='', query=None):
    """
    Return a tuple suited for urlpatterns.

    This will redirect the pattern to the viewname by applying funfactory's
    locale-aware reverse to the given string.

    If a url is given instead of a viewname, the redirect will go directly to
    the specified url.

    If a name is given, reverse lookups by that name will work.

    If query is None (the default), any params from the original request will
    be appended to the redirect location, after a '?'. Otherwise, query is
    expected to be a dict or a sequence of two-element tuples for passing
    to urllib.urlencode.

    Usage:
    urlpatterns = patterns('',
        redirect(r'^projects/$', 'mozorg.product'),
        redirect(r'^apps/$', 'https://marketplace.firefox.com'),
        redirect(r'^firefox/$', 'firefox.new', name='firefox'),
        redirect(r'^the/dude$', 'abides', query={'aggression': 'not_stand'}),
    )
    """
    if permanent:
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect

    def _view(request):
        # If it's a callable, call it and get the url out.
        if callable(to):
            to_value = to(request)
        else:
            to_value = to

        try:
            redirect_url = reverse(to_value)
        except NoReverseMatch:
            # Assume it's a URL
            redirect_url = to_value

        if query:
            querystring = urlencode(query)
        elif query is None:
            querystring = request.META.get('QUERY_STRING')
        else:
            querystring = ''

        if querystring:
            redirect_url = '?'.join([redirect_url, querystring])

        if anchor:
            redirect_url = '#'.join([redirect_url, anchor])
        return redirect_class(redirect_url)

    if name:
        return url(pattern, _view, name=name)
    return (pattern, _view)
