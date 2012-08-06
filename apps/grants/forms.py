from django import forms
from models import Grant


class GrantForm (forms.ModelForm):
    formatted_value = forms.CharField(max_length=401, label='Amount')
    focus_area = forms.CharField(max_length=200, label='Focus Area')

    class Meta:
        model = Grant
        fields = ('grantee', 'title', 'formatted_value', 'year', 'focus_area')
