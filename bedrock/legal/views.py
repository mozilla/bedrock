# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django.template.loader import render_to_string

from lib import l10n_utils

from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

from bedrock.base.urlresolvers import reverse

from forms import FraudReportForm


FRAUD_REPORT_EMAIL_FROM = 'Mozilla.com <noreply@mozilla.com>'
FRAUD_REPORT_EMAIL_SUBJECT = 'New trademark infringement report: %s; %s'
FRAUD_REPORT_EMAIL_TO = ['trademarks@mozilla.com']


def submit_form(request, form):
    form_submitted = True

    if form.is_valid():
        form_error = False
        data = form.cleaned_data

        subject = FRAUD_REPORT_EMAIL_SUBJECT % (data['input_url'],
                                                data['input_category'])
        sender = FRAUD_REPORT_EMAIL_FROM
        to = FRAUD_REPORT_EMAIL_TO
        msg = render_to_string('legal/emails/fraud-report.txt', data, request=request)

        email = EmailMessage(subject, msg, sender, to)

        attachment = data['input_attachment']

        if attachment:
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


def impressum(request):
    # The "impressum" page is intended for Germany. Redirect to German (de) if
    # requested in any other locale. (Bug 1248393)
    if request.locale != 'de':
        return redirect(re.sub(r'^/%s/' % request.locale, '/de/',
                               reverse('legal.impressum')), permanent=True)

    return l10n_utils.render(request, 'legal/impressum.html', {'localized': True})
