from operator import attrgetter
from django.http import Http404

import l10n_utils
import bleach

from grants_db import GRANTS

grant_labels = {
    '': 'All',
    'open-source-technology': 'Open Source Technology',
    'learning-webmaking': 'Learning & Webmaking',
    'user-sovereignty': 'User Sovereignty',
    'free-culture-community': 'Free Culture & Community'
}


def grant_info(request, slug):
    grant_data = filter(lambda k: k.url == slug, GRANTS)

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
        grants = filter(lambda k: k.type == type_filter, GRANTS)
    else:
        grants = GRANTS

    # first sort by title (alphabetically)
    sorted_grantees = sorted(grants, key=attrgetter('grantee'))
    # now sort by year (reverse numeric)
    sorted_grants = sorted(sorted_grantees, key=attrgetter('year'), reverse=True)

    return l10n_utils.render(request, "grants/index.html", {
            'filter': type_filter,
            'grants': sorted_grants,
            'grant_labels': grant_labels
    })
