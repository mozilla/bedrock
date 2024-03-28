# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.test import TestCase

from lib.l10n_utils import translation


class TestTranslationUtils(TestCase):
    def setUp(self):
        translation.deactivate()

    def test_get_language(self):
        # nothing set, should return default lang
        self.assertEqual(translation.get_language(), settings.LANGUAGE_CODE)

        translation.activate("lang-xx")
        # 2024 Update: we're making Django work with uppercased territories in lang codes
        # but see test__fix_case below for more explanation
        self.assertEqual(translation.get_language(), "lang-XX")

    def test_activate_deactivate(self):
        """Should activate and deactivate languages"""
        self.assertEqual(translation.get_language(), settings.LANGUAGE_CODE)
        translation.activate("de")
        self.assertEqual(translation.get_language(), "de")
        self.assertNotEqual(translation.get_language(), settings.LANGUAGE_CODE)
        translation.deactivate()
        self.assertEqual(translation.get_language(), settings.LANGUAGE_CODE)

    def test_get_language_bidi(self):
        """Should return true if the base lang (before the dash) is "he", "ar", "fa", or "ur".

        List of left-to-right languages are in Django global settings and very unlikely to change.
        """
        translation.activate("en-GB")
        self.assertFalse(translation.get_language_bidi())

        translation.activate("de")
        self.assertFalse(translation.get_language_bidi())

        translation.activate("ar")
        self.assertTrue(translation.get_language_bidi())

        translation.activate("ur-PK")
        self.assertTrue(translation.get_language_bidi())

        translation.activate("skr")
        self.assertTrue(translation.get_language_bidi())

    def test__fix_case(self):
        cases = (
            ("en-us", "en-US"),
            ("EN-gB", "en-GB"),
            ("en", "en"),
            ("zh-hk", "zh-HK"),
            # more complex codes that should not be changed - see function docstring
            ("zh-Hant", "zh-Hant"),
            ("zh-Hant-TW", "zh-Hant-TW"),
            ("zh-HK", "zh-HK"),
            ("zh-Hant-HK", "zh-Hant-HK"),
            ("zh-hant", "zh-hant"),
            ("zh-hant-tw", "zh-hant-tw"),
            ("zh-Hant", "zh-Hant"),
            ("zh-Hant-tw", "zh-Hant-tw"),
            ("zh-Hant-TW", "zh-Hant-TW"),
            ("ja-JP-mac", "ja-JP-mac"),
            # no-ops
            ("dude", "dude"),
            ("the-DUDE", "the-DUDE"),
            ("the-DUDE-abIDeS", "the-DUDE-abIDeS"),
            ("xx", "xx"),
            ("dq", "dq"),
            # very special case
        )
        for val, expected in cases:
            with self.subTest(val=val, expected=expected):
                self.assertEqual(translation._fix_case(val), expected)
