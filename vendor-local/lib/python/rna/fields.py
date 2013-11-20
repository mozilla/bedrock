from django import forms

from rest_framework.compat import parse_datetime


class ISO8601DateTimeField(forms.DateTimeField):
    def strptime(self, value, format):
        return parse_datetime(value)
