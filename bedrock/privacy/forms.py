# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.forms import widgets


class EmailInput(widgets.TextInput):
    input_type = 'email'


class PrivacyContactForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'required': 'true'
            }))
    sender = forms.EmailField(
        required=True,
        widget=EmailInput(
            attrs={
                'required': 'true',
                'placeholder': 'you@yourdomain.com'
            }))
    comments = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'required': 'true',
                'placeholder': 'Enter your comments...',
                'rows': '10',
                'cols': '77'
            }))
