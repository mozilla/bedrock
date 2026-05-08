# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Subquery
from django.http import Http404

from wagtail.models import Locale, Page, Site

from bedrock.base.i18n import split_path_and_normalize_language

logger = logging.getLogger(__name__)


def get_page_for_request(*, request):
    """For the given HTTPRequest (and its path) find the corresponding Wagtail
    page, if one exists"""

    lang_code, path, _ = split_path_and_normalize_language(request.path)
    try:
        locale = Locale.objects.get(language_code=lang_code)
    except Locale.DoesNotExist:
        locale = None

    try:
        page = Page.find_for_request(request=request, path=path)
        if page and locale and locale != page.locale:
            page = page.get_translation(locale=locale)

    except (ObjectDoesNotExist, Http404):
        page = None

    return page


def find_fallback_page_for_locale(locale_code, url_path):
    """
    For an alias locale (e.g. 'pt-PT'), find the corresponding live page
    in the fallback locale's page tree (e.g. 'pt-BR').
    url_path is the bare path without locale prefix (normalized internally).
    Returns a Page instance or None.
    """
    fallback_locale_code = getattr(settings, "FALLBACK_LOCALES", {}).get(locale_code)
    if not fallback_locale_code:
        return None

    try:
        fallback_locale = Locale.objects.get(language_code=fallback_locale_code)
    except Locale.DoesNotExist:
        return None

    site = Site.objects.filter(is_default_site=True).select_related("root_page").first()
    if not site:
        return None
    try:
        locale_root = site.root_page.get_translation(fallback_locale)
    except Page.DoesNotExist:
        logger.exception("No root page translation found for fallback locale %r", fallback_locale_code)
        return None

    _url_path = url_path.strip("/")
    if not _url_path:
        return locale_root if locale_root.live else None
    full_url_path = f"{locale_root.url_path}{_url_path}/"

    return Page.objects.live().filter(url_path=full_url_path).first()


def compute_cms_page_locales(page):
    """
    Return a tuple of locales: (all_locales, content_locales) for a CMS page.

    all_locales: content_locales + alias locales from FALLBACK_LOCALES.
    content_locales: locales with real translated content (no alias expansion).
    """
    content_locales = [page.locale.language_code]
    try:
        _actual_translations = (
            page.get_translations()
            .live()
            .exclude(
                id__in=Subquery(
                    page.aliases.all().values_list("id", flat=True),
                )
            )
        )
        content_locales += [x.locale.language_code for x in _actual_translations]
    except ValueError:
        # when there's no draft and no potential for aliases, etc, the above lookup will fail
        pass

    # Expand with alias locales from FALLBACK_LOCALES reverse map.
    # e.g. if pt-BR is in the list, also add pt-PT.
    alias_additions = [alias for alias, target in getattr(settings, "FALLBACK_LOCALES", {}).items() if target in content_locales]

    all_locales = list(dict.fromkeys(content_locales + alias_additions))
    deduped_content = list(dict.fromkeys(content_locales))

    return all_locales, deduped_content


def get_locales_for_cms_page(page):
    # Patch in a list of CMS-available locales for pages that are
    # translations, not just aliases
    all_locales, _ = compute_cms_page_locales(page)
    return all_locales


def get_cms_locales_for_path(request):
    locales = []

    if page := get_page_for_request(request=request):
        locales = get_locales_for_cms_page(page=page)

    return locales
