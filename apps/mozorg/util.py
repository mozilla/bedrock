# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.conf.urls.defaults import url
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from funfactory.urlresolvers import reverse
import commonware.log
import l10n_utils


log = commonware.log.getLogger('mozorg.util')

def page(name, tmpl, decorators=None, **kwargs):
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


    # Apply decorators
    if decorators:
        if callable(decorators):
            _view = decorators(_view)
        else:
            try:
                # Decorators should be applied in reverse order so that input
                # can be sent in the order your would write nested decorators
                # e.g. dec1(dec2(_view)) -> [dec1, dec2]
                for decorator in reversed(decorators):
                    _view = decorator(_view)
            except TypeError:
                log.exception('decorators not iterable or does not contain callable items')

    return url(pattern, _view, name=name)
