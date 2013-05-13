# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lib import l10n_utils
import jingo

from commonware.response.decorators import xframe_allow

#from django.core.context_processors import csrf
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_protect

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

    return l10n_utils.render(request, 'privacy/ffos_privacy.html', template_vars)
