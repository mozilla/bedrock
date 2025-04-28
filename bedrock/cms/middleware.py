# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
from collections import defaultdict
from http import HTTPStatus

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation.trans_real import parse_accept_lang_header

from wagtail.models import Page

from bedrock.base.i18n import normalize_language

logger = logging.getLogger(__name__)


class CMSLocaleFallbackMiddleware:
    """Middleware to seek a viable translation in the CMS of a request that
    404ed, based on the user's Accept-Language headers, ultimately
    trying settings.LANGUAGE_CODE as the last effort

    This has to exist because Wagtail doesn't fail over to the default/any
    other locale if a request to /some-locale/some/path/ 404s
    """

    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == HTTPStatus.NOT_FOUND:
            if self._has_null_byte(request) is True:
                # Don't bother processing URLs with null-byte content - they
                # are fake/vuln scan requests
                return response

            # At this point we have a request that has resulted in a 404,
            # which means it didn't match any Django URLs, and didn't match
            # a CMS page for the current locale+path combination in the URL.

            # Let's see if there is an alternative version available in a
            # different locale that the user would actually like to see.
            # And failing that, if we have it in the default locale, we can
            # fall back to that (which is consistent with what we do with
            # Fluent-based hard-coded pages).

            _path = request.path.lstrip("/")
            lang_prefix, _, sub_path = _path.partition("/")
            # (There will be a language-code prefix, thanks to earlier i18n middleware)

            # Is the requested path available in other languages, checked in
            # order of user preference?
            accept_lang_header = request.headers.get("Accept-Language")

            # We only want the language codes from parse_accept_lang_header,
            # not their weighting, and we want them to be formatted the way
            # we expect them to be

            if accept_lang_header:
                ranked_locales = [normalize_language(x[0]) for x in parse_accept_lang_header(accept_lang_header)]
            else:
                ranked_locales = []

            # Ensure the default locale is also included, as a last-ditch option.
            # NOTE: remove if controversial in terms of user intent but then
            # we'll have to make sure we pass a locale code into the call to
            # url() in templates, so that cms_only_urls.py returns a useful
            # language code

            if settings.LANGUAGE_CODE not in ranked_locales:
                ranked_locales.append(settings.LANGUAGE_CODE)

            _url_path = sub_path.lstrip("/")
            if not _url_path.endswith("/"):
                _url_path += "/"

            # Now try to get hold of all the pages that exist in the CMS for the extracted path
            # that are also in a locale that is acceptable to the user or maybe the fallback locale.

            # We do this by seeking full url_paths that are prefixed with /home/ (for the
            # default locale) or home-<locale_code> - Wagtail sort of 'denorms' the
            # language code into the root of the page tree for each separate locale - eg:
            # * /home/test-path/to/a/page for en-US
            # * /home-fr/test-path/to/a/page for French

            possible_url_path_patterns = []
            for locale_code in ranked_locales:
                if locale_code == settings.LANGUAGE_CODE:
                    root = "/home"
                else:
                    root = f"/home-{locale_code}"

                full_url_path = f"{root}/{_url_path}"
                possible_url_path_patterns.append(full_url_path)

            cms_pages_with_viable_locales = Page.objects.live().filter(
                url_path__in=possible_url_path_patterns,
                # There's no extra value in filtering with locale__language_code__in=ranked_locales
                # due to the locale code being embedded in the url_path strings
            )

            if cms_pages_with_viable_locales:
                # OK, we have some candidate pages with that desired path and at least one
                # viable locale. Let's try to send the user to their most preferred one.

                # Evaluate the queryset just once, then explore the results in memory
                lookup = defaultdict(list)
                for page in cms_pages_with_viable_locales:
                    lookup[page.locale.language_code].append(page)

                for locale_code in ranked_locales:
                    if locale_code in lookup:
                        page_list = lookup[locale_code]
                        # There _should_ only be one matching for this locale, but let's not assume
                        if len(page_list) > 1:
                            logger.warning(f"CMS 404-fallback problem - multiple pages with same path found: {page_list}")
                        page = page_list[0]  # page_list should be a list of 1 item
                        return HttpResponseRedirect(page.url)

                # Note: we can make this more efficient by leveraging the cached page tree
                # (once the work to pre-cache the page tree lands)

        return response

    def _has_null_byte(self, request):
        if "\x00" in request.path:
            logger.warning("Null byte found in request path: %s", request.path)
            # This gets called as a 404, so let's just treat it as Not Found
            return True
        return False
