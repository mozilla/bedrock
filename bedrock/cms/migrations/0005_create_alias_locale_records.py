# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys

from django.db import migrations

from bedrock.base.config_manager import config


def create_alias_locales(apps, schema_editor):
    # Skip in test environments — test fixtures create the locale records they need.
    if "pytest" in sys.modules or config("SQLITE_EXPORT_MODE", parser=bool, default="false"):
        return

    from wagtail.models import Locale, Page, Site

    alias_locales = ["es-CL", "pt-PT", "en-GB", "en-CA"]

    site = Site.objects.filter(is_default_site=True).select_related("root_page").first()
    if not site:
        return

    # The locale root pages live at depth 2 (children of the Wagtail tree
    # root at depth 1).  Note: site.root_page is the *homepage* (depth 3),
    # not the locale root — using it would place new pages one level too deep.
    en_us_locale_root = Page.objects.filter(
        depth=2,
        locale__language_code="en-US",
    ).first()
    if not en_us_locale_root:
        return
    wagtail_root = en_us_locale_root.get_parent()

    for code in alias_locales:
        locale, _ = Locale.objects.get_or_create(language_code=code)

        if en_us_locale_root.get_translation_or_none(locale) is not None:
            continue

        # Create a non-live locale root page for the alias locale at depth 2,
        # alongside the other locale roots (de, fr, es-ES, etc.).
        #
        # We use copy() rather than copy_for_translation() because the Wagtail
        # tree root (depth 1) has no per-locale translations, which causes
        # copy_for_translation()'s parent-translation check to fail.
        #
        # keep_live=False ensures Wagtail won't serve this page at
        # /<alias-locale>/ — the fallback machinery
        # (wagtail_serve_with_locale_fallback + find_fallback_page_for_locale)
        # handles those requests and serves the canonical locale's content.
        # The root page is a structural record; the fallback machinery
        # does not require it to exist.
        en_us_locale_root.copy(
            to=wagtail_root,
            update_attrs={
                "locale": locale,
                "slug": f"home-{code}",
            },
            copy_revisions=False,
            keep_live=False,
            reset_translation_key=False,
            log_action=None,
        )


def remove_alias_locales(apps, schema_editor):
    if "pytest" in sys.modules or config("SQLITE_EXPORT_MODE", parser=bool, default="false"):
        return

    from wagtail.models import Locale, Page

    alias_locales = ["es-CL", "pt-PT", "en-GB", "en-CA"]

    en_us_locale_root = Page.objects.filter(
        depth=2,
        locale__language_code="en-US",
    ).first()
    if not en_us_locale_root:
        return

    for code in alias_locales:
        locale = Locale.objects.filter(language_code=code).first()
        if not locale:
            continue

        # Delete the locale root page only if it has no child pages
        # (i.e. the alias locale was never promoted to a full locale with its own content).
        alias_root = en_us_locale_root.get_translation_or_none(locale)
        if alias_root is not None and not alias_root.get_children().exists():
            alias_root.delete()

        # Delete the Locale record if no pages remain under it.
        if not Page.objects.filter(locale=locale).exists():
            locale.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0004_bedrocklocale"),
    ]

    operations = [
        migrations.RunPython(create_alias_locales, remove_alias_locales),
    ]
