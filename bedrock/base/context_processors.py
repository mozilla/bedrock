# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

from bedrock.base.geo import get_country_from_request
from lib.l10n_utils import translation


def geo(request):
    return {"country_code": get_country_from_request(request)}


def i18n(request):
    return {
        "LANGUAGES": settings.LANGUAGES,
        "LANG": (dict(settings.LANGUAGE_URL_MAP).get(translation.get_language()) or translation.get_language()),
        "DIR": "rtl" if translation.get_language_bidi() else "ltr",
    }


def globals(request):
    return {
        "request": request,
        "settings": settings,
    }
