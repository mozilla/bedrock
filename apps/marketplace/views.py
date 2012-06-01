# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import l10n_utils
from django.conf import settings
from django.core.validators import email_re
from django.views.decorators.csrf import csrf_exempt
from bedrock_util import secure_required

import basket

from mozorg.forms import NewsletterForm
from bedrock_util import secure_required

@csrf_exempt
@secure_required
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
@csrf_exempt
@secure_required
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
