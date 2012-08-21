from django.http import Http404

import l10n_utils
import bleach

from grants_db import GRANTS

grant_labels = {
    'open-source-technology': 'Open Source Technology',
    'learning-webmaking': 'Learning & Webmaking',
    'user-sovereignty': 'User Sovereignty',
    'free-culture-community': 'Free Culture & Community'
}


def grant_info(request, slug):
    grant_data = GRANTS[slug]

    if not grant_data:
        raise Http404

    return l10n_utils.render(request, "grants/info.html", {
        'grant': grant_data,  # Using named tuple so need to deep dive
        'grant_labels': grant_labels
    })


def grants(request):
    type_filter = bleach.clean(request.GET.get('type', ''))

    if type_filter and type_filter not in grant_labels:
        raise Http404

    if type_filter:
        grants = dict((k, v) for k, v in GRANTS.items() if type_filter in v['type'])
    else:
        grants = GRANTS

    return l10n_utils.render(request, "grants/index.html", {
            'filter': type_filter,
            'grants': grants,
            'grant_labels': grant_labels
    })
