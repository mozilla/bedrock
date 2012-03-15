import l10n_utils
from django.conf import settings
from django.core.validators import email_re
from session_csrf import anonymous_csrf

import basket

from mozorg.forms import NewsletterForm

@anonymous_csrf
def marketplace(request):
    success = False
    form = NewsletterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            basket.subscribe(data['email'], 'app-dev', format=data['fmt'])
            success = True
            
    return l10n_utils.render(request,
                             "marketplace/marketplace.html",
                             {'form': form,
                              'success': success})
