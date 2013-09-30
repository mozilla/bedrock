# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import mock

from bedrock.mozorg.tests import TestCase

from ..forms import (BooleanRadioRenderer, ManageSubscriptionsForm,
                     NewsletterFooterForm, NewsletterForm,
                     UnlabeledTableCellRadios
                     )
from .test_views import newsletters


class TestRenderers(TestCase):

    def test_radios(self):
        """Test radio button renderer"""
        choices = ((123, "NAME_A"), (245, "NAME_2"))
        renderer = UnlabeledTableCellRadios("name", "value", {}, choices)
        output = str(renderer)
        # The choices should not be labeled
        self.assertNotIn("NAME_A", output)
        self.assertNotIn("NAME_2", output)
        # But the values should be in there
        self.assertIn('value="123"', output)
        self.assertIn('value="245"', output)
        # Should be table cells
        self.assertTrue(output.startswith("<td>"))
        self.assertTrue(output.endswith("</td>"))
        self.assertIn("</td><td>", output)

    def test_boolean_true(self):
        """renderer starts with True selected if value given is True"""
        choices = ((False, "False"), (True, "True"))
        renderer = BooleanRadioRenderer("name", value="True", attrs={},
                                        choices=choices)
        output = str(renderer)

        # The True choice should be checked
        self.assertIn('checked=checked value="True"', output)

    def test_boolean_false(self):
        """renderer starts with False selected if value given is False"""
        choices = ((False, "False"), (True, "True"))
        renderer = BooleanRadioRenderer("name", value="False", attrs={},
                                        choices=choices)
        output = str(renderer)

        # The False choice should be checked
        self.assertIn('checked=checked value="False"', output)


class TestManageSubscriptionsForm(TestCase):
    def test_locale(self):
        """Get initial lang, country from the right places"""
        # Get initial lang and country from 'initial' if provided there,
        # else from the locale passed in
        # First, not passed in
        locale = "en-US"
        form = ManageSubscriptionsForm(locale=locale, initial={})
        self.assertEqual('en', form.initial['lang'])
        self.assertEqual('us', form.initial['country'])
        # now, test with them passed in.
        form = ManageSubscriptionsForm(locale=locale,
                                       initial={
                                           'lang': 'pt',
                                           'country': 'br',
                                       })
        self.assertEqual('pt', form.initial['lang'])
        self.assertEqual('br', form.initial['country'])

    @mock.patch('bedrock.newsletter.forms.get_lang_choices')
    def test_long_language(self, langs_mock):
        """Fuzzy match their language preference"""
        # Suppose their selected language in ET is a long form ("es-ES")
        # while we only have the short forms ("es") in our list of
        # valid languages.  Or vice-versa.  Find the match to the one
        # in our list and use that, not the lang from ET.
        locale = 'en-US'
        langs_mock.return_value = [['en', 'English'], ['es', 'Spanish']]
        form = ManageSubscriptionsForm(locale=locale,
                                       initial={
                                           'lang': 'es-ES',
                                           'country': 'es',
                                       })
        # Initial value is 'es'
        self.assertEqual('es', form.initial['lang'])

    def test_bad_language(self):
        """Handle their language preference if it's not valid"""
        # Suppose their selected language in ET is one we don't recognize
        # at all.  Use the language from their locale instead.
        locale = "pt-BR"
        form = ManageSubscriptionsForm(locale=locale,
                                       initial={
                                           'lang': 'zz',
                                           'country': 'es',
                                       })
        self.assertEqual('pt', form.initial['lang'])


