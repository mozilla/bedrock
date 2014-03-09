# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jingo

from django.core.mail import EmailMessage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView

from funfactory.urlresolvers import reverse

from .forms import SpeakerRequestForm
from lib import l10n_utils

SPEAKER_REQUEST_EMAIL_FROM = 'Mozilla.com <noreply@mozilla.com>'
SPEAKER_REQUEST_EMAIL_SUBJECT = 'New speaker request form submission'
SPEAKER_REQUEST_EMAIL_TO = ['events@mozilla.com']


class SpeakerRequestView(FormView):
    form_class = SpeakerRequestForm
    template_name = 'press/speaker-request.html'

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(SpeakerRequestView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SpeakerRequestView, self).get_form_kwargs()
        kwargs['auto_id'] = '%s'
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SpeakerRequestView, self).get_context_data(**kwargs)
        context['form_success'] = 'success' in self.request.GET
        return context

    def get_success_url(self):
        return reverse('press.speaker-request') + '?success=True'

    def form_valid(self, form):
        self.send_email(form)
        return super(SpeakerRequestView, self).form_valid(form)

    def send_email(self, form):
        subject = SPEAKER_REQUEST_EMAIL_SUBJECT
        sender = SPEAKER_REQUEST_EMAIL_FROM
        to = SPEAKER_REQUEST_EMAIL_TO
        msg = jingo.render_to_string(self.request, 'press/emails/speaker-request.txt', form.cleaned_data)

        email = EmailMessage(subject, msg, sender, to)

        attachment = form.cleaned_data['sr_attachment']

        if (attachment):
            email.attach(attachment.name, attachment.read(), attachment.content_type)

        email.send()

    def render_to_response(self, context, **response_kwargs):
        return l10n_utils.render(self.request,
                                 self.get_template_names(),
                                 context,
                                 **response_kwargs)
