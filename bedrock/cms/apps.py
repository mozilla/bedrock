# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from django.apps import AppConfig


class CmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bedrock.cms"

    def ready(self):
        """Called when Django starts up - we use this to patch Wagtail's Locale model."""
        # Replace Wagtail's Locale.get_active() with our implementation
        self._patch_locale_get_active()

    @staticmethod
    def _patch_locale_get_active():
        """
        Replace Wagtail's Locale.get_active() with Bedrock's version.

        This ensures that when Wagtail's routing code calls Locale.get_active(),
        it uses our implementation that normalizes language codes from lowercase
        (e.g., 'es-es') to mixed-case (e.g., 'es-ES').

        This fix is necessary because:
        1. Django internally normalizes language codes to lowercase
        2. Wagtail stores Locale records with mixed-case codes (e.g., 'es-ES')
        3. Wagtail's get_supported_content_language_variant() falls back to the
           first matching locale prefix when exact match fails
        4. This causes wrong locales to be matched (e.g., 'es-AR' instead of 'es-ES')

        By normalizing the language code before the database lookup, we ensure
        the correct locale is always found regardless of the order in
        WAGTAIL_CONTENT_LANGUAGES.
        """
        from wagtail.models import Locale

        from bedrock.cms.models.locale import BedrockLocale

        # Replace the classmethod on the base Locale class
        # We need to use the descriptor protocol properly for classmethods
        Locale.get_active = classmethod(BedrockLocale.get_active.__func__)
