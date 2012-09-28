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

