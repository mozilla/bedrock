# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.forms import widgets

from bedrock.mozorg.forms import HoneyPotWidget
from lib.l10n_utils.dotlang import _lazy as _


LANG_FILES = 'privacy/ffos_privacy'


class EmailInput(widgets.TextInput):
    input_type = 'email'


class PrivacyContactForm(forms.Form):
    sender = forms.EmailField(
        required=True,
        error_messages={
            'required': _('This field is required, please enter your email address.')
        },
        widget=EmailInput(
            attrs={
                'required': 'required',
                'placeholder': _('you@yourdomain.com')
            }))
    comments = forms.CharField(
        required=True,
        error_messages={
            'required': _('This field is required, please enter your comments or questions.')
        },
        widget=forms.Textarea(
            attrs={
                'required': 'required',
                'placeholder': _('Enter your comments...'),
                'rows': '10',
                'cols': '77'
            }))
    # honeypot
    office_fax = forms.CharField(
        widget=HoneyPotWidget,
        required=False)
