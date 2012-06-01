# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.conf.urls.defaults import url
from django.views.decorators.csrf import csrf_exempt
from functools import wraps

import basket
import l10n_utils
from mozorg.forms import NewsletterForm

def handle_newsletter(request):
    success = False
    form = NewsletterForm(request.POST or None)

    is_footer_form = (request.method == 'POST' and
                      'newsletter-footer' in request.POST)
    if is_footer_form:
        if form.is_valid():
            newsletter = request.POST['newsletter']
            data = form.cleaned_data

            try:
                basket.subscribe(data['email'], newsletter, format=data['fmt'])
                success = True
            except basket.BasketException, e:
                msg = ("We are sorry, but there was a problem with our system. "
                       "Please try again later!")
                form.errors['__all__'] = form.error_class([msg])

    return {'email_form': form,
            'email_success': success}

def page_view(request, tmpl, **kwargs):
    ctx = kwargs
    ctx.update(handle_newsletter(request))

    return l10n_utils.render(request, tmpl, ctx)


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
        return page_view(request, tmpl, **kwargs)

    return url(pattern, _view, name=name)
