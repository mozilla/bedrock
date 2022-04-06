# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms

from bedrock.mozorg.forms import (
    DateInput,
    EmailInput,
    HoneyPotWidget,
    NumberInput,
    TelInput,
    TimeInput,
    URLInput,
)

SPEAKER_REQUEST_FILE_SIZE_LIMIT = 5242880  # 5MB


class PressInquiryForm(forms.Form):
    jobtitle = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "required", "required": "required", "aria-required": "true"}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "required", "required": "required", "aria-required": "true"}))
    user_email = forms.EmailField(
        max_length=254,  # max length allowed for emails
        required=True,
        widget=EmailInput(
            attrs={
                "required": "required",
                "class": "required",
                "aria-required": "true",
            }
        ),
    )
    media_org = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "required", "required": "required", "aria-required": "true"}))
    inquiry = forms.CharField(
        required=True, widget=forms.Textarea(attrs={"class": "required", "required": "required", "aria-required": "true", "rows": "", "cols": ""})
    )
    deadline = forms.CharField(required=True, widget=DateInput(attrs={"class": "required", "required": "required", "aria-required": "true"}))

    # honeypot
    office_fax = forms.CharField(widget=HoneyPotWidget, required=False)

    def clean_office_fax(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.pop("office_fax", None)

        if honeypot:
            raise forms.ValidationError("Your submission could not be processed")


class SpeakerRequestForm(forms.Form):
    # event fields
    sr_event_name = forms.CharField(
        max_length=255,
        required=True,
        error_messages={
            "required": "Please enter a name for the event.",
        },
        widget=forms.TextInput(
            attrs={
                "class": "required",
                "required": "required",
                "aria-required": "true",
            }
        ),
    )
    sr_event_url = forms.URLField(
        max_length=2000,
        required=True,
        error_messages={
            "required": "Please enter a URL.",
            "invalid": "Please enter a valid URL.",
        },
        widget=URLInput(
            attrs={
                "class": "required",
                "required": "required",
                "aria-required": "true",
                "placeholder": "http://www.my-event.com",
            }
        ),
    )
    sr_event_date = forms.CharField(
        required=True,
        error_messages={
            "required": "Please provide a date.",
        },
        widget=DateInput(
            attrs={
                "class": "required",
                "required": "required",
                "aria-required": "true",
            }
        ),
    )
    sr_event_time = forms.CharField(
        required=True,
        error_messages={
            "required": "Please provide a time.",
        },
        widget=TimeInput(
            attrs={
                "class": "required",
                "required": "required",
                "aria-required": "true",
            }
        ),
    )
    sr_guest_speaker1 = forms.CharField(
        max_length=200,
        required=False,
    )
    sr_guest_speaker2 = forms.CharField(
        max_length=200,
        required=False,
    )

    # contact fields
    sr_contact_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "required": "required",
                "class": "required",
                "aria-required": "true",
            }
        ),
    )
    sr_contact_title = forms.CharField(
        max_length=200,
        required=False,
    )
    sr_contact_company = forms.CharField(
        max_length=200,
        required=False,
    )
    sr_contact_phone = forms.CharField(
        max_length=50,
        required=False,
        widget=TelInput(),
    )
    sr_contact_email = forms.EmailField(
        max_length=254,  # max length allowed for emails
        required=True,
        error_messages={
            "invalid": "Please enter a valid email address",
        },
        widget=EmailInput(
            attrs={
                "required": "required",
                "class": "required",
                "aria-required": "true",
            }
        ),
    )
    sr_contact_company_url = forms.URLField(
        max_length=2000,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "http://www.my-company.com",
            }
        ),
    )

    # event details fields
    sr_event_venue = forms.CharField(
        max_length=400,
        required=False,
    )
    sr_event_theme = forms.CharField(
        max_length=200,
        required=False,
    )
    sr_event_goal = forms.CharField(
        max_length=300,
        required=False,
    )
    sr_event_format = forms.CharField(
        max_length=200,
        required=False,
    )
    sr_event_audience_size = forms.IntegerField(
        required=False,
        widget=NumberInput(
            attrs={
                "min": 1,
                "placeholder": 25,
            }
        ),
    )
    sr_event_audience_demographics = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": "",
                "cols": "",
            }
        ),
    )
    sr_event_speakers_confirmed = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": "",
                "cols": "",
            }
        ),
    )
    sr_event_speakers_invited = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": "",
                "cols": "",
            }
        ),
    )
    sr_event_speakers_past = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": "",
                "cols": "",
            }
        ),
    )
    sr_event_media_coverage = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": "",
                "cols": "",
            }
        ),
    )
    sr_event_sponsors = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": "",
                "cols": "",
            }
        ),
    )
    sr_event_confirmation_deadline = forms.DateField(
        required=False,
        widget=DateInput(),
    )

    # presentation details fields
    sr_presentation_type = forms.MultipleChoiceField(
        required=False,
        choices=(
            ("keynote", "Keynote"),
            ("presentation", "Presentation"),
            ("fireside chat", "Fireside Chat"),
            ("panel", "Panel"),
            ("other", "Other"),
        ),
        widget=forms.CheckboxSelectMultiple(),
    )
    sr_presentation_panelists = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(),
    )
    sr_presentation_topic = forms.CharField(
        required=False,
        max_length=255,
    )
    sr_presentation_length = forms.IntegerField(
        required=False,
        widget=NumberInput(
            attrs={
                "min": 0.5,
                "step": 0.5,
                "placeholder": 2.5,
            }
        ),
    )

    # additional info fields
    sr_attachment = forms.FileField(
        required=False,
    )

    # honeypot
    office_fax = forms.CharField(widget=HoneyPotWidget, required=False)

    def clean_sr_attachment(self):
        cleaned_data = super().clean()
        attachment = cleaned_data.get("sr_attachment")

        if attachment:
            if attachment.size > SPEAKER_REQUEST_FILE_SIZE_LIMIT:
                raise forms.ValidationError("Attachment must not exceed 5MB")

        return attachment

    def clean_office_fax(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.pop("office_fax", None)

        if honeypot:
            raise forms.ValidationError("Your submission could not be processed")
