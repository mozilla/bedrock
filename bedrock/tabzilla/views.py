# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lib import l10n_utils

from bedrock.mozorg.decorators import cache_control_expires


@cache_control_expires(12)
def tabzilla_js(request):
    return l10n_utils.render(request, 'tabzilla/tabzilla.js',
                             content_type='text/javascript')
