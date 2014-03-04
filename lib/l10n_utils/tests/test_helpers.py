# coding: utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from babel.core import UnknownLocaleError
from mock import patch
from nose.tools import eq_

from bedrock.mozorg.tests import TestCase
from l10n_utils import helpers


@patch.object(helpers, 'lang_file_has_tag')
class TestL10nHasTag(TestCase):
    def test_gets_right_langfile(self, lfht_mock):
        helpers.l10n_has_tag({'langfile': 'dude'}, 'abide')
        lfht_mock.assert_called_with('dude', tag='abide')

    def test_override_langfile(self, lfht_mock):
        helpers.l10n_has_tag({'langfile': 'dude'}, 'abide', 'uli')
        lfht_mock.assert_called_with('uli', tag='abide')


class TestCurrentLocale(TestCase):
    @patch('l10n_utils.helpers.Locale')
    def test_unknown_locale(self, Locale):
        """
        If Locale.parse raises an UnknownLocaleError, return the en-US
        locale object.
        """
        Locale.parse.side_effect = UnknownLocaleError('foo')
        eq_(helpers.current_locale(), Locale.return_value)
        Locale.assert_called_with('en', 'US')

    @patch('l10n_utils.helpers.Locale')
    def test_value_error(self, Locale):
        """
        If Locale.parse raises a ValueError, return the en-US locale
        object.
        """
        Locale.parse.side_effect = ValueError
        eq_(helpers.current_locale(), Locale.return_value)
        Locale.assert_called_with('en', 'US')

    @patch('l10n_utils.helpers.get_language')
    @patch('l10n_utils.helpers.Locale')
    def test_success(self, Locale, get_language):
        eq_(helpers.current_locale(), Locale.parse.return_value)
        Locale.parse.assert_called_with(get_language.return_value, sep='-')


class TestL10nFormatDate(TestCase):
    @patch('l10n_utils.helpers.current_locale')
    @patch('l10n_utils.helpers.format_date')
    def test_success(self, format_date, current_locale):
        eq_(helpers.l10n_format_date('somedate', format='long'),
            format_date.return_value)
        format_date.assert_called_with(
            'somedate', locale=current_locale.return_value, format='long')
