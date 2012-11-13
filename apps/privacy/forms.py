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
