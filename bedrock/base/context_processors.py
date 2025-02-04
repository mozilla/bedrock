# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
from datetime import datetime

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


def canonical_path(request):
    """
    The canonical path can be overridden with a template variable like
    l10n_utils.render(request, template_name, {'canonical_path': '/firefox/'})
    """
    lang = getattr(request, "locale", settings.LANGUAGE_CODE)
    url = getattr(request, "path", "/")
    return {"canonical_path": re.sub(r"^/" + lang, "", url) if lang else url}


def current_year(request):
    return {"current_year": datetime.today().year}
