# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import shutil
import tempfile
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.test import TestCase

from bedrock.settings import base as base_settings
from bedrock.settings.base import get_dev_languages


class AcceptedLocalesTest(TestCase):
    """Test lazy evaluation of locale related settings.

    Verify that some localization-related settings are lazily evaluated based
    on the current value of the DEV variable.  Depending on the value,
    DEV_LANGUAGES or PROD_LANGUAGES should be used.

    """

    @classmethod
    def setup_class(cls):
        """Point FLUENT_REPO_PATH at a throwaway l10n checkout.

        The stand-in contains:

            - en-US/
            - fr/
            - metadata/
            - empty_file

        A temporary directory rather than the real data/www-l10n keeps this
        class from disturbing other tests that may be reading the Fluent
        files at the same time in another pytest worker.

        Also, set PROD_LANGUAGES to ('en-US',).

        """
        cls.DEV = settings.DEV
        cls.PROD_LANGUAGES = settings.PROD_LANGUAGES
        cls.DEV_LANGUAGES = settings.DEV_LANGUAGES
        settings.PROD_LANGUAGES = ("en-US",)
        cls.locale = Path(tempfile.mkdtemp())
        for loc in ("en-US", "fr", "metadata"):
            (cls.locale / loc).mkdir()
        (cls.locale / "empty_file").touch()
        cls.repo_path_patch = mock.patch.object(base_settings, "FLUENT_REPO_PATH", cls.locale)
        cls.repo_path_patch.start()

    @classmethod
    def teardown_class(cls):
        """Remove the testing locale dir and restore the patched settings."""

        cls.repo_path_patch.stop()
        settings.DEV = cls.DEV
        settings.PROD_LANGUAGES = cls.PROD_LANGUAGES
        settings.DEV_LANGUAGES = cls.DEV_LANGUAGES
        shutil.rmtree(cls.locale)

    def test_build_dev_languages(self):
        """Test that the list of dev locales is built properly.

        On dev instances, the list of accepted locales should correspond to
        the per-locale directories in locale/.

        """
        settings.DEV = True
        langs = get_dev_languages()
        assert langs == ["en-US", "fr"] or langs == ["fr", "en-US"], "DEV_LANGUAGES do not correspond to the contents of locale/."

    def test_dev_languages(self):
        """Test the accepted locales on dev instances.

        On dev instances, allow locales defined in DEV_LANGUAGES.

        """
        settings.DEV = True
        # simulate the successful result of the DEV_LANGUAGES list
        # comprehension defined in settings.
        settings.DEV_LANGUAGES = [
            "en-US",
            "fr",
            "de",
            "es-MX",
        ]
        assert settings.LANGUAGE_URL_MAP == {
            "en-US": "en-US",
            "fr": "fr",
            "de": "de",
            "es-MX": "es-MX",
        }, "DEV is True, but DEV_LANGUAGES are not used to define the allowed locales."

    def test_prod_languages(self):
        """Test the accepted locales on prod instances.

        On stage/prod instances, allow locales defined in PROD_LANGUAGES.

        """
        settings.DEV = False
        assert settings.LANGUAGE_URL_MAP == {"en-US": "en-US"}, "DEV is False, but PROD_LANGUAGES are not used to define the allowed locales."
