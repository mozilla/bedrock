from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.validators import EMPTY_VALUES

FORMATS = (('H', 'HTML'), ('T', 'Text'))

class SideRadios(widgets.RadioFieldRenderer):
    """Render radio buttons as labels"""

    def render(self):
        radios = [unicode(w) for idx, w in enumerate(self)]

        return mark_safe(''.join(radios))

class PrivacyWidget(widgets.CheckboxInput):
    """Render a checkbox with privacy text. Lots of pages need this so
    it should be standardized"""

    def render(self, name, value, attrs=None):
        attrs['required'] = 'true'
        input_txt = super(PrivacyWidget, self).render(name, value, attrs)
        return ('<label for="privacy-check" class="privacy-check-label">'
                '%s '
                '<span class="title">I agree to the '
                '<a href="/en-US/privacy-policy">Privacy Policy</a>'
                '</span></label>') % input_txt

class EmailInput(widgets.TextInput):
    input_type = 'email'

class NewsletterForm(forms.Form):
    email = forms.EmailField(label='hello', required=False, 
                             widget=EmailInput(attrs={'required':'true'}))
    fmt = forms.ChoiceField(widget=forms.RadioSelect(renderer=SideRadios),
                            choices=FORMATS,
                            initial='H')
    privacy = forms.BooleanField(widget=PrivacyWidget, required=False)

    def ensure(self, name):
        data = self.cleaned_data.get(name) or None
        if data in EMPTY_VALUES:
            raise forms.ValidationError("%s is required" % name.title())
    
    def clean_email(self):
        self.ensure('email')
        return self.cleaned_data['email']

    def clean_privacy(self):
        self.ensure('privacy')
        return self.cleaned_data['privacy']

