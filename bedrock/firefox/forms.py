# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms

import phonenumbers


class SMSSendToDeviceForm(forms.Form):
    phone_number = forms.CharField(max_length=20, required=False)
    platform = forms.ChoiceField(
        choices=(
            ("ios", "ios"),
            ("android", "android"),
            ("all", "all"),
        ),
        required=False,
    )

    def clean_phone_number(self):
        region_code = "US"  # US only for proof of concept.
        number = self.cleaned_data["phone_number"]

        # For testing purposes we accept 5555555555 (no formatting).
        if number == "5555555555":
            return number

        try:
            pn = phonenumbers.parse(number, region_code)
        except phonenumbers.NumberParseException:
            raise forms.ValidationError("Invalid phone number")

        if not phonenumbers.is_valid_number_for_region(pn, region_code):
            raise forms.ValidationError(f"Invalid phone number for region: {region_code}")

        return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
