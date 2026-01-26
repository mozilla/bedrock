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
        # Replace Wagtail's formfield_for_dbfield with our SVG-sanitizing version
        self._patch_image_form_field()

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

    @staticmethod
    def _patch_image_form_field():
        """
        Replace Wagtail's formfield_for_dbfield with our version that uses
        SanitizingWagtailImageField for SVG sanitization.

        This ensures that all image upload forms use our custom field which
        sanitizes SVG files and rejects them if they contain potentially
        dangerous content like scripts or event handlers.

        This is similar to the _patch_locale_get_active approach - we replace
        a Wagtail function with our enhanced version at app startup.
        """

        from django.utils.text import capfirst
        from django.utils.translation import gettext as _

        import wagtail.images.forms
        from wagtail.admin.forms.collections import CollectionChoiceField
        from wagtail.models import Collection

        from bedrock.cms.fields import SanitizingWagtailImageField

        def formfield_for_dbfield(db_field, **kwargs):
            """
            Custom formfield callback for image forms with SVG sanitization.

            This replaces Wagtail's default formfield_for_dbfield to use our
            SanitizingWagtailImageField instead of WagtailImageField.
            """
            if db_field.name == "file":
                return SanitizingWagtailImageField(
                    label=capfirst(db_field.verbose_name),
                    **kwargs,
                )
            elif db_field.name == "collection":
                return CollectionChoiceField(
                    label=_("Collection"),
                    queryset=Collection.objects.all(),
                    empty_label=None,
                    **kwargs,
                )

            # For all other fields, use default
            return db_field.formfield(**kwargs)

        # Replace Wagtail's function with ours
        wagtail.images.forms.formfield_for_dbfield = formfield_for_dbfield
