# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import mock

from bedrock.mozorg.tests import TestCase
from bedrock.newsletter.forms import (
    BooleanRadioRenderer, ManageSubscriptionsForm,
    NewsletterFooterForm, NewsletterForm, UnlabeledTableCellRadios,
)
from bedrock.newsletter.tests import newsletters


newsletters_mock = mock.Mock()
newsletters_mock.return_value = newsletters


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

    def test_str_true(self):
        """renderer starts with True selected if value given is True"""
        choices = ((False, "False"), (True, "True"))
        renderer = BooleanRadioRenderer("name", value="True", attrs={},
                                        choices=choices)
        output = str(renderer)

        # The True choice should be checked
        self.assertIn('checked=checked value="True"', output)

    def test_str_false(self):
        """renderer starts with False selected if value given is False"""
        choices = ((False, "False"), (True, "True"))
        renderer = BooleanRadioRenderer("name", value="False", attrs={},
                                        choices=choices)
        output = str(renderer)

        # The False choice should be checked
        self.assertIn('checked=checked value="False"', output)

    def test_boolean_true(self):
        """renderer starts with True selected if value given is True"""
        choices = ((False, "False"), (True, "True"))
        renderer = BooleanRadioRenderer("name", value=True, attrs={},
                                        choices=choices)
        output = str(renderer)

        # The True choice should be checked
        self.assertIn('checked=checked value="True"', output)

    def test_boolean_false(self):
        """renderer starts with False selected if value given is False"""
        choices = ((False, "False"), (True, "True"))
        renderer = BooleanRadioRenderer("name", value=False, attrs={},
                                        choices=choices)
        output = str(renderer)

        # The False choice should be checked
        self.assertIn('checked=checked value="False"', output)


class TestManageSubscriptionsForm(TestCase):
    @mock.patch('bedrock.newsletter.forms.get_lang_choices')
    def test_locale(self, langs_mock):
        """Get initial lang, country from the right places"""
        # Get initial lang and country from 'initial' if provided there,
        # else from the locale passed in
        # First, not passed in
        langs_mock.return_value = [['en', 'English'], ['pt', 'Portuguese']]
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


@mock.patch('bedrock.newsletter.utils.get_newsletters', newsletters_mock)
class TestNewsletterForm(TestCase):
    def test_form(self):
        """test NewsletterForm"""
        # not much to test, but at least construct one
        title = "Newsletter title"
        newsletter = 'newsletter-a'
        initial = {
            'title': title,
            'newsletter': newsletter,
            'subscribed_radio': True,
            'subscribed_check': True,
        }
        form = NewsletterForm(initial=initial)
        rendered = str(form)
        self.assertIn(newsletter, rendered)
        self.assertIn(title, rendered)
        # And validate one
        form = NewsletterForm(data=initial)
        self.assertTrue(form.is_valid())
        self.assertEqual(title, form.cleaned_data['title'])

    def test_multiple_newsletters(self):
        """Should allow to subscribe to multiple newsletters at a time."""
        newsletters = 'mozilla-and-you,beta'
        data = {
            'email': 'dude@example.com',
            'lang': 'en',
            'privacy': 'Y',
            'fmt': 'H',
            'newsletters': newsletters,
        }
        form = NewsletterFooterForm(newsletters, 'en-US', data=data.copy())
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['newsletters'], newsletters)

        # whitespace shouldn't matter
        form = NewsletterFooterForm('mozilla-and-you , beta ', 'en-US', data=data.copy())
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['newsletters'], newsletters)


