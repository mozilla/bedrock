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
    trying settings.LANGAUGE_CODE as the last effort

    This has to exist because Wagtail doesn't fail over to the default/any
    other locale if a request to /some-locale/some/path/ 404s
    """

    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == HTTPStatus.NOT_FOUND:
            # At this point we have a request that has resulted in a 404,
            # which means it didn't match any Django URLs, and didn't match
            # a CMS page for the current locale+path combination in the URL.

            # Let's see if there is an alternative version available in a
            # different locale that the user would actually like to see.
            # And failing that, if we have it in the default locale, we can
            # fall back to that (which is consistent with what we do with
            # Fluent-based hard-coded pages).

            path_ = request.path.lstrip("/")
            extracted_lang, _, _sub_path = path_.partition("/")

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

            # Make sure the locale-less _url_path we're trying to match starts
            # with / to avoid partial matches
            _url_path = f"/{_sub_path.lstrip('/')}"
            if not _url_path.endswith("/"):
                _url_path += "/"

            # Now try to get hold of all the pages that exist in the CMS for the extracted path
            # that are also in a locale that is acceptable to the user + maybe the fallback locale
            cms_pages_with_viable_locales = Page.objects.filter(
                url_path__endswith=_url_path,
                locale__language_code__in=ranked_locales,
            )

            if cms_pages_with_viable_locales:
                # OK, we have some candidate pages with that desired path and at least one of
                # viable locale. Let's try to send the user to their most preferred one.

                # Evaluate the queryset once and explore the results in memory
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

                # Fallback: send the user to the first one
                return HttpResponseRedirect(cms_pages_with_viable_locales.first().url)

        return response
