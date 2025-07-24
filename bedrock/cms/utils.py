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
from bedrock.cms.models import utility as utility_models  # to avoid circular dep

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

    cms_paths = get_from_cache_wrapped_kv_store(key=BEDROCK_ALL_CMS_PATHS_CACHE_KEY, cast_to=set)

    if cms_paths is None:
        cms_paths = warm_page_path_cache()
    else:
        # The set is turned into a list when put into the DB, but
        # when we pull it out we can't reliably decode it as a set() unless
        # we definitely know it should be one -- which we do in this case.
        cms_paths = set(cms_paths)

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

    set_in_cached_wrapped_kv_store(
        BEDROCK_ALL_CMS_PATHS_CACHE_KEY,
        paths,
    )
    return paths


def _get_from_db_kv_store(key, default=None):
    try:
        return utility_models.SimpleKVStore.objects.get(key=key).value
    except utility_models.SimpleKVStore.DoesNotExist:
        logger.info(f"SimpleKVStore: No key {key} found")
        return default


def _set_in_db_kv_store(key, value):
    try:
        stored = utility_models.SimpleKVStore.objects.get(key=key)
    except utility_models.SimpleKVStore.DoesNotExist:
        logger.info(f"SimpleKVStore: No key {key} found, making new one")
        stored = utility_models.SimpleKVStore(key=key)

    logger.info(f"SimpleKVStore: setting value for {key}")
    stored.value = value
    stored.save()

    return stored


def get_from_cache_wrapped_kv_store(key, default=None):
    """
    Retrieve a value from the hybrid cache. First checks local cache, then falls
    back to DB KV store.

    If found in DB cache, the value is added to local cache for faster subsequent
    access.

    This can be called from any code, because it does not require write access to
    the DB.

    :param key: The cache key to retrieve.
    :param default: Default value to return if the key is not found in either cache.

    :return: The cached value, or the default if the key is not found.
    """
    # Check local cache
    value = cache.get(key)

    if value is not None:
        return value

    # Check DB for the value...
    value = _get_from_db_kv_store(key)
    # ... and if it has a value, pop it into
    # the local cache en route to returning the value
    if value is not None:
        cache.set(
            key,
            value,
            timeout=settings.CACHE_TIME_SHORT,
        )
        return value

    return default


def set_in_cached_wrapped_kv_store(key, value):
    """
    Set a value in the hybrid "cache".

    Writes to both the local cache and the DB KV table.

    IMPORTANT: this should only be called from somewhere with DB-write access -
    i.e. the CMS deployment pod. If it is called from a Web deployment pod, it
    will only set the local-memory cache and also log an exception, because
    there will be unpredictable results if you're trying to cache
    something that should be available across pods -- and if you're not, you
    should just use the regular 'default' local-memory cache directly.

    :param key: The cache key to set.
    :param value: The value to cache.
    """
    # Set in DB first
    try:
        stored = _set_in_db_kv_store(
            key,
            value,
        )
        # Storing may turn a set into a list. We want to stably cache that
        # rather than storing a list in the DB and a set in locmem
        stored.refresh_from_db()
        value = stored.value
    except Exception as ex:
        # Cope with the DB cache not being available
        logger.exception(f"Could not set value in DB-backed cache: {ex}")

    # Set in local cache with a deliberately short timeout
    cache.set(
        key,
        value,
        timeout=settings.CACHE_TIME_SHORT,
    )
