# coding: utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from operator import itemgetter

import re
from datetime import datetime
from random import randrange

from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

import basket
from basket.base import request

from lib.l10n_utils.dotlang import _
from lib.l10n_utils.dotlang import _lazy
from product_details import product_details

from .email_contribute import INTEREST_CHOICES


FORMATS = (('H', _lazy('HTML')), ('T', _lazy('Text')))
LANGS_TO_STRIP = ['en-US', 'es']
PARENTHETIC_RE = re.compile(r' \([^)]+\)$')
LANG_FILES = ['mozorg/contribute', 'firefox/partners/index']


def strip_parenthetical(lang_name):
    """
    Remove the parenthetical from the end of the language name string.
    """
    return PARENTHETIC_RE.sub('', lang_name, 1)


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

        policy_txt = _(u'I’m okay with Mozilla handling my info as explained '
                       u'in <a href="%s">this Privacy Policy</a>')
        return mark_safe(
            '<label for="%s" class="privacy-check-label">'
            '%s '
            '<span class="title">%s</span></label>'
            % (attrs['id'], input_txt,
               policy_txt % reverse('privacy'))
        )


class HoneyPotWidget(widgets.TextInput):
    """Render a text field to (hopefully) trick bots. Will be used on many pages."""

    def render(self, name, value, attrs=None):
        honeypot_txt = _(u'Leave this field empty.')
        # semi-randomized in case we have more than one per page.
        # this is maybe/probably overthought
        honeypot_id = 'office-fax-' + str(randrange(1001)) + '-' + str(datetime.now().strftime("%Y%m%d%H%M%S%f"))
        return mark_safe(
            '<div class="super-priority-field">'
            '<label for="%s">%s</label>'
            '<input type="text" name="office_fax" id="%s">'
            '</div>' % (honeypot_id, honeypot_txt, honeypot_id))


class URLInput(widgets.TextInput):
    input_type = 'url'


class EmailInput(widgets.TextInput):
    input_type = 'email'


class DateInput(widgets.DateInput):
    input_type = 'date'


class TimeInput(widgets.TimeInput):
    input_type = 'time'


class TelInput(widgets.TextInput):
    input_type = 'tel'


class NumberInput(widgets.TextInput):
    input_type = 'number'


class L10nSelect(forms.Select):
    def render_option(self, selected_choices, option_value, option_label):
        if option_value == '':
            option_label = u'-- {0} --'.format(_('select'))
        return super(L10nSelect, self).render_option(selected_choices, option_value, option_label)


