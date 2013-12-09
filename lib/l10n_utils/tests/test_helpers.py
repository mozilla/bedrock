# coding: utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mock import patch
import jingo

from bedrock.mozorg.tests import TestCase


def render(s, context=None):
    t = jingo.env.from_string(s)
    return t.render(context or {})


@patch('lib.l10n_utils.helpers.lang_file_has_tag')
class TestL10nHasTag(TestCase):
    def test_gets_right_langfile(self, lfht_mock):
        lfht_mock.return_value = True
        res = render('{{ "nihilist" if l10n_has_tag("abide") }}',
                     {'langfile': 'dude'})
        self.assertEqual(res, 'nihilist')
        lfht_mock.assert_called_with('dude', tag='abide')

    def test_override_langfile(self, lfht_mock):
        lfht_mock.return_value = True
        res = render('{{ "nihilist" if l10n_has_tag("abide", "uli") }}',
                     {'langfile': 'dude'})
        self.assertEqual(res, 'nihilist')
        lfht_mock.assert_called_with('uli', tag='abide')
