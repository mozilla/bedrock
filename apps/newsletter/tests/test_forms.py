# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import mock

from mozorg.tests import TestCase

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
        self.assertEqual('en', form.fields['lang'].initial)
        self.assertEqual('us', form.fields['country'].initial)
        form = ManageSubscriptionsForm(locale=locale,
                                       initial={
                                           'lang': 'pt',
                                           'country': 'br',
                                       })
        self.assertEqual('pt', form.fields['lang'].initial)
        self.assertEqual('br', form.fields['country'].initial)

    @mock.patch('newsletter.utils.get_newsletters')
    def test_must_subscribe(self, get_newsletters):
        # if must_subscribe is set, there must be at least one item
        # in .newsletters or validation will fail
        # (These are not fields, just attributes we set on the form
        # as we go along to help validate all the input)
        get_newsletters.return_value = newsletters
        locale = "en-US"
        data = {'email': 'user@example.com', 'format': 'H', 'lang': 'en'}
        form = ManageSubscriptionsForm(locale=locale, data=data)
        form.must_subscribe = True
        form.newsletters = []
        self.assertFalse(form.is_valid())
        form = ManageSubscriptionsForm(locale=locale, data=data)
        form.must_subscribe = True
        form.newsletters = ['mozilla-and-you']
        self.assertTrue(form.is_valid(), msg=str(form.errors))
        form = ManageSubscriptionsForm(locale=locale, data=data)
        form.must_subscribe = False
        form.newsletters = []
        self.assertTrue(form.is_valid())

    @mock.patch('newsletter.utils.get_newsletters')
    def test_newsletters_in_language(self, get_newsletters):
        # you cannot subscribe to newsletters that aren't available
        # in the language that you've chosen
        get_newsletters.return_value = newsletters
        locale = "en-US"
        data = {'email': 'user@example.com', 'format': 'H'}
        form = ManageSubscriptionsForm(locale=locale, data=data)
        form.newsletters = ['no-such-english-newsletter']
        self.assertFalse(form.is_valid())


class TestNewsletterForm(TestCase):
    @mock.patch('newsletter.utils.get_newsletters')
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
        }
        form = NewsletterForm(initial=initial)
        rendered = str(form)
        self.assertIn(newsletter, rendered)
        self.assertIn(title, rendered)
        # And validate one
        form = NewsletterForm(data=initial)
        self.assertTrue(form.is_valid())
        self.assertEqual(title, form.cleaned_data['title'])
