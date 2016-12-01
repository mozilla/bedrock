# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lib import l10n_utils


def foundation_index(request):
    locale = l10n_utils.get_locale(request)
    version = request.GET.get('v', None)

    if (locale != 'en-US' or version != 'b'):
        version = None

    return l10n_utils.render(request, 'foundation/index.html', {'version': version})
