from django import forms

from bedrock.newsletter.forms import NewsletterFooterForm


class VPNWaitlistForm(NewsletterFooterForm):
    PLATFORM_CHOICES = (
        ('windows', 'Windows 10'),
        ('ios', 'iOS'),
        ('android', 'Android'),
        ('mac', 'Mac'),
        ('chromebook', 'Chromebook'),
        ('linux', 'Linux'),
    )
    platforms = forms.MultipleChoiceField(required=False,
                                          choices=PLATFORM_CHOICES,
                                          widget=forms.CheckboxSelectMultiple)

    def __init__(self, locale, data=None, *args, **kwargs):
        super().__init__('guardian-vpn-waitlist', locale, data, *args, **kwargs)
