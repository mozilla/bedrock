# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.http import HttpResponseRedirect

from lib import l10n_utils

from bedrock.mozorg.decorators import cache_control_expires


@cache_control_expires(12)
def tabzilla_js(request):
    resp = l10n_utils.render(request, 'tabzilla/tabzilla.js',
                             content_type='text/javascript')

    is_enabled = not settings.TEMPLATE_DEBUG and settings.CDN_BASE_URL
    if is_enabled and isinstance(resp, HttpResponseRedirect):
        # CDN URL should be protocol relative, but that won't work
        # in a Location header.
        protocol = 'https:' if request.is_secure() else 'http:'
        cdn_base = protocol + settings.CDN_BASE_URL
        resp['location'] = cdn_base + resp['location']
    return resp
