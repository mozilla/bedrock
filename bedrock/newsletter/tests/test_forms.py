# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import mock

from bedrock.mozorg.tests import TestCase

from ..forms import (BooleanRadioRenderer, UnlabeledTableCellRadios,
                     NewsletterForm, ManageSubscriptionsForm)
from .test_views import newsletters


class TestRenderers(TestCase):

    def test_radios(self):
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
        # Boolean renderer starts with True selected if value given is True
        choices = ((False, "False"), (True, "True"))
        renderer = BooleanRadioRenderer("name", value="True", attrs={},
                                        choices=choices)
        output = str(renderer)

        # The True choice should be checked
        self.assertIn('checked=checked value="True"', output)

    def test_boolean_false(self):
        # Boolean renderer starts with False selected if value given is True
        choices = ((False, "False"), (True, "True"))
        renderer = BooleanRadioRenderer("name", value="False", attrs={},
                                        choices=choices)
        output = str(renderer)

        # The False choice should be checked
        self.assertIn('checked=checked value="False"', output)


class TestManageSubscriptionsForm(TestCase):
    def test_locale(self):
        # Get initial lang and country from 'initial' if provided there,
        # else from the locale passed in
        # First, not passed in
        locale = "en-US"
        form = ManageSubscriptionsForm(locale=locale, initial={})
        self.assertEqual('en', form.initial['lang'])
        self.assertEqual('us', form.initial['country'])
        form = ManageSubscriptionsForm(locale=locale,
                                       initial={
                                           'lang': 'pt',
                                           'country': 'br',
                                       })
        self.assertEqual('pt', form.initial['lang'])
        self.assertEqual('br', form.initial['country'])

    def test_long_language(self):
        # Suppose their selected language in ET is a long form ("es-ES")
        # while we only have the short forms ("es") in our list of
        # valid languages.  We should fake it - add es-ES to the choices
        # so that it both shows up, and is selected by default.
        locale = "es-ES"
        form = ManageSubscriptionsForm(locale=locale,
                                       initial={
                                           'lang': 'es-ES',
                                           'country': 'es',
                                       })
        # Initial value is 'es-ES'
        self.assertEqual('es-ES', form.initial['lang'])
        # es-ES is one of the valid choices for this field
        self.assertIn('es-ES', [x[0] for x in form.fields['lang'].choices])


class TestNewsletterForm(TestCase):
    @mock.patch('bedrock.newsletter.utils.get_newsletters')
    def test_form(self, get_newsletters):
        # test NewsletterForm
        # not much to test, but at least construct one
        get_newsletters.return_value = newsletters
        title = "Newsletter title"
        newsletter = 'newsletter-a'
        initial = {
            'title': title,
            'newsletter': newsletter,
            'subscribed': True,
            'english_only': False,
        }
        form = NewsletterForm(initial=initial)
        rendered = str(form)
        self.assertIn(newsletter, rendered)
        self.assertIn(title, rendered)
        # And validate one
        form = NewsletterForm(data=initial)
        self.assertTrue(form.is_valid())
        self.assertEqual(title, form.cleaned_data['title'])
