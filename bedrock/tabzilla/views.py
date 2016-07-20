# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path
from datetime import datetime

from django.conf import settings
from django.http import HttpResponseRedirect
from django.template import loader
from django.views.decorators.http import last_modified

from lib import l10n_utils

from bedrock.mozorg.decorators import cache_control_expires


def template_last_modified(template):
    def inner_last_modified(request):
        locale = l10n_utils.get_locale(request)

        tmpl_file = loader.get_template(template).template.filename
        template_time = os.path.getmtime(tmpl_file)

        try:
            lang_file = 'tabzilla/tabzilla'
            rel_path = os.path.join('locale', locale, '%s.lang' % lang_file)
            abs_path = os.path.join(settings.ROOT, rel_path)
            lang_time = os.path.getmtime(abs_path)
        except OSError:
            lang_time = 0

        return datetime.fromtimestamp(max(template_time, lang_time))

    return inner_last_modified


def _resp(request, path, ctype, context=None):
    resp = l10n_utils.render(request, path, context, content_type=ctype)

    is_enabled = not settings.TEMPLATE_DEBUG and settings.CDN_BASE_URL
    if is_enabled and isinstance(resp, HttpResponseRedirect):
        # CDN URL should be protocol relative, but that won't work
        # in a Location header.
        protocol = 'https:' if request.is_secure() else 'http:'
        cdn_base = protocol + settings.CDN_BASE_URL
        resp['location'] = cdn_base + resp['location']
    return resp


@cache_control_expires(12)
@last_modified(template_last_modified('tabzilla/tabzilla.js'))
def tabzilla_js(request):
    return _resp(request, 'tabzilla/tabzilla.js', 'text/javascript')


@cache_control_expires(12)
@last_modified(template_last_modified('tabzilla/transbar.jsonp'))
def transbar_jsonp(request):
    resp = _resp(request, 'tabzilla/transbar.jsonp', 'application/javascript')
    resp['Access-Control-Allow-Origin'] = '*'
    return resp
