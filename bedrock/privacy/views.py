# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lib import l10n_utils
import jingo

from commonware.response.decorators import xframe_allow

from django import template
from django.core.mail import EmailMessage
from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

from funfactory.urlresolvers import reverse

from forms import PrivacyContactForm


@xframe_allow
def facebook(request):
    return l10n_utils.render(request, 'privacy/facebook.html')


def submit_form(request, form):
    form_submitted = False

    if form.is_valid():
        form_submitted = True
        form_error = False

        honeypot = form.cleaned_data.pop('superpriority')

        if honeypot:
            form_error = True
        else:
            subject = 'Message sent from Privacy Hub'
            sender = form.cleaned_data['sender']
            to = ['privacy@mozilla.com']
            msg = jingo.render_to_string(request, 'privacy/emails/info.txt', form.cleaned_data)
            headers = {'Reply-To': sender}

            email = EmailMessage(subject, msg, sender, to, headers=headers)
            email.send()
    else:
        form_error = True

    return {'form_submitted': form_submitted, 'form_error': form_error}


@csrf_protect
def privacy(request):
    form = PrivacyContactForm()

    form_submitted = False
    form_error = False

    if request.method == 'POST':
        form = PrivacyContactForm(request.POST)
        form_results = submit_form(request, form)

        form_submitted = form_results['form_submitted']
        form_error = form_results['form_error']

    template_vars = {
        'form': form,
        'form_submitted': form_submitted,
        'form_error': form_error,
    }

    return l10n_utils.render(request, 'privacy/index.html', template_vars)


@csrf_protect
def archive(request, archive_name):
    tpl = 'privacy/archive/' + archive_name.rstrip('/') + '.html'

    # make sure requested template exists
    try:
        template.loader.get_template(tpl)
    except template.TemplateDoesNotExist:
        raise Http404

    form = PrivacyContactForm()

    form_submitted = False
    form_error = False

    if request.method == 'POST':
        form = PrivacyContactForm(request.POST)
        form_results = submit_form(request, form)

        form_submitted = form_results['form_submitted']
        form_error = form_results['form_error']

    template_vars = {
        'form': form,
        'form_submitted': form_submitted,
        'form_error': form_error,
    }

    return l10n_utils.render(request, tpl, template_vars)


@xframe_allow
@csrf_protect
def firefoxos(request):
    form = PrivacyContactForm()
    form_submitted = False
    form_error = False

    if request.method == 'POST':
        form = PrivacyContactForm(request.POST)
        form_results = submit_form(request, form)

        form_submitted = form_results['form_submitted']
        form_error = form_results['form_error']

    template_vars = {
        'form': form,
        'form_submitted': form_submitted,
        'form_error': form_error,
    }

    if request.POST and not form_error:
        # Seeing the form was submitted without error, redirect, do not simply
        # send a response to avoid problem described below.
        # @see https://bugzilla.mozilla.org/show_bug.cgi?id=873476 (3.2)
        response = redirect(reverse('privacy.firefoxos'), template_vars)
        response['Location'] += '?submitted=%s' % form_submitted

        return response
    else:
        # If the below is called after a redirect the template_vars will be lost, therefore
        # we need to update the form_submitted state from the submitted url parameter.
        submitted = request.GET.get('submitted') == 'True'
        template_vars['form_submitted'] = submitted
        return l10n_utils.render(request, 'privacy/ffos_privacy.html', template_vars)
