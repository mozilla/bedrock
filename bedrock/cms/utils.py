# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Subquery
from django.http import Http404

from wagtail.contrib.redirects.models import Redirect
from wagtail.models import Locale, Page

from bedrock.base.i18n import split_path_and_normalize_language

logger = logging.getLogger(__name__)

BEDROCK_ALL_CMS_PATHS_CACHE_KEY = "bedrock_cms_all_known_live_page_paths"


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


def get_locales_for_cms_page(page):
    # Patch in a list of CMS-available locales for pages that are
    # translations, not just aliases

    locales_available_via_cms = [page.locale.language_code]
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
        locales_available_via_cms += [x.locale.language_code for x in _actual_translations]
    except ValueError:
        # when there's no draft and no potential for aliases, etc, the above lookup will fail
        pass

    return locales_available_via_cms


def get_cms_locales_for_path(request):
    locales = []

    if page := get_page_for_request(request=request):
        locales = get_locales_for_cms_page(page=page)

    return locales


def _get_all_cms_paths() -> set:
    """Fetch all the possible URL paths that are available
    in Wagtail, in all locales, for LIVE pages only and for
    all Redirects
    """
    pages = set([x.url for x in Page.objects.live() if x.url is not None])
    redirects = set([x.old_path for x in Redirect.objects.all()])

    return pages.union(redirects)


def path_exists_in_cms(path: str) -> bool:
    """
    Using the paths cached via warm_page_path_cache, return a boolean
    simply showing whether or not Wagtail can serve the requested path
    (whether as a Page or as a Redirect).

    Avoiding Wagtail-raised 404s is the goal of this function.
    We don't care if there'll be a chain of redirects or a slash being
    auto-appended - we'll let Django/Wagtail handle that.
    """

    cms_paths = cache.get(BEDROCK_ALL_CMS_PATHS_CACHE_KEY)
    if cms_paths is None:
        cms_paths = warm_page_path_cache()
    if "?" in path:
        path = path.partition("?")[0]

    if path in cms_paths:
        return True
    elif not path.endswith("/") and f"{path}/" in cms_paths:
        # pages have trailing slashes in their paths, but we might get asked for one without it
        return True
    elif path.endswith("/") and path[:-1] in cms_paths:
        # redirects have no trailing slashes in their paths, but we might get asked for one with it
        return True
    return False


def warm_page_path_cache() -> set:
    paths = _get_all_cms_paths()
    logger.info(f"Warming the cache '{BEDROCK_ALL_CMS_PATHS_CACHE_KEY}' with {len(paths)} paths ")

    cache.set(
        BEDROCK_ALL_CMS_PATHS_CACHE_KEY,
        paths,
        settings.CACHE_TIME_LONG,
    )
    return paths
