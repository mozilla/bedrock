import l10n_utils
from django.conf import settings
from django.core.validators import email_re

import basket

def marketplace(request):
    submitted = False
    error = False
    email = ''

    if request.method == 'POST':
        email = request.POST['email']
        format_ = 'T' if request.POST.get('format') == 'text' else 'H'
        newsletter = 'app-dev'

        if not email_re.match(email):
            error = 'email'

        if not request.POST.get('privacy', None):
            error = 'privacy'

        if not error:
            basket.subscribe(email, newsletter, format=format_)
            submitted = True
            
    return l10n_utils.render(request,
                             "marketplace/marketplace.html",
                             {'submitted': submitted,
                              'error': error,
                              'email': email})
