# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from builtins import str
import re
from datetime import datetime

from django.conf import settings
from django.urls import reverse

from bedrock.mozorg.util import get_fb_like_locale
from lib.l10n_utils import get_locale


# match 1 - 4 digits only
FC_RE = re.compile(r'^\d{1,4}$')


def canonical_path(request):
    """
    The canonical path can be overridden with a template variable like
    l10n_utils.render(request, template_name, {'canonical_path': '/firefox/'})
    """
    lang = getattr(request, 'locale', settings.LANGUAGE_CODE)
    url = getattr(request, 'path', '/')
    return {'canonical_path': re.sub(r'^/' + lang, '', url)}


def current_year(request):
    return {"current_year": datetime.today().year}


def funnelcake_param(request):
    """If a query param for a funnelcake is sent, add it to the context."""
    fc_id = request.GET.get('f', None)
    context = {}

    if fc_id and FC_RE.match(fc_id):
        # special case for installer-help page
        # bug 933852
        installer_help_url = reverse('firefox.installer-help')
        if installer_help_url in request.path_info:
            fc_id = str(int(fc_id) + 1)
        context['funnelcake_id'] = fc_id

    return context


def facebook_locale(request):
    return {'facebook_locale': get_fb_like_locale(get_locale(request))}


def contrib_numbers(request):
    return settings.CONTRIBUTE_NUMBERS
