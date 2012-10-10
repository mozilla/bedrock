from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

from funfactory.urlresolvers import reverse


def redirect(pattern, viewname, permanent=True, anchor=None):
    """
    Return a tuple suited for urlpatterns.

    This will redirect the pattern to the viewname by applying funfactory's
    locale-aware reverse to the given string.

    Usage:
    urlpatterns = patterns('',
    redirect(r'^projects/$', 'mozorg.product'),
    )
    """
    if permanent:
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect

    def _view(request):
        url = reverse(viewname)
        if anchor:
            url = '#'.join([url, anchor])
        return redirect_class(url)

    return (pattern, _view)


def redirect_external(pattern, url, permanent=True):
    """
    Return a tuple suited for urlpatterns.

    This will redirect the pattern to an external URL

    Usage:
    urlpatterns = patterns('',
    redirect(r'^projects/$', 'http://webmaker.org/projects/'),
    )
    """
    if permanent:
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect

    def _view(request):
        return redirect_class(url)

    return (pattern, _view)
