import os

from django.conf.urls.defaults import url
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


import basket
from funfactory.urlresolvers import reverse
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
            except basket.BasketException:
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
