# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView

from bedrock.base.urlresolvers import reverse

from .forms import (PressInquiryForm, SpeakerRequestForm)
from lib import l10n_utils

PRESS_INQUIRY_EMAIL_SUBJECT = 'New Press Inquiry'
PRESS_INQUIRY_EMAIL_TO = ['press@mozilla.com']
SPEAKER_REQUEST_EMAIL_FROM = PRESS_INQUIRY_EMAIL_FROM = 'Mozilla.com <noreply@mozilla.com>'
SPEAKER_REQUEST_EMAIL_SUBJECT = 'New speaker request form submission'
SPEAKER_REQUEST_EMAIL_TO = ['events@mozilla.com']


class PressInquiryView(FormView):
    form_class = PressInquiryForm
    template_name = 'press/press-inquiry.html'

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super(PressInquiryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PressInquiryView, self).get_context_data(**kwargs)
        context['form_success'] = 'success' in self.request.GET
        return context

    def get_success_url(self):
        return reverse('press.press-inquiry') + '?success=True'

    def form_valid(self, form):
        self.send_email(form)
        return super(PressInquiryView, self).form_valid(form)

    def send_email(self, form):
        subject = PRESS_INQUIRY_EMAIL_SUBJECT
        sender = PRESS_INQUIRY_EMAIL_FROM
        to = PRESS_INQUIRY_EMAIL_TO
        msg = render_to_string('press/emails/press-inquiry.txt', form.cleaned_data,
                               request=self.request)

        email = EmailMessage(subject, msg, sender, to)
        email.send()

    def render_to_response(self, context, **response_kwargs):
        return l10n_utils.render(self.request,
                                 self.get_template_names(),
                                 context,
                                 **response_kwargs)


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
        msg = render_to_string('press/emails/speaker-request.txt', form.cleaned_data,
                               request=self.request)

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
