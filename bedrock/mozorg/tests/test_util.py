# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.test.utils import override_settings

from nose.tools import ok_

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg.util import hide_contrib_form


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')


class TestHideContribForm(TestCase):
    @override_settings(ROOT=ROOT)
    def test_lang_file_is_hiding(self):
        """
        `hide_contrib_form` should return true if lang file has the
        comment (## hide_form ##), and false otherwise.
        """
        # 'de' lang file has 'active' and 'hide_form' comments
        ok_(hide_contrib_form('de'))
        # 'fr' lang file has 'active' comment
        ok_(not hide_contrib_form('fr'))
        # 'pt-BR' lang file has hide_form' comment
        ok_(hide_contrib_form('pt-BR'))
        # 'sl' lang file has no comments
        ok_(not hide_contrib_form('sl'))
