# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import re
from operator import itemgetter

from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.safestring import mark_safe

from product_details import product_details

from bedrock.mozorg.forms import (FORMATS, EmailInput, PrivacyWidget,
                                  SideRadios, strip_parenthetical)
from bedrock.newsletter import utils
from lib.l10n_utils.dotlang import _, _lazy


_newsletters_re = re.compile(r'^[\w,-]+$')

LANG_FILES = ['mozorg/newsletters']


def validate_newsletters(newsletters):
    if not newsletters:
        raise ValidationError('No Newsletter Provided')

    newsletters = newsletters.replace(' ', '')
    if not _newsletters_re.match(newsletters):
        raise ValidationError('Invalid Newsletter')

    return newsletters


def get_lang_choices(newsletters=None):
    """
     Return a localized list of choices for language.

     List looks like: [[lang_code, lang_name], [lang_code, lang_name], ...]

     :param newsletters: Either a comma separated string or a list of newsletter ids.
    """
    lang_choices = []
    languages = utils.get_languages_for_newsletters(newsletters)

    for lang in languages:
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


def newsletter_title(newsletter):
    """Given a newsletter's key, return its title if we can,
    otherwise return the key
    """
    newsletters = utils.get_newsletters()
    if newsletter in newsletters and 'title' in newsletters[newsletter]:
        return newsletters[newsletter]['title']
    return newsletter


class UnlabeledTableCellRadios(widgets.RadioFieldRenderer):
    """Render radio buttons as table cells, without their labels"""

    def render(self):
        radios = [w.tag() for w in self]
        if radios:
            return mark_safe('<td>' + '</td><td>'.join(radios) + "</td>")
        return mark_safe('')


class BooleanRadioRenderer(widgets.RadioFieldRenderer):
    """Return a boolean with two radio buttons, the first meaning
    true and the second false, rendered as two table cells.
    """
    def render(self):
        if self.value is True or self.value == 'True':
            trueattrs = 'checked=checked'
            falseattrs = ''
        else:
            trueattrs = ''
            falseattrs = 'checked=checked'

        template = \
            """
            <td>
              <input type="radio" name="{name}" {trueattrs} value="True">
            </td>
            <td>
              <input type="radio" name="{name}" {falseattrs} value="False">
            </td>
            """
        result = template.format(
            name=self.name,
            trueattrs=trueattrs,
            falseattrs=falseattrs
        )
        return mark_safe(result)


class TableCheckboxInput(widgets.CheckboxInput):
    """Add table cell markup around the rendered checkbox, so we can use
    it interchangeably with the BooleanRadioRenderer"""
    def render(self, *args, **kwargs):
        out = super(TableCheckboxInput, self).render(*args, **kwargs)
        return mark_safe("<td>" + out + "</td>")


class ManageSubscriptionsForm(forms.Form):
    """
    Form used on manage subscriptions page for the user's information,
    like email address and language preference.

    @param locale: locale string, e.g. "en-US".  Will be used to set
    country and lang defaults if not otherwise provided in initial
    or bound data.
    @param args: Other standard form args
    @param kwargs: Other standard form kwargs
    """

    format = forms.ChoiceField(widget=forms.RadioSelect(renderer=SideRadios),
                               choices=FORMATS,
                               initial='H')
    remove_all = forms.BooleanField(required=False)

    country = forms.ChoiceField(choices=[],  # will set choices based on locale
                                required=False)
    lang = forms.ChoiceField(choices=[],     # will set choices based on newsletter languages
                             required=False)

    def __init__(self, locale, *args, **kwargs):
        regions = product_details.get_regions(locale)
        regions = sorted(regions.iteritems(), key=itemgetter(1))
        lang_choices = get_lang_choices()
        languages = [x[0] for x in lang_choices]

        lang = country = locale.lower()
        if '-' in lang:
            lang, country = lang.split('-', 1)
        lang = lang if lang in languages else 'en'

        self.newsletters = kwargs.pop('newsletters', [])

        # Get initial - work with a copy so we're not modifying the
        # data that was passed to us
        initial = kwargs.get('initial', {}).copy()
        if not initial.get('country', None):
            initial['country'] = country
        if not initial.get('lang', None):
            initial['lang'] = lang
        else:
            lang = initial['lang']

        # Sometimes people are in ET with a language that is spelled a
        # little differently from our list. E.g. we have 'es' on our
        # list, but in ET their language is 'es-ES'. Try to find a match
        # for their current lang in our list and use that. If we can't
        # find one, then fall back to guessing from their locale,
        # ignoring what they had in ET.  (This is just for the initial
        # value on the form; they can always change to another valid
        # language before submitting.)
        if lang not in languages:
            for valid_lang, _unused in lang_choices:
                # if the first two chars match, close enough
                if lang.lower()[:2] == valid_lang.lower()[:2]:
                    lang = valid_lang
                    break
            else:
                # No luck - guess from the locale
                lang = locale.lower()
                if '-' in lang:
                    lang, _unused = lang.split('-', 1)
            initial['lang'] = lang

        kwargs['initial'] = initial
        super(ManageSubscriptionsForm, self).__init__(*args, **kwargs)
        self.fields['country'].choices = regions
        self.fields['lang'].choices = lang_choices

        self.already_subscribed = initial.get('newsletters', [])

    def clean(self):
        valid_newsletters = utils.get_newsletters()
        for newsletter in self.newsletters:
            if newsletter not in valid_newsletters:
                msg = _("%s is not a valid newsletter") % newsletter
                raise ValidationError(msg)
        return super(ManageSubscriptionsForm, self).clean()


