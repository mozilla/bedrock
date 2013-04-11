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

from captcha.fields import ReCaptchaField
from l10n_utils.dotlang import _
from product_details import product_details

from .email_contribute import INTEREST_CHOICES


FORMATS = (('H', 'HTML'), ('T', 'Text'))
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
