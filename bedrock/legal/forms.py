# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms

from bedrock.mozorg.forms import HoneyPotWidget

FRAUD_REPORT_FILE_SIZE_LIMIT = 5242880  # 5MB


class FraudReportForm(forms.Form):
    input_url = forms.URLField(
        max_length=2000,
        required=True,
        error_messages={
            "required": "Please enter a URL.",
        },
        widget=forms.TextInput(
            attrs={
                "size": 40,
                "placeholder": "http://offendingsite.com",
                "class": "required fill-width",
                "required": "required",
                "aria-required": "true",
            }
        ),
    )
    input_category = forms.ChoiceField(
        choices=(
            ("Charging for software", "Charging for software"),
            ("Collecting personal information", "Collecting personal information"),
            ("Domain name violation", "Domain name violation"),
            ("Logo misuse/modification", "Logo misuse/modification"),
            ("Distributing modified Firefox/malware", "Distributing modified Firefox/malware"),
        ),
        required=True,
        error_messages={
            "required": "Please select a category.",
        },
        widget=forms.Select(
            attrs={
                "title": "Category",
                "class": "required",
                "required": "required",
                "aria-required": "true",
            }
        ),
    )
    input_product = forms.ChoiceField(
        choices=(
            ("Firefox", "Firefox"),
            ("SeaMonkey", "SeaMonkey"),
            ("Thunderbird", "Thunderbird"),
            ("Other Mozilla Product/Project", "Other Mozilla Product/Project (specify)"),
        ),
        required=True,
        error_messages={
            "required": "Please select a product.",
        },
        widget=forms.Select(
            attrs={
                "title": "Product",
                "class": "required",
                "required": "required",
                "aria-required": "true",
            }
        ),
    )
    input_specific_product = forms.CharField(max_length=254, required=False, widget=forms.TextInput(attrs={"size": 20, "class": "fill-width"}))
    input_details = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": "", "cols": "", "class": "fill-width"}))
    input_attachment = forms.ImageField(required=False)
    input_attachment_desc = forms.CharField(
        max_length=254, required=False, widget=forms.Textarea(attrs={"rows": "", "cols": "", "class": "fill-width"})
    )
    input_email = forms.EmailField(
        max_length=254,
        required=False,
        error_messages={
            "invalid": "Please enter a valid email address",
        },
        widget=forms.TextInput(attrs={"size": 20, "class": "fill-width"}),
    )
    # honeypot
    office_fax = forms.CharField(widget=HoneyPotWidget, required=False)

    def clean_input_attachment(self):
        attachment = self.cleaned_data.get("input_attachment")

        if attachment:
            if attachment.size > FRAUD_REPORT_FILE_SIZE_LIMIT:
                raise forms.ValidationError("Attachment must not exceed 5MB")

        return attachment

    def clean_office_fax(self):
        honeypot = self.cleaned_data.pop("office_fax", None)

        if honeypot:
            raise forms.ValidationError("Your submission could not be processed")
