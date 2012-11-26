# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.urlresolvers import NoReverseMatch
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

from funfactory.urlresolvers import reverse


def redirect(pattern, to, permanent=True, anchor=None):
    """
    Return a tuple suited for urlpatterns.

    This will redirect the pattern to the viewname by applying funfactory's
    locale-aware reverse to the given string.

    If a url is given instead of a viewname, the redirect will go directly to
    the specified url.

    Usage:
    urlpatterns = patterns('',
        redirect(r'^projects/$', 'mozorg.product'),
        redirect(r'^apps/$', url='https://marketplace.mozilla.org'),
    )
    """
    if permanent:
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect

    def _view(request):
        try:
            redirect_url = reverse(to)
        except NoReverseMatch:
            # Assume it's a URL
            redirect_url = to

        if anchor:
            redirect_url = '#'.join([redirect_url, anchor])
        return redirect_class(redirect_url)

    return (pattern, _view)