class ContributeSignupForm(forms.Form):
    required_attr = {'required': 'required'}
    empty_choice = ('', '')
    category_choices = (
        ('coding', _lazy('Coding')),
        ('testing', _lazy('Testing')),
        ('writing', _lazy('Writing')),
        ('teaching', _lazy('Teaching')),
        ('helping', _lazy('Helping')),
        ('translating', _lazy('Translating')),
        ('activism', _lazy('Activism')),
        ('dontknow', _lazy(u'I don’t know')),
    )
    coding_choices = (
        empty_choice,
        ('coding-firefox', _lazy('Firefox')),
        ('coding-firefoxos', _lazy('Firefox OS')),
        ('coding-websites', _lazy('Websites')),
        ('coding-addons', _lazy('Firefox add-ons')),
        ('coding-marketplace', _lazy('HTML5 apps')),
        ('coding-webcompat', _lazy('Diagnosing Web compatibility issues')),
        ('coding-cloud', _lazy('Online services')),
    )
    testing_choices = (
        empty_choice,
        ('testing-firefox', _lazy('Firefox and Firefox OS')),
        ('testing-addons', _lazy('Firefox add-ons')),
        ('testing-marketplace', _lazy('HTML5 apps')),
        ('testing-webcompat', _lazy('Web compatibility')),
    )
    translating_choices = (
        empty_choice,
        ('translating-products', _lazy('Products')),
        ('translating-websites', _lazy('Websites')),
        ('translating-tools', _lazy(u'I’d like to work on localization tools')),
    )
    writing_choices = (
        empty_choice,
        ('writing-social', _lazy('Social media')),
        ('writing-journalism', _lazy('Journalism')),
        ('writing-techusers', _lazy('Technical docs for users')),
        ('writing-techdevs', _lazy('Technical docs for developers')),
        ('writing-addons', _lazy('Technical docs for Firefox add-ons')),
        ('writing-marketplace', _lazy('Technical docs for HTML5 apps')),
    )
    teaching_choices = (
        empty_choice,
        ('teaching-webmaker', _lazy('Teach the Web (Webmaker)')),
        ('teaching-fellowships', _lazy('Open News fellowships')),
        ('teaching-hive', _lazy('Hive - Community based digital education')),
        ('teaching-science', _lazy('Open Web science research')),
    )

    email = forms.EmailField(widget=EmailInput(attrs=required_attr))
    privacy = forms.BooleanField(widget=PrivacyWidget)
    category = forms.ChoiceField(choices=category_choices,
                                 widget=forms.RadioSelect(attrs=required_attr))
    area_coding = forms.ChoiceField(choices=coding_choices, required=False, widget=L10nSelect)
    area_testing = forms.ChoiceField(choices=testing_choices, required=False, widget=L10nSelect)
    area_translating = forms.ChoiceField(choices=translating_choices, required=False,
                                         widget=L10nSelect)
    area_writing = forms.ChoiceField(choices=writing_choices, required=False, widget=L10nSelect)
    area_teaching = forms.ChoiceField(choices=teaching_choices, required=False, widget=L10nSelect)
    name = forms.CharField(widget=forms.TextInput(attrs=required_attr))
    message = forms.CharField(widget=forms.Textarea, required=False)
    newsletter = forms.BooleanField(required=False)
    format = forms.ChoiceField(widget=forms.RadioSelect(attrs=required_attr), choices=(
        ('H', _lazy('HTML')),
        ('T', _lazy('Text')),
    ))

    def __init__(self, locale, *args, **kwargs):
        regions = product_details.get_regions(locale)
        regions = sorted(regions.iteritems(), key=itemgetter(1))
        regions.insert(0, self.empty_choice)
        super(ContributeSignupForm, self).__init__(*args, **kwargs)
        self.locale = locale
        self.fields['country'] = forms.ChoiceField(choices=regions, widget=L10nSelect)

    def clean(self):
        cleaned_data = super(ContributeSignupForm, self).clean()
        category = cleaned_data.get('category')
        # only bother if category was supplied
        if category:
            area_name = 'area_' + category
            if area_name in cleaned_data and not cleaned_data[area_name]:
                required_message = self.fields[area_name].error_messages['required']
                self._errors[area_name] = self.error_class([required_message])
                del cleaned_data[area_name]

        return cleaned_data


class ContributeForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(attrs={'required': 'required'}))
    privacy = forms.BooleanField(widget=PrivacyWidget)
    newsletter = forms.BooleanField(required=False)
    interest = forms.ChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.Select(attrs={'required': 'required'}))
    comments = forms.CharField(
        widget=forms.widgets.Textarea(attrs={'rows': '4',
                                             'cols': '30'}))
    # honeypot
    office_fax = forms.CharField(widget=HoneyPotWidget, required=False)


class WebToLeadForm(forms.Form):
    interests_standard = (
        ('Firefox for Desktop', _lazy(u'Firefox for Desktop')),
        ('Firefox for Android', _lazy(u'Firefox for Android')),
        ('Firefox Marketplace', _lazy(u'Firefox Marketplace')),
        ('Firefox OS', _lazy(u'Firefox OS')),
        ('Persona', _lazy(u'Persona')),
        ('Marketing and Co-promotions', _lazy(u'Marketing and Co-promotions')),
        ('Other', _lazy(u'Other')),
    )

    interests_fx = (
        ('Firefox for Android', _lazy(u'Firefox for Android')),
        ('Firefox Marketplace', _lazy(u'Firefox Marketplace')),
        ('Firefox OS', _lazy(u'Firefox OS')),
        ('Other', _lazy(u'Other')),
    )

    first_name = forms.CharField(
        max_length=40,
        required=True,
        error_messages={
            'required': _lazy(u'Please enter your first name.')
        },
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _lazy(u'First Name'),
                'class': 'required',
                'required': 'required',
                'aria-required': 'true'
            }
        )
    )
    last_name = forms.CharField(
        max_length=80,
        required=True,
        error_messages={
            'required': _('Please enter your last name.')
        },
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _lazy(u'Last Name'),
                'class': 'required',
                'required': 'required',
                'aria-required': 'true'
            }
        )
    )
    title = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _lazy(u'Title')
            }
        )
    )
    company = forms.CharField(
        max_length=40,
        required=True,
        error_messages={
            'required': _lazy(u'Please enter your company name.')
        },
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _lazy(u'Company'),
                'class': 'required',
                'required': 'required',
                'aria-required': 'true'
            }
        )
    )
    URL = forms.URLField(
        max_length=80,
        required=False,
        error_messages={
            'invalid': _lazy(u'Please supply a valid URL.')
        },
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _lazy(u'Website')
            }
        )
    )
    email = forms.EmailField(
        max_length=80,
        required=True,
        error_messages={
            'required': _lazy(u'Please enter your email address.'),
            'invalid': _lazy(u'Please enter a valid email address')
        },
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _lazy(u'Email'),
                'class': 'required',
                'required': 'required',
                'aria-required': 'true'
            }
        )
    )
    phone = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _lazy(u'Phone')
            }
        )
    )
    mobile = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'size': 20,
                'placeholder': _lazy(u'Mobile')
            }
        )
    )
    street = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': _lazy(u'Address'),
                'rows': '',
                'cols': ''
            }
        )
    )
    city = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': _lazy(u'City')
            }
        )
    )
    state = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': _lazy(u'State/Province')
            }
        )
    )
    country = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': _lazy(u'Country')
            }
        )
    )
    zip = forms.CharField(
        required=False,
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': _lazy(u'Zip')
            }
        )
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': _lazy(u'Description'),
                'rows': '',
                'cols': ''
            }
        )
    )
    # honeypot
    office_fax = forms.CharField(widget=HoneyPotWidget, required=False)
    # uncomment below to debug salesforce
    # debug = forms.IntegerField(required=False)
    # debugEmail = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        interest_set = kwargs.pop('interest_set', 'standard')
        interest_choices = self.interests_fx if (interest_set == 'fx') else self.interests_standard
        kwargs.pop('lead_source', None)

        super(WebToLeadForm, self).__init__(*args, **kwargs)

        self.fields['interest'] = forms.MultipleChoiceField(
            choices=interest_choices,
            required=False,
            widget=forms.SelectMultiple(
                attrs={
                    'title': _lazy(u'Interest'),
                    'size': 7
                }
            )
        )


class ContributeStudentAmbassadorForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    status = forms.ChoiceField(
        choices=(('', ''),
                 ('student', _lazy('Student')), ('teacher', _lazy('Teacher')),
                 ('administrator', _lazy('Administrator')),
                 ('other', _lazy('Other'))))
    school = forms.CharField(max_length=100)
    grad_year = forms.ChoiceField(
        required=False,
        choices=([('', _lazy('Expected Graduation Year'))] +
                 [(i, str(i)) for i in range(datetime.now().year,
                                             datetime.now().year + 8)]))
    major = forms.ChoiceField(
        required=False,
        choices=[('', ''),
                 ('computer science', _lazy('Computer Science')),
                 ('computer engineering', _lazy('Computer Engineering')),
                 ('engineering', _lazy('Engineering (other)')),
                 ('social science', _lazy('Social Science')),
                 ('science', _lazy('Science (other)')),
                 ('business/marketing', _lazy('Business/Marketing')),
                 ('education', _lazy('Education')),
                 ('mathematics', _lazy('Mathematics')),
                 ('other', _lazy('Other'))])
    major_free_text = forms.CharField(max_length=100, required=False)
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
    # honeypot
    office_fax = forms.CharField(widget=HoneyPotWidget, required=False)
    source_url = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        locale = kwargs.get('locale', 'en-US')
        super(ContributeStudentAmbassadorForm, self).__init__(*args, **kwargs)
        country_list = product_details.get_regions(locale).items()
        country_list = sorted(country_list, key=lambda country: country[1])
        country_list.insert(0, ('', ''))
        self.fields['country'].choices = country_list

    def clean(self, *args, **kwargs):
        super(ContributeStudentAmbassadorForm, self).clean(*args, **kwargs)
        if (self.cleaned_data.get('status', '') == 'student'
                and not self.cleaned_data.get('grad_year', '')):
            self._errors['grad_year'] = (
                self.error_class([_('This field is required.')]))
        return self.cleaned_data

    def clean_grad_year(self):
        return self.cleaned_data.get('grad_year', '')

    def clean_major(self):
        return self.cleaned_data.get('major_free_field',
                                     self.cleaned_data['major'])

    def clean_share_information(self):
        if self.cleaned_data.get('share_information', False):
            return 'Y'
        return 'N'

    def clean_office_fax(self):
        honeypot = self.cleaned_data.pop('office_fax', None)

        if honeypot:
            raise forms.ValidationError(
                _('Your submission could not be processed'))

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
            'STUDENTS_CURRENT_STATUS': data['status'],
            'STUDENTS_SCHOOL': data['school'],
            'STUDENTS_GRAD_YEAR': data['grad_year'],
            'STUDENTS_MAJOR': data['major'],
            'COUNTRY_': data['country'],
            'STUDENTS_CITY': data['city'],
            'STUDENTS_ALLOW_SHARE': data['share_information'],
        }
        request('post', 'custom_update_student_ambassadors',
                token=result['token'], data=data)
