# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
from datetime import datetime

from django.conf import settings

# match 1 - 4 digits only
FC_RE = re.compile(r"^\d{1,4}$")


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


def contrib_numbers(request):
    return settings.CONTRIBUTE_NUMBERS
