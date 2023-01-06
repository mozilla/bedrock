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

        translation.activate("non-default")
        self.assertEqual(translation.get_language(), "non-default")

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
