# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import l10n_utils
import jingo

from commonware.response.decorators import xframe_allow

from django.core.mail import EmailMessage

from forms import PrivacyContactForm


@xframe_allow
def facebook(request):
    return l10n_utils.render(request, 'privacy/facebook.html')


def privacy(request):
    form = PrivacyContactForm()
    form_submitted = False
    if request.method == 'POST':
        form = PrivacyContactForm(request.POST)

        if form.is_valid():
            subject = 'Message sent from Privacy Hub'
            sender = form.cleaned_data['sender']
            to = ['privacy@mozilla.com']
            msg = jingo.render_to_string(request, 'privacy/emails/info.txt', form.cleaned_data)
            headers = {'Reply-To': sender}

            email = EmailMessage(subject, msg, sender, to, headers=headers)
            email.send()
            form_submitted = True

    return l10n_utils.render(request, 'privacy/index.html', {
            'form': form,
            'form_submitted': form_submitted
        })
