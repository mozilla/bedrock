# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django import forms

from bedrock.mozorg.forms import (HoneyPotWidget)


class SendToDeviceWidgetForm(forms.Form):
    number = forms.CharField(max_length=20, min_length=4, required=False)
    email = forms.EmailField(max_length=100, required=False)
    platform = forms.ChoiceField(choices=(
        ('ios', 'ios'),
        ('android', 'android'),
        ('all', 'all'),
    ), required=False)

    def clean_number(self):
        number = self.cleaned_data['number']
        if number:
            number = re.sub(r'\D+', '', number)

        return number


class UnfckForm(forms.Form):
    unfck_field = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.Textarea(),
    )

    # honeypot
    office_fax = forms.CharField(widget=HoneyPotWidget, required=False)

    def clean_office_fax(self):
        cleaned_data = super(UnfckForm, self).clean()
        honeypot = cleaned_data.pop('office_fax', None)

        if honeypot:
            raise forms.ValidationError('Your submission could not be processed')
