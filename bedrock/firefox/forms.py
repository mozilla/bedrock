# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django import forms


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
