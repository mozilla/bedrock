# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.views.decorators.csrf import csrf_exempt

import basket
from lib import l10n_utils
from commonware.decorators import xframe_allow

from bedrock.mozorg import email_contribute
from bedrock.mozorg.forms import ContributeForm, NewsletterForm
from bedrock.mozorg.util import hide_contrib_form

@xframe_allow
def hacks_newsletter(request):
    return l10n_utils.render(request,
                             'mozorg/newsletter/hacks.mozilla.org.html')


@csrf_exempt
def contribute(request, template, return_to_form):
    has_contribute_form = (request.method == 'POST' and
                           'contribute-form' in request.POST)

    has_newsletter_form = (request.method == 'POST' and
                           'newsletter-form' in request.POST)

    locale = getattr(request, 'locale', 'en-US')

    contribute_success = False
    newsletter_success = False

    # This is ugly, but we need to handle two forms. I would love if
    # these forms could post to separate pages and get redirected
    # back, but we're forced to keep the error/success workflow on the
    # same page. Please change this.
    if has_contribute_form:
        form = ContributeForm(request.POST)
        contribute_success = email_contribute.handle_form(request, form)
        if contribute_success:
            # If form was submitted successfully, return a new, empty
            # one.
            form = ContributeForm()
    else:
        form = ContributeForm()

    if has_newsletter_form:
        newsletter_form = NewsletterForm(locale,
                                         request.POST,
                                         prefix='newsletter')
        if newsletter_form.is_valid():
            data = newsletter_form.cleaned_data

            try:
                basket.subscribe(data['email'],
                                 'about-mozilla',
                                 format=data['fmt'],
                                 country=data['country'])
                newsletter_success = True
            except basket.BasketException:
                msg = newsletter_form.error_class(
                    ['We apologize, but an error occurred in our system.'
                     'Please try again later.']
                )
                newsletter_form.errors['__all__'] = msg
    else:
        newsletter_form = NewsletterForm(locale, prefix='newsletter')

    hide_form = hide_contrib_form(request.locale)

    return l10n_utils.render(request,
                             template,
                             {'form': form,
                              'contribute_success': contribute_success,
                              'newsletter_form': newsletter_form,
                              'newsletter_success': newsletter_success,
                              'return_to_form': return_to_form,
                              'hide_form': hide_form})


@xframe_allow
@csrf_exempt
def contribute_embed(request, template, return_to_form):
    """The same as contribute but allows frame embedding."""
    return contribute(request, template, return_to_form)
