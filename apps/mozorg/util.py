import os

from django.conf.urls.defaults import url
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from funfactory.urlresolvers import reverse
import l10n_utils


def page(name, tmpl, **kwargs):
    # The URL pattern is the name with a forced trailing slash if not
    # empty
    pattern = r'^%s/$' % name if name else r'^$'

    # Set the name of the view to the template path replaced with dots
    (base, ext) = os.path.splitext(tmpl)
    name = base.replace('/', '.')

    # we don't have a caching backend yet, so no csrf (it's just a
    # newsletter form anyway)
    @csrf_exempt
    def _view(request):
        return l10n_utils.render(request, tmpl, kwargs)

    # This is for graphite so that we can differentiate pages
    _view.page_name = name

    return url(pattern, _view, name=name)


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
