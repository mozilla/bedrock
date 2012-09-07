import re

from django import forms

from l10n_utils.dotlang import _


class SMSSendForm(forms.Form):
    number = forms.CharField(max_length=14)
    optin = forms.BooleanField()

    def clean_number(self):
        mobile = self.cleaned_data['number']
        mobile = re.sub(r'\D+', '', mobile)
        if len(mobile) == 10:
            mobile = '1' + mobile
        elif len(mobile) != 11 or mobile[0] != '1':
            raise forms.ValidationError(_('Must be a valid U.S. phone number'))
        return mobile
