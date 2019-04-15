from __future__ import absolute_import
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from operator import attrgetter
from django.http import Http404

from lib import l10n_utils
import bleach

from .grants_db import GRANTS

grant_labels = {
    '': 'All',
    'open-source-technology': 'Open Source Technology',
    'learning-webmaking': 'Learning & Webmaking',
    'user-sovereignty': 'User Sovereignty',
    'free-culture-community': 'Free Culture & Community'
}


def grant_info(request, slug):
    grant_data = [k for k in GRANTS if k.url == slug]

    if not grant_data:
        raise Http404

    return l10n_utils.render(request, "grants/info.html", {
        'grant': grant_data[0],
        'grant_labels': grant_labels
    })


def grants(request):
    type_filter = bleach.clean(request.GET.get('type', ''))

    if type_filter and type_filter not in grant_labels:
        raise Http404

    if type_filter:
        grants = [k for k in GRANTS if k.type == type_filter]
    else:
        grants = GRANTS

    grants.sort(key=attrgetter('grantee'))

    return l10n_utils.render(request, "grants/index.html", {
            'filter': type_filter,
            'grants': grants,
            'grant_labels': grant_labels
    })
