from django.conf.urls.defaults import url
from session_csrf import anonymous_csrf

import basket
import l10n_utils
from mozorg.forms import NewsletterForm

@anonymous_csrf
def _page_view(request, tmpl, **kwargs):
    ctx = kwargs

    # Turn off the newsletter by passing newsletter=False
    #
    # Need to pull this out so custom pages can still call this code,
    # but this is run on every page that uses the default view.
    if kwargs.get('newsletter', True) != False:
        success = False
        form = NewsletterForm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                data = form.cleaned_data
                basket.subscribe(data['email'], 'app-dev', format=data['fmt'])
                success = True

        ctx.update({'form': form,
                    'success': success})

    return l10n_utils.render(request, tmpl, ctx)


def page_view(tmpl, **kwargs):
    def view(request):
        return _page_view(request, tmpl, **kwargs)
    return view


def page(name, tmpl, **kwargs):
    # The URL pattern is the name with a forced trailing slash if not
    # empty
    pattern = r'^%s/$' % name if name else r'^$'

    # Set the name of the view to the template path replaced with dots
    name = tmpl.rstrip(".html").replace('/', '.')

    return url(pattern, page_view(tmpl, **kwargs), name=name)
