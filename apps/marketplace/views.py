import l10n_utils
from django.conf import settings
from django.core.validators import email_re

import basket

def marketplace(request):
    submitted = False
    form_error = False
    email = ''

    if request.method == 'POST':
        email = request.POST['email']
        newsletter = 'app-dev'

        if email_re.match(email):
            basket.subscribe(email, newsletter)
            submitted = True
        else:
            form_error = True
            

    return l10n_utils.render(request,
                             "marketplace/marketplace.html",
                             {'submitted': submitted,
                              'form_error': form_error,
                              'email': email})
