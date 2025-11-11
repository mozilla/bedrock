# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from django.utils import translation

from wagtail.models import Locale as WagtailLocale

from bedrock.base.i18n import normalize_language

logger = logging.getLogger(__name__)


class BedrockLocale(WagtailLocale):
    """Custom Locale model that handles Bedrock's mixed-case language codes.

    Wagtail's default Locale.get_active() uses Django's translation.get_language()
    which returns lowercase codes (e.g., 'es-es'). However, our Locale records
    are stored with mixed-case codes (e.g., 'es-ES'). This subclass normalizes
    the language code before lookup to ensure the correct Locale is found.

    The issue occurs because:
    1. Django normalizes 'es-ES' to lowercase 'es-es' internally
    2. Wagtail's get_supported_content_language_variant() tries to match 'es-es'
    3. When exact match fails, it falls back to the FIRST 'es-*' locale in
       WAGTAIL_CONTENT_LANGUAGES
    4. If 'es-AR' comes before 'es-ES', it returns 'es-AR' instead of 'es-ES'
    5. This causes Locale.get_active() to fail and fall back to default locale

    This fix ensures that the language code is normalized to Bedrock's mixed-case
    format before querying the database, so the correct locale is always found
    regardless of the order in WAGTAIL_CONTENT_LANGUAGES.
    """

    class Meta:
        proxy = True

    @classmethod
    def get_active(cls):
        """
        Gets the Locale for the currently activated language code.

        Overrides Wagtail's implementation to normalize the language code
        before looking it up, ensuring mixed-case codes like 'es-ES' are
        matched correctly even when Django returns lowercase 'es-es'.
        """
        try:
            language_code = translation.get_language()

            # Normalize the language code to match Bedrock's mixed-case format
            normalized_code = normalize_language(language_code)

            if normalized_code:
                locale = cls.objects.get(language_code=normalized_code)
                return locale
            else:
                # If normalization fails, try the original code
                logger.warning(f"[BedrockLocale.get_active] Normalization returned None, using original: {language_code}")
                return cls.objects.get(language_code=language_code)
        except cls.DoesNotExist:
            # Fall back to default locale
            from django.conf import settings

            logger.warning(
                f"[BedrockLocale.get_active] Locale not found for '{normalized_code or language_code}', "
                f"falling back to default: {settings.LANGUAGE_CODE}"
            )
            return cls.objects.get(language_code=settings.LANGUAGE_CODE)
