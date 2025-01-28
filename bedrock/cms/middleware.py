# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import logging
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
            extracted_lang, _, _path = path_.partition("/")

            # Is the requested path available in other languages, checked in
            # order of user preference?
            accept_lang_header = request.headers.get("Accept-Language")

            # We only want the language codes from parse_accept_lang_header,
            # not their weighting, and we want them to be formatted the way
            # we expect them to be
            ranked_locales = [normalize_language(x[0]) for x in parse_accept_lang_header(accept_lang_header)]

            # Ensure the default locale is also included, as a last-ditch option.
            # NOTE: remove if controversial in terms of user intent but then
            # we'll have to make sure we pass a locale code into the call to
            # url() in templates, so that cms_only_urls.py returns a useful
            # language code

            if settings.LANGUAGE_CODE not in ranked_locales:
                ranked_locales.append(settings.LANGUAGE_CODE)

            _url_path = f"{_path}"
            if not _url_path.endswith("/"):
                _url_path += "/"

            # Now try to get hold of all the pages that exist in the CMS for the extracted path
            cms_pages = Page.objects.filter(url_path__endswith=_url_path)

            if cms_pages:
                # OK, we have some candidate pages that desired path
                # locales. Let's try to send the user to their most preferred one.

                # Note: This is not optimal right now, but we can make it one-DB-hit
                # once the work to pre-cache the page tree lands
                for locale_code in ranked_locales:
                    qs = cms_pages.filter(locale__language_code=locale_code)
                    if qs.exists():
                        # There _should_ only be one matching for this locale
                        if qs.count() > 1:
                            logger.warning(f"CMS 404-fallback problem: multiple pages with same path found {qs}")
                        return HttpResponseRedirect(qs.first().url)

                # Fallback: send the user to the first one
                return HttpResponseRedirect(cms_pages.first().url)

        return response