class NewsletterForm(forms.Form):
    """
    Form to let a user subscribe to or unsubscribe from a newsletter
    on the manage existing newsletters page.  Used in a FormSet.
    """
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    subscribed_radio = forms.BooleanField(
        widget=forms.RadioSelect(renderer=BooleanRadioRenderer),
        required=False,  # they have to answer, but answer can be False
    )
    subscribed_check = forms.BooleanField(
        widget=TableCheckboxInput,
        required=False,  # they have to answer, but answer can be False
    )
    newsletter = forms.CharField(widget=forms.HiddenInput)


class NewsletterFooterForm(forms.Form):
    """
    Form used to subscribe to a single newsletter, typically in the
    footer of a page (see newsletters/middleware.py) but sometimes
    on a dedicated page.
    """
    email = forms.EmailField(widget=EmailInput(attrs={'required': 'required'}))
    # first/last_name not yet included in email_newsletter_form helper
    # currently used on /contribute/friends/ (custom markup)
    first_name = forms.CharField(widget=forms.TextInput, required=False)
    last_name = forms.CharField(widget=forms.TextInput, required=False)
    privacy = forms.BooleanField(widget=PrivacyWidget)
    source_url = forms.URLField(required=False)
    newsletters = forms.CharField(widget=forms.HiddenInput,
                                  required=True,
                                  max_length=100)

    # has to take a newsletters argument so it can figure
    # out which languages to list in the form.
    def __init__(self, newsletters, locale, data=None, *args, **kwargs):
        regions = product_details.get_regions(locale)
        regions = sorted(regions.iteritems(), key=itemgetter(1))

        try:
            newsletters = validate_newsletters(newsletters)
        except ValidationError:
            # replace with most common good newsletter
            # form validation will work with submitted data
            newsletters = 'mozilla-and-you'

        lang = locale.lower()
        if '-' in lang:
            lang, country = lang.split('-', 1)
        else:
            country = ''
            regions.insert(0, ('', _lazy('Select country')))
        lang_choices = get_lang_choices(newsletters)
        languages = [x[0] for x in lang_choices]
        if lang not in languages:
            # The lang from their locale is not one that our newsletters
            # are translated into. Initialize the language field to no
            # choice, to force the user to pick one of the languages that
            # we do support.
            lang = ''
            lang_choices.insert(0, ('', _lazy('Available Languages')))

        super(NewsletterFooterForm, self).__init__(data, *args, **kwargs)

        required_args = {
            'required': 'required',
            'aria-required': 'true',
        }
        country_widget = widgets.Select(attrs=required_args)
        self.fields['country'] = forms.ChoiceField(widget=country_widget,
                                                   choices=regions,
                                                   initial=country,
                                                   required=False)
        lang_widget = widgets.Select(attrs=required_args)
        self.fields['lang'] = forms.TypedChoiceField(widget=lang_widget,
                                                     choices=lang_choices,
                                                     initial=lang,
                                                     required=False)
        self.fields['newsletters'].initial = newsletters

    def clean_newsletters(self):
        return validate_newsletters(self.cleaned_data['newsletters'])


class EmailForm(forms.Form):
    """
    Form to enter email, e.g. to be sent a recovery message
    """
    email = forms.EmailField(widget=EmailInput(attrs={'required': 'required'}))
