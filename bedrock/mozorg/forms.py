# coding: utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from datetime import datetime
from operator import itemgetter
from random import randrange

from django import forms
from django.conf import settings
from django.forms import widgets
from django.utils.safestring import mark_safe

import basket
from basket.base import request

from captcha.fields import ReCaptchaField
from lib.l10n_utils.dotlang import _
from lib.l10n_utils.dotlang import _lazy
from product_details import product_details

from .email_contribute import INTEREST_CHOICES


FORMATS = (('H', _lazy('HTML')), ('T', _lazy('Text')))
LANGS = settings.NEWSLETTER_LANGUAGES
LANGS_TO_STRIP = ['en-US', 'es']
PARENTHETIC_RE = re.compile(r' \([^)]+\)$')
LANG_FILES = 'mozorg/contribute'


def strip_parenthetical(lang_name):
    """
    Remove the parenthetical from the end of the language name string.
    """
    return PARENTHETIC_RE.sub('', lang_name, 1)


def get_lang_choices():
    """
     Return a localized list of choices for language.
    """
    lang_choices = []
    for lang in LANGS:
        if lang in product_details.languages:
            lang_name = product_details.languages[lang]['native']
        else:
            try:
                locale = [loc for loc in product_details.languages.keys()
                          if loc.startswith(lang)][0]
            except IndexError:
                continue
            lang_name = product_details.languages[locale]['native']
        lang_choices.append([lang, strip_parenthetical(lang_name)])
    return sorted(lang_choices, key=itemgetter(1))


class SideRadios(widgets.RadioFieldRenderer):
    """Render radio buttons as labels"""

    def render(self):
        radios = [unicode(w) for idx, w in enumerate(self)]

        return mark_safe(''.join(radios))


class PrivacyWidget(widgets.CheckboxInput):
    """Render a checkbox with privacy text. Lots of pages need this so
    it should be standardized"""

    def render(self, name, value, attrs=None):
        attrs['required'] = 'required'
        input_txt = super(PrivacyWidget, self).render(name, value, attrs)

        policy_txt = _(u'I’m okay with you handling this info as you explain '
                       u'in your <a href="%s">Privacy Policy</a>')
        return mark_safe(
            '<label for="%s" class="privacy-check-label">'
            '%s '
            '<span class="title">%s</span></label>'
            % (attrs['id'], input_txt,
               policy_txt % '/en-US/privacy-policy')
         )


class HoneyPotWidget(widgets.CheckboxInput):
    """Render a checkbox to (hopefully) trick bots. Will be used on many pages."""

    def render(self, name, value, attrs=None):
        honeypot_txt = _(u'Check this box if you are not human.')
        # semi-randomized in case we have more than one per page.
        # this is maybe/probably overthought
        honeypot_id = 'super-priority-' + str(randrange(1001)) + '-' + str(datetime.now().strftime("%Y%m%d%H%M%S%f"))
        return mark_safe(
            '<div class="super-priority-field">'
            '<label for="%s" class="super-priority-check-label">%s</label>'
            '<input type="checkbox" name="superpriority" id="%s">'
            '</div>' % (honeypot_id, honeypot_txt, honeypot_id))


class EmailInput(widgets.TextInput):
    input_type = 'email'

NEWSLETTER_CHOICES = (('app-dev',) * 2,
                      ('mozilla-and-you',) * 2)


class NewsletterForm(forms.Form):
    newsletter = forms.ChoiceField(choices=NEWSLETTER_CHOICES,
                                   widget=forms.HiddenInput)
    email = forms.EmailField(widget=EmailInput(attrs={'required': 'required'}))
    fmt = forms.ChoiceField(widget=forms.RadioSelect(renderer=SideRadios),
                            choices=FORMATS,
                            initial='H')
    privacy = forms.BooleanField(widget=PrivacyWidget)
    source_url = forms.URLField(verify_exists=False, required=False)

    LANG_CHOICES = get_lang_choices()

    def __init__(self, locale, *args, **kwargs):
        regions = product_details.get_regions(locale)
        regions = sorted(regions.iteritems(), key=lambda x: x[1])

        lang = country = locale.lower()
        if '-' in lang:
            lang, country = lang.split('-', 1)
        lang = lang if lang in LANGS else 'en'

        super(NewsletterForm, self).__init__(*args, **kwargs)
        self.fields['country'] = forms.ChoiceField(choices=regions,
                                                   initial=country,
                                                   required=False)
        self.fields['lang'] = forms.ChoiceField(choices=self.LANG_CHOICES,
                                                initial=lang,
                                                required=False)


class ContributeForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(attrs={'required': 'required'}))
    privacy = forms.BooleanField(widget=PrivacyWidget)
    newsletter = forms.BooleanField(required=False)
    interest = forms.ChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.Select(attrs={'required': 'required'}))
    comments = forms.CharField(
        widget=forms.widgets.Textarea(attrs={'required': 'required',
                                             'rows': '4',
                                             'cols': '30'}))
    captcha = ReCaptchaField(attrs={'theme': 'clean'})


class WebToLeadForm(forms.Form):
    # l10n handled in the template
    interest_choices = (
        ('Firefox for Desktop', 'Firefox for Desktop'),
        ('Firefox for Android', 'Firefox for Android'),
        ('Firefox Marketplace', 'Firefox Marketplace'),
        ('Firefox OS', 'Firefox OS'),
        ('Persona', 'Persona'),
        ('Marketing and Co-promotions', 'Marketing and Co-promotions'),
        ('Other', 'Other'),
    )

    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=80, required=True)
    title = forms.CharField(max_length=40, required=False)
    company = forms.CharField(max_length=40, required=True)
    URL = forms.URLField(max_length=80, required=False)
    email = forms.EmailField(max_length=80, required=True)
    phone = forms.CharField(max_length=40, required=False)
    mobile = forms.CharField(max_length=40, required=False)
    interest = forms.MultipleChoiceField(choices=interest_choices,
                                         required=False)
    description = forms.CharField(required=False)
    superpriority = forms.BooleanField(widget=HoneyPotWidget, required=False)
    # uncomment below to debug salesforce
    # debug = forms.IntegerField(required=False)
    # debugEmail = forms.EmailField(required=False)


class ContributeUniversityAmbassadorForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    current_status = forms.ChoiceField(
        choices=(('', _lazy('Current Status')),
                 ('student', _lazy('Student')), ('teacher', _lazy('Teacher')),
                 ('administrator', _lazy('Administrator')),
                 ('other', _lazy('Other'))))
    school = forms.CharField(max_length=100)
    expected_graduation_year = forms.ChoiceField(
        required=False,
        choices=([('', _lazy('Expected Graduation Year'))] +
                 [(i, str(i)) for i in range(datetime.now().year,
                                             datetime.now().year + 8)]))
    area = forms.ChoiceField(
        required=False,
        choices=[('', _lazy('Area of Study')),
                 ('computer science', _lazy('Computer Science')),
                 ('computer engineering', _lazy('Computer Engineering')),
                 ('engineering', _lazy('Engineering (other)')),
                 ('social science', _lazy('Social Science')),
                 ('science', _lazy('Science (other)')),
                 ('business/marketing', _lazy('Business/Marketing')),
                 ('education', _lazy('Education')),
                 ('mathematics', _lazy('Mathematics')),
                 ('other', _lazy('Other'))])
    area_free_text = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100)
    country = forms.ChoiceField()
    fmt = forms.ChoiceField(widget=forms.RadioSelect(renderer=SideRadios),
                            label=_lazy('Email format preference:'),
                            choices=FORMATS, initial='H')
    age_confirmation = forms.BooleanField(
        widget=widgets.CheckboxInput(),
        label=_lazy(u'I’m 18 years old and eligible to participate in '
                    'the program'))
    share_information = forms.BooleanField(
        required=False,
        widget=widgets.CheckboxInput(),
        label=_lazy(u'Please share my contact information and interests with '
                    'related Mozilla contributors for the purpose of '
                    'collaborating on Mozilla projects'))
    privacy = forms.BooleanField(widget=PrivacyWidget)
    nl_mozilla_and_you = forms.BooleanField(
        required=False,
        widget=widgets.CheckboxInput(),
        label=_lazy(u'Firefox & You: A monthly newsletter packed with tips to'
                    ' improve your browsing experience'))
    nl_mobile = forms.BooleanField(
        required=False,
        widget=widgets.CheckboxInput(),
        label=_lazy(u'Firefox for Android: Get the power of Firefox in the'
                    ' palm of your hand'))
    nl_firefox_flicks = forms.BooleanField(
        required=False,
        widget=widgets.CheckboxInput(),
        label=_lazy(u'Firefox Flicks'))
    nl_about_mozilla = forms.BooleanField(
        required=False,
        widget=widgets.CheckboxInput(),
        label=_lazy(u'About Mozilla: News from the Mozilla Project'))
    captcha = ReCaptchaField(attrs={'theme': 'clean'})
    source_url = forms.URLField(verify_exists=False, required=False)

    def __init__(self, *args, **kwargs):
        locale = kwargs.get('locale', 'en-US')
        super(ContributeUniversityAmbassadorForm, self).__init__(*args, **kwargs)
        country_list = product_details.get_regions(locale).items()
        country_list = sorted(country_list, key=lambda country: country[1])
        country_list.insert(0, ('', _('Country')))
        self.fields['country'].choices = country_list

    def clean(self, *args, **kwargs):
        super(ContributeUniversityAmbassadorForm, self).clean(*args, **kwargs)
        if (self.cleaned_data.get('current_status', '') == 'student'
                and not self.cleaned_data.get('expected_graduation_year', '')):
            self._errors['expected_graduation_year'] = (
                self.error_class([_('This field is required.')]))
        return self.cleaned_data

    def clean_expected_graduation_year(self):
        return self.cleaned_data.get('expected_graduation_year', '')

    def clean_area(self):
        return self.cleaned_data.get('area_free_field',
                                     self.cleaned_data['area'])

    def clean_share_information(self):
        if self.cleaned_data.get('share_information', False):
            return 'Y'
        return 'N'

    def newsletters(self):
        newsletters = ['ambassadors']
        for newsletter in ['nl_mozilla_and_you', 'nl_mobile',
                           'nl_firefox_flicks', 'nl_about_mozilla']:
            if self.cleaned_data.get(newsletter, False):
                newsletters.append(newsletter[3:].replace('_', '-'))
        return newsletters

    def save(self):
        data = self.cleaned_data
        result = basket.subscribe(data['email'], self.newsletters(),
                                  format=data['fmt'], country=data['country'],
                                  welcome_message='Student_Ambassadors_Welcome',
                                  source_url=data['source_url'])

        data = {
            'FIRST_NAME': data['first_name'],
            'LAST_NAME': data['last_name'],
            'STUDENTS_CURRENT_STATUS': data['current_status'],
            'STUDENTS_SCHOOL': data['school'],
            'STUDENTS_GRAD_YEAR': data['expected_graduation_year'],
            'STUDENTS_MAJOR': data['area'],
            'COUNTRY_': data['country'],
            'STUDENTS_CITY': data['city'],
            'STUDENTS_ALLOW_SHARE': data['share_information'],
        }
        request('post', 'custom_update_student_ambassadors',
                token=result['token'], data=data)
