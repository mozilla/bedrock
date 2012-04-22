import l10n_utils
from django.conf import settings
from django.core.validators import email_re
from django.views.decorators.csrf import csrf_exempt

import basket

from mozorg.forms import NewsletterForm

@csrf_exempt
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

def partners(request):
    success = False
    form = NewsletterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            basket.subscribe(data['email'], 'app-dev', format=data['fmt'])
            success = True
            
    return l10n_utils.render(request,
                             "marketplace/partners.html",
                             {'form': form,
                              'success': success})
