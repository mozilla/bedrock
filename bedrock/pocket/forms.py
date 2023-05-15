# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms
from django.conf import settings


def newsletter_choices():
    choices = []
    for key in settings.BRAZE_API_NEWSLETTERS.keys():
        choices.append((key, key))


class NewsletterForm(forms.Form):
    email = forms.EmailField(required=True)
    newsletter = forms.ChoiceField(choices=newsletter_choices, required=True)
    subscriber_campaign = forms.CharField(max_length=100)
    subscriber_medium = forms.CharField(max_length=100)
    subscriber_source = forms.CharField(max_length=100)
    subscriber_language = forms.CharField(max_length=5)
    subscriber_country = forms.CharField(max_length=2)
    subscriber_form_source = forms.CharField(max_length=100)