class TestNewsletterForm(TestCase):
    @mock.patch('bedrock.newsletter.utils.get_newsletters')
    def test_form(self, get_newsletters):
        """test NewsletterForm"""
        # not much to test, but at least construct one
        get_newsletters.return_value = newsletters
        title = "Newsletter title"
        newsletter = 'newsletter-a'
        initial = {
            'title': title,
            'newsletter': newsletter,
            'subscribed': True,
        }
        form = NewsletterForm(initial=initial)
        rendered = str(form)
        self.assertIn(newsletter, rendered)
        self.assertIn(title, rendered)
        # And validate one
        form = NewsletterForm(data=initial)
        self.assertTrue(form.is_valid())
        self.assertEqual(title, form.cleaned_data['title'])

    @mock.patch('bedrock.newsletter.utils.get_newsletters')
    def test_invalid_newsletter(self, get_newsletters):
        """Should raise a validation error for an invalid newsletter."""
        get_newsletters.return_value = newsletters
        data = {
            'newsletter': 'mozilla-and-you',
            'email': 'dude@example.com',
            'lang': 'en',
            'privacy': 'Y',
            'fmt': 'H',
        }
        form = NewsletterFooterForm('en-US', data=data)
        self.assertTrue(form.is_valid())

        data['newsletter'] = 'does-not-exist'
        form = NewsletterFooterForm('en-US', data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['newsletter'][0], 'does-not-exist is not '
                                                       'a valid newsletter')

    @mock.patch('bedrock.newsletter.utils.get_newsletters')
    def test_multiple_newsletters(self, get_newsletters):
        """Should allow to subscribe to multiple newsletters at a time."""
        get_newsletters.return_value = newsletters
        data = {
            'newsletter': 'mozilla-and-you,beta',
            'email': 'dude@example.com',
            'lang': 'en',
            'privacy': 'Y',
            'fmt': 'H',
        }
        form = NewsletterFooterForm('en-US', data=data.copy())
        self.assertTrue(form.is_valid())

        # whitespace shouldn't matter
        data['newsletter'] = 'mozilla-and-you ,  beta  '
        form = NewsletterFooterForm('en-US', data=data.copy())
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['newsletter'],
                         'mozilla-and-you,beta')

    @mock.patch('bedrock.newsletter.utils.get_newsletters')
    def test_multiple_newsletters_invalid(self, get_newsletters):
        """Should throw error if any newsletter is invalid."""
        get_newsletters.return_value = newsletters
        data = {
            'newsletter': 'mozilla-and-you,beta-DUDE',
            'email': 'dude@example.com',
            'privacy': 'Y',
            'fmt': 'H',
        }
        form = NewsletterFooterForm('en-US', data=data.copy())
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['newsletter'][0], 'beta-DUDE is not '
                                                       'a valid newsletter')


class TestNewsletterFooterForm(TestCase):
    @mock.patch('bedrock.newsletter.utils.get_newsletters')
    def test_form(self, get_newsletters):
        """Form works normally"""
        get_newsletters.return_value = newsletters
        newsletter = u"mozilla-and-you"
        data = {
            'email': 'foo@example.com',
            'lang': 'fr',
            'newsletter': newsletter,
            'privacy': True,
            'fmt': 'H',
        }
        form = NewsletterFooterForm(locale='en-US', data=data)
        self.assertTrue(form.is_valid(), form.errors)
        cleaned_data = form.cleaned_data
        self.assertEqual(data['fmt'], cleaned_data['fmt'])
        self.assertEqual(data['lang'], cleaned_data['lang'])

    def test_country_default(self):
        """country defaults based on the locale"""
        form = NewsletterFooterForm(locale='fr')
        self.assertEqual('fr', form.fields['country'].initial)
        form = NewsletterFooterForm(locale='pt-BR')
        self.assertEqual('br', form.fields['country'].initial)

    def test_lang_default(self):
        """lang defaults based on the locale"""
        form = NewsletterFooterForm(locale='pt-BR')
        self.assertEqual('pt', form.fields['lang'].initial)

    @mock.patch('bedrock.newsletter.utils.get_newsletters')
    def test_lang_not_required(self, get_newsletters):
        """lang not required since field not always displayed"""
        get_newsletters.return_value = newsletters
        newsletter = u"mozilla-and-you"
        data = {
            'email': 'foo@example.com',
            'newsletter': newsletter,
            'privacy': True,
            'fmt': 'H',
        }
        form = NewsletterFooterForm(locale='en-US', data=data)
        self.assertTrue(form.is_valid(), form.errors)
        # Form returns '' for lang, so we don't accidentally change the user's
        # preferred language thinking they entered something here that they
        # didn't.
        self.assertEqual(u'', form.cleaned_data['lang'])

    @mock.patch('bedrock.newsletter.utils.get_newsletters')
    def test_privacy_required(self, get_newsletters):
        """they have to check the privacy box"""
        get_newsletters.return_value = newsletters
        newsletter = u"mozilla-and-you"
        data = {
            'email': 'foo@example.com',
            'newsletter': newsletter,
            'privacy': False,
            'fmt': 'H',
        }
        form = NewsletterFooterForm(locale='en-US', data=data)
        self.assertIn('privacy', form.errors)
