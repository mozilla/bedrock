import os

from django.conf.urls.defaults import url
from session_csrf import anonymous_csrf
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
            data = form.cleaned_data
            basket.subscribe(data['email'], 'app-dev', format=data['fmt'])
            success = True

    return {'email_form': form,
            'email_success': success}


@anonymous_csrf
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

    return url(pattern,
               lambda request: page_view(request, tmpl, **kwargs),
               name=name)
