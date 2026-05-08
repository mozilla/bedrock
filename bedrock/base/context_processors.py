# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

from bedrock.base.geo import get_country_from_request
from lib.l10n_utils import translation


def geo(request):
    return {"country_code": get_country_from_request(request)}


def i18n(request):
    url_locale = translation.get_language()
    lang = dict(settings.LANGUAGE_URL_MAP).get(url_locale) or url_locale
    # Normally, CANONICAL_LANG == LANG, but sometimes, a user requests a page
    # that does not exist, but the locale has a fallback locale, so the user is
    # served the content from the fallback locale at the requested URL (for
    # example, the user requests /pt-PT/somepage, which does not exist, so the
    # user gets /pt-BR/somepage content at the /pt-PT/somepage/ URL). In this
    # case, pt-PT is the LANG, and pt-BR is the CANONICAL_LANG.
    content_locale = getattr(request, "content_locale", None)
    return {
        "LANGUAGES": settings.LANGUAGES,
        "LANG": lang,
        "CANONICAL_LANG": content_locale or lang,
        "DIR": "rtl" if translation.get_language_bidi() else "ltr",
    }


def globals(request):
    return {
        "request": request,
        "settings": settings,
    }
