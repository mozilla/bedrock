# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms
from django.conf import settings


def newsletter_choices():
    choices = []
    for key in settings.BRAZE_API_NEWSLETTERS.keys():
        choices.append((key, key))
    return choices


class NewsletterForm(forms.Form):
    email = forms.EmailField()
    newsletter = forms.ChoiceField(choices=newsletter_choices)
    subscriber_campaign = forms.CharField(max_length=100, required=False)
    subscriber_medium = forms.CharField(max_length=100, required=False)
    subscriber_source = forms.CharField(max_length=100, required=False)
    subscriber_language = forms.CharField(max_length=5, required=False)
    subscriber_country = forms.CharField(max_length=2, required=False)
    subscriber_form_source = forms.CharField(max_length=100, required=False)
