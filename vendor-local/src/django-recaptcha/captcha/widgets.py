from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from captcha import client


class ReCaptcha(forms.widgets.Widget):
    recaptcha_challenge_name = 'recaptcha_challenge_field'
    recaptcha_response_name = 'recaptcha_response_field'

    def __init__(self, public_key=None, use_ssl=None, attrs={}, *args, \
            **kwargs):
        self.public_key = public_key if public_key else \
                settings.RECAPTCHA_PUBLIC_KEY
        self.use_ssl = use_ssl if use_ssl != None else getattr(settings, \
                'RECAPTCHA_USE_SSL', False)
        self.js_attrs = attrs
        super(ReCaptcha, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % client.displayhtml(self.public_key, \
                self.js_attrs, use_ssl=self.use_ssl))

    def value_from_datadict(self, data, files, name):
        return [data.get(self.recaptcha_challenge_name, None),
            data.get(self.recaptcha_response_name, None)]
