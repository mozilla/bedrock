# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django import forms

from bedrock.newsletter.forms import NewsletterFooterForm


class VPNWaitlistForm(NewsletterFooterForm):
    PLATFORM_CHOICES = (
        ("windows", "Windows 10"),
        ("ios", "iOS"),
        ("android", "Android"),
        ("mac", "Mac"),
        ("chromebook", "Chromebook"),
        ("linux", "Linux"),
    )
    fpn_platform = forms.MultipleChoiceField(required=False, choices=PLATFORM_CHOICES, widget=forms.CheckboxSelectMultiple)

    def __init__(self, locale, data=None, *args, **kwargs):
        super().__init__("guardian-vpn-waitlist", locale, data, *args, **kwargs)
