from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.validators import EMPTY_VALUES
from captcha.fields import ReCaptchaField
from l10n_utils.dotlang import _
from product_details import product_details

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

        policy_txt = _('I agree to the <a href="%s">Privacy Policy</a>')
        return mark_safe(
            '<label for="%s" class="privacy-check-label">'
            '%s '
            '<span class="title">%s</span></label>' 
            % (attrs['id'], input_txt,
               policy_txt.format('/en-US/privacy-policy'))
         )

class EmailInput(widgets.TextInput):
    input_type = 'email'

class NewsletterForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(attrs={'required':'true'}))
    fmt = forms.ChoiceField(widget=forms.RadioSelect(renderer=SideRadios),
                            choices=FORMATS,
                            initial='H')
    privacy = forms.BooleanField(widget=PrivacyWidget)

class NewsletterCountryForm(NewsletterForm):
    def __init__(self, locale, *args, **kwargs):
        regions = product_details.get_regions(locale)
        regions = sorted(regions.iteritems(), key=lambda x: x[1])
        locale = locale.lower()

        if locale.find('-') != -1:
            locale = locale.split('-')[1]

        super(NewsletterCountryForm, self).__init__(*args, **kwargs)
        self.fields['country'] = forms.ChoiceField(choices=regions,
                                                   initial=locale)

INTEREST_CHOICES = (('', 'Area of interest?'),
                    ('Support', 'Helping Users'),
                    ('QA', 'Testing and QA'),
                    ('Coding', 'Coding'),
                    ('Marketing', 'Marketing'),
                    ('Localization', 'Localization'),
                    ('Webdev', 'Web Development'),
                    ('Add-ons', 'Add-ons'),
                    ('Design', 'Visual Design'),
                    ('Students', 'Student Reps'),
                    ('Documentation', 'Developer Documentation'),
                    ('Accessibility', 'Accessibility'),
                    ('IT', 'Systems Administration'),
                    ('Research', 'User Research'),
                    ('Thunderbird', 'Thunderbird'),
                    (' ', 'Other'),
                    ('Firefox Suggestions', 'I have a suggestion for Firefox'),
                    ('Firefox Issue', 'I need help with a Firefox issue'))

class ContributeForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(attrs={'required':'true'}))
    privacy = forms.BooleanField(widget=PrivacyWidget)
    newsletter = forms.BooleanField(required=False)
    interest = forms.ChoiceField(choices=INTEREST_CHOICES)
    comments = forms.CharField(widget=forms.widgets.Textarea(attrs={'required':'true', 'rows':'', 'cols':''}))
    captcha = ReCaptchaField(attrs={'theme':'clean'})
