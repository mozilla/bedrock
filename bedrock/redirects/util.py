# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from urllib import urlencode

from django.core.urlresolvers import NoReverseMatch, RegexURLResolver
from django.conf.urls import url
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

from bedrock.base.urlresolvers import reverse


LOCALE_RE = r'^(?:\w{2,3}(?:-\w{2})?/)?'
redirectpatterns = []


def register(patterns):
    redirectpatterns.extend(patterns)


def get_resolver():
    return RegexURLResolver(r'^/', redirectpatterns)


def redirect(pattern, to, permanent=True, locale_prefix=True,
             anchor=None, name=None, query=None):
    """
    Return a tuple suited for urlpatterns.

    This will redirect the pattern to the viewname by applying our
    locale-aware reverse to the given string.

    If a url is given instead of a viewname, the redirect will go directly to
    the specified url.

    If `locale_prefix` is `True` it will automatically match the pattern you specify
    as well as that patter prefixed with any locale (default: `True`). This implies that
    the pattern is anchored at the start of the URL (otherwise it doesn't have to be).

    If a name is given, reverse lookups by that name will work.

    If query is None (the default), any params from the original request will
    be appended to the redirect location, after a '?'. Otherwise, query is
    expected to be a dict or a sequence of two-element tuples for passing
    to urllib.urlencode.

    Usage:
    urlpatterns = patterns('',
        redirect(r'projects/$', 'mozorg.product'),
        redirect(r'^projects/seamonkey$', 'mozorg.product', locale_prefix=False),
        redirect(r'apps/$', 'https://marketplace.firefox.com'),
        redirect(r'firefox/$', 'firefox.new', name='firefox'),
        redirect(r'the/dude$', 'abides', query={'aggression': 'not_stand'}),
    )
    """
    if permanent:
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect

    if locale_prefix:
        pattern = pattern.lstrip('^/')
        pattern = LOCALE_RE + pattern

    def _view(request, *args, **kwargs):
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

        # use info from url captures.
        if args or kwargs:
            redirect_url = redirect_url.format(*args, **kwargs)

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

    return url(pattern, _view, name=name)
