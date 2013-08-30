# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.test.utils import override_settings

from nose.tools import ok_, eq_

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg.util import hide_contrib_form, get_fb_like_locale


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


class TestGetFacebookLikeLocale(TestCase):

    def test_supported_locale(self):
        """
        Return the given locale if supported.
        """
        eq_(get_fb_like_locale('en-PI'), 'en_PI')

    def test_first_supported_locale_for_language(self):
        """
        If the given locale is not supported, iterate through
        the supported locales and return the first one that
        matches the language.
        """
        eq_(get_fb_like_locale('es-AR'), 'es_ES')

    def test_unsupported_locale(self):
        """
        Return the default en_US when locale isn't supported.
        """
        eq_(get_fb_like_locale('zz-ZZ'), 'en_US')
