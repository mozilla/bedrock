# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lib import l10n_utils
import jingo

from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

from funfactory.urlresolvers import reverse

from forms import FraudReportForm


FRAUD_REPORT_EMAIL_FROM = 'Mozilla.com <noreply@mozilla.com>'
FRAUD_REPORT_EMAIL_SUBJECT = 'New violating website report'
FRAUD_REPORT_EMAIL_TO = ['trademarks@mozilla.com', 'mozilla@mofo.com']


def submit_form(request, form):
    form_submitted = True

    if form.is_valid():
        form_error = False

        subject = FRAUD_REPORT_EMAIL_SUBJECT
        sender = FRAUD_REPORT_EMAIL_FROM
        to = FRAUD_REPORT_EMAIL_TO
        msg = jingo.render_to_string(request, 'legal/emails/fraud-report.txt', form.cleaned_data)

        email = EmailMessage(subject, msg, sender, to)

        attachment = form.cleaned_data['attachment']

        if (attachment):
            email.attach(attachment.name, attachment.read(), attachment.content_type)

        email.send()
    else:
        form_error = True

    return {'form_submitted': form_submitted, 'form_error': form_error}


@csrf_protect
def fraud_report(request):
    form = FraudReportForm(auto_id='%s')

    form_submitted = False
    form_error = False

    if request.method == 'POST':
        form = FraudReportForm(request.POST, request.FILES)
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
        response = redirect(reverse('legal.fraud-report'), template_vars)
        response['Location'] += '?submitted=%s' % form_submitted

        return response
    else:
        # If the below is called after a redirect the template_vars will be lost, therefore
        # we need to update the form_submitted state from the submitted url parameter.
        submitted = request.GET.get('submitted') == 'True'
        template_vars['form_submitted'] = submitted
        return l10n_utils.render(request, 'legal/fraud-report.html', template_vars)
