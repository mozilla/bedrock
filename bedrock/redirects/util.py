# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from urllib import urlencode

from django.core.urlresolvers import NoReverseMatch, RegexURLResolver, reverse
from django.conf.urls import url
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.views.decorators.vary import vary_on_headers

import commonware.log

from bedrock.mozorg.decorators import cache_control_expires


log = commonware.log.getLogger('redirects.util')
LOCALE_RE = r'^(?P<locale>\w{2,3}(?:-\w{2})?/)?'
# redirects registry
redirectpatterns = []


def register(patterns):
    redirectpatterns.extend(patterns)


def get_resolver(patterns=None):
    return RegexURLResolver(r'^/', patterns or redirectpatterns)


def header_redirector(header_name, regex, match_dest, nomatch_dest, case_sensitive=False):
    flags = 0 if case_sensitive else re.IGNORECASE
    regex_obj = re.compile(regex, flags)
    header_name = 'HTTP_' + header_name.upper().replace('-', '_')

    def decider(request, *args, **kwargs):
        value = request.META.get(header_name, '')
        match = regex_obj.search(value)
        if match:
            return match_dest
        else:
            return nomatch_dest

    return decider


def ua_redirector(regex, match_dest, nomatch_dest, case_sensitive=False):
    return header_redirector('user-agent', regex, match_dest, nomatch_dest, case_sensitive)


def redirect(pattern, to, permanent=True, locale_prefix=True, anchor=None, name=None,
             query=None, vary=None, cache_timeout=12, decorators=None):
    """
    Return a url matcher suited for urlpatterns.

    pattern: the regex against which to match the requested URL.
    to: either a url name that `reverse` will find, a url that will simply be returned,
        or a function that will be given the request and url captures, and return the
        destination.
    permanent: boolean whether to send a 301 or 302 response.
    locale_prefix: automatically prepend `pattern` with a regex for an optional locale
        in the url. This locale (or None) will show up in captured kwargs as 'locale'.
    anchor: if set it will be appended to the destination url after a '#'.
    name: if used in a `urls.py` the redirect URL will be available as the name
        for use in calls to `reverse()`. Does _NOT_ work if used in a `redirects.py` file.
    query: a dict of query params to add to the destination url.
    vary: if you used an HTTP header to decide where to send users you should include that
        header's name in the `vary` arg.
    cache_timeout: number of hours to cache this redirect. just sets the proper `cache-control`
        and `expires` headers.
    decorators: a callable (or list of callables) that will wrap the view used to redirect
        the user. equivalent to adding a decorator to any other view.

    Usage:
    urlpatterns = [
        redirect(r'projects/$', 'mozorg.product'),
        redirect(r'^projects/seamonkey$', 'mozorg.product', locale_prefix=False),
        redirect(r'apps/$', 'https://marketplace.firefox.com'),
        redirect(r'firefox/$', 'firefox.new', name='firefox'),
        redirect(r'the/dude$', 'abides', query={'aggression': 'not_stand'}),
    ]
    """
    if permanent:
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect

    if locale_prefix:
        pattern = pattern.lstrip('^/')
        pattern = LOCALE_RE + pattern

    view_decorators = []
    if cache_timeout:
        view_decorators.append(cache_control_expires(cache_timeout))

    if vary:
        if isinstance(vary, basestring):
            vary = [vary]
        view_decorators.append(vary_on_headers(*vary))

    if decorators:
        if callable(decorators):
            view_decorators.append(decorators)
        else:
            view_decorators.extend(decorators)

    def _view(request, *args, **kwargs):
        # don't want to have 'None' in substitutions
        kwargs = {k: v or '' for k, v in kwargs.items()}
        args = [x or '' for x in args]

        # If it's a callable, call it and get the url out.
        if callable(to):
            to_value = to(request, *args, **kwargs)
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

    # Apply decorators
    try:
        # Decorators should be applied in reverse order so that input
        # can be sent in the order your would write nested decorators
        # e.g. dec1(dec2(_view)) -> [dec1, dec2]
        for decorator in reversed(view_decorators):
            _view = decorator(_view)
    except TypeError:
        log.exception('decorators not iterable or does not contain '
                      'callable items')

    return url(pattern, _view, name=name)