@mock.patch('bedrock.newsletter.utils.get_newsletters', newsletters_mock)
class TestNewsletterFooterForm(TestCase):
    newsletter_name = 'mozilla-and-you'

    def test_form(self):
        """Form works normally"""
        data = {
            'email': 'foo@example.com',
            'lang': 'fr',
            'first_name': 'Walter',
            'last_name': 'Sobchak',
            'privacy': True,
            'fmt': 'H',
            'source_url': 'https://accounts.firefox.com',
            'newsletters': self.newsletter_name,
        }
        form = NewsletterFooterForm(self.newsletter_name, locale='en-US', data=data.copy())
        self.assertTrue(form.is_valid(), form.errors)
        cleaned_data = form.cleaned_data
        self.assertEqual(data['fmt'], cleaned_data['fmt'])
        self.assertEqual(data['lang'], cleaned_data['lang'])
        self.assertEqual(data['source_url'], cleaned_data['source_url'])

    def test_source_url_non_url(self):
        """Form works normally"""
        data = {
            'email': 'foo@example.com',
            'lang': 'fr',
            'first_name': 'Walter',
            'last_name': 'Sobchak',
            'privacy': True,
            'fmt': 'H',
            'source_url': 'about:devtools?dude=abiding',
            'newsletters': self.newsletter_name,
        }
        form = NewsletterFooterForm(self.newsletter_name, locale='en-US', data=data.copy())
        self.assertTrue(form.is_valid(), form.errors)
        cleaned_data = form.cleaned_data
        self.assertEqual(data['source_url'], cleaned_data['source_url'])

    def test_source_url_too_long(self):
        """Form works normally"""
        data = {
            'email': 'foo@example.com',
            'lang': 'fr',
            'first_name': 'Walter',
            'last_name': 'Sobchak',
            'privacy': True,
            'fmt': 'H',
            'source_url': 'about:devtools' * 20,
            'newsletters': self.newsletter_name,
        }
        form = NewsletterFooterForm(self.newsletter_name, locale='en-US', data=data.copy())
        self.assertTrue(form.is_valid(), form.errors)
        cleaned_data = form.cleaned_data
        self.assertEqual(data['source_url'][:255], cleaned_data['source_url'])

    def test_country_default(self):
        """country defaults based on the locale.

        But only for country based locales (e.g. pt-BR)"""
        form = NewsletterFooterForm(self.newsletter_name, locale='fr')
        self.assertEqual('', form.fields['country'].initial)
        form = NewsletterFooterForm(self.newsletter_name, locale='pt-BR')
        self.assertEqual('br', form.fields['country'].initial)
        form = NewsletterFooterForm(self.newsletter_name, locale='zh-TW')
        self.assertEqual('tw', form.fields['country'].initial)

    def test_lang_choices_per_newsletter(self):
        """Lang choices should be based on the newsletter."""
        form = NewsletterFooterForm('beta', 'en-US')
        choices = [lang[0] for lang in form.fields['lang'].choices]
        self.assertEqual(choices, ['en'])

        form = NewsletterFooterForm('join-mozilla', 'en-US')
        choices = [lang[0] for lang in form.fields['lang'].choices]
        self.assertEqual(choices, ['en', 'es'])

    def test_lang_choices_multiple_newsletters(self):
        """Lang choices should be based on all newsletters."""
        form = NewsletterFooterForm('join-mozilla,firefox-tips', 'en-US')
        choices = [lang[0] for lang in form.fields['lang'].choices]
        self.assertEqual(choices, ['de', 'en', 'es', 'fr', 'pt', 'ru'])

    def test_lang_default(self):
        """lang defaults based on the locale"""
        form = NewsletterFooterForm(self.newsletter_name, locale='pt-BR')
        self.assertEqual('pt', form.fields['lang'].initial)

    def test_lang_default_not_supported(self):
        """lang defaults to blank if not supported by newsletter."""
        form = NewsletterFooterForm('beta', locale='pt-BR')
        self.assertEqual('', form.fields['lang'].initial)

    def test_lang_not_required(self):
        """lang not required since field not always displayed"""
        data = {
            'email': 'foo@example.com',
            'privacy': True,
            'fmt': 'H',
            'newsletters': self.newsletter_name,
        }
        form = NewsletterFooterForm(self.newsletter_name, locale='en-US', data=data.copy())
        self.assertTrue(form.is_valid(), form.errors)
        # Form returns '' for lang, so we don't accidentally change the user's
        # preferred language thinking they entered something here that they
        # didn't.
        self.assertEqual(u'', form.cleaned_data['lang'])

    def test_privacy_required(self):
        """they have to check the privacy box"""
        data = {
            'email': 'foo@example.com',
            'privacy': False,
            'fmt': 'H',
            'newsletters': self.newsletter_name,
        }
        form = NewsletterFooterForm(self.newsletter_name, locale='en-US', data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('privacy', form.errors)

    def test_invalid_newsletter_is_error(self):
        """Invalid newsletter should not raise exception. Bug 1072302.

        Instead, an invalid newsletter name should manifest as a normal
        form error.
        """
        data = {
            'email': 'fred@example.com',
            'lang': 'fr',
            'privacy': True,
            'fmt': 'H',
            'newsletters': '',
        }
        form = NewsletterFooterForm('', locale='en-US', data=data.copy())
        self.assertFalse(form.is_valid())
        self.assertIn('newsletters', form.errors)
        self.assertEqual(form.errors['newsletters'], [u'This field is required.'])

        invalid_newsletter = '!nv@l1d'
        data = {
            'email': 'fred@example.com',
            'lang': 'fr',
            'privacy': True,
            'fmt': 'H',
            'newsletters': invalid_newsletter,
        }
        form = NewsletterFooterForm(invalid_newsletter, locale='en-US', data=data.copy())
        self.assertFalse(form.is_valid())
        self.assertIn('newsletters', form.errors)
        self.assertEqual(form.errors['newsletters'], [u'Invalid Newsletter'])
