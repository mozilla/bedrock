# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django.conf import settings
from django.core.context_processors import csrf
from django.http import (HttpResponse, HttpResponseRedirect)
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

import basket
from lib import l10n_utils
import requests
from commonware.decorators import xframe_allow
from funfactory.urlresolvers import reverse
from lib.l10n_utils.dotlang import _

from bedrock.firefox import version_re
from bedrock.firefox.utils import is_current_or_newer
from bedrock.mozorg import email_contribute
from bedrock.mozorg.forms import (ContributeForm, ContributeUniversityAmbassadorForm,
                                  NewsletterForm, WebToLeadForm)
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
                    [_('We apologize, but an error occurred in our system. '
                       'Please try again later.')]
                )
                newsletter_form.errors['__all__'] = msg
    else:
        newsletter_form = NewsletterForm(locale, prefix='newsletter')

    return l10n_utils.render(request,
                             template,
                             {'form': form,
                              'contribute_success': contribute_success,
                              'newsletter_form': newsletter_form,
                              'newsletter_success': newsletter_success,
                              'return_to_form': return_to_form,
                              'hide_form': hide_contrib_form(request.locale),
                              'has_moz15': locale in settings.LOCALES_WITH_MOZ15})


@xframe_allow
@csrf_exempt
def contribute_embed(request, template, return_to_form):
    """The same as contribute but allows frame embedding."""
    return contribute(request, template, return_to_form)


@csrf_protect
def partnerships(request):
    form = WebToLeadForm()

    template_vars = {}
    template_vars.update(csrf(request))
    template_vars['form'] = form

    return l10n_utils.render(request, 'mozorg/partnerships.html', template_vars)


@csrf_protect
@require_POST
def contact_bizdev(request):
    form = WebToLeadForm(request.POST)

    msg = 'Form invalid'
    stat = 400
    success = 0

    if form.is_valid():
        data = form.cleaned_data.copy()

        honeypot = data.pop('superpriority')

        if honeypot:
            msg = 'Visitor invalid'
            stat = 400
        else:
            interest = data.pop('interest')
            data['00NU0000002pDJr'] = interest
            data['oid'] = '00DU0000000IrgO'
            data['retURL'] = ('http://www.mozilla.org/en-US/about/'
                              'partnerships?success=1')
            r = requests.post('https://www.salesforce.com/servlet/'
                              'servlet.WebToLead?encoding=UTF-8', data)
            msg = requests.status_codes._codes.get(r.status_code, ['error'])[0]
            stat = r.status_code

            success = 1

    if request.is_ajax():
        return HttpResponse(msg, status=stat)
    else:
        return HttpResponseRedirect("%s?success=%s" % (reverse('mozorg.partnerships'), success))


def plugincheck(request, template='mozorg/plugincheck.html'):
    """
    Determine whether the current UA is the latest Firefox,
    passes the result to the template and renders the
    specified template.
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    user_version = "0"
    ua_regexp = r"Firefox/(%s)" % version_re
    match = re.search(ua_regexp, user_agent)
    if match:
        user_version = match.group(1)

    data = {
        'is_latest': is_current_or_newer(user_version)
    }

    return l10n_utils.render(request, template, data)


@csrf_exempt
def contribute_university_ambassadors(request):
    form = ContributeUniversityAmbassadorForm(request.POST or None)
    if form.is_valid():
        try:
            form.save()
        except basket.BasketException:
            msg = form.error_class(
                [_('We apologize, but an error occurred in our system. '
                   'Please try again later.')])
            form.errors['__all__'] = msg
        else:
            return redirect('mozorg.contribute_university_ambassadors_thanks')
    return l10n_utils.render(
        request,
        'mozorg/contribute_university_ambassadors.html', {'form': form}
    )
