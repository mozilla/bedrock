# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os.path
from datetime import datetime

from django.conf import settings
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


@cache_control_expires(12)
@last_modified(template_last_modified('infobar/infobar.jsonp'))
def infobar_jsonp(request):
    resp = l10n_utils.render(request, 'infobar/infobar.jsonp',
        content_type='application/javascript')
    resp['Access-Control-Allow-Origin'] = '*'
    return resp
