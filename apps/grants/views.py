from django.http import Http404

import l10n_utils

from grants_db import GRANTS

GRANT_LABELS = {
    'open-source-technology': 'Open Source Technology',
    'learning-webmaking': 'Learning & Webmaking',
    'user-sovereignty': 'User Sovereignty',
    'free-culture-community': 'Free Culture & Community'
}


def grant_info(request, slug):

    grant_data = filter(lambda x: x[0] == slug, GRANTS)

    if not grant_data:
        raise Http404

    return l10n_utils.render(request, "grants/info.html", {
        'grant': grant_data[0][1],  # Using named tuple so need to deep dive
        'grant_labels': GRANT_LABELS
    })


def grants(request):

    type_filter = request.GET.get('type', '')

    if type_filter:
        grants = filter(lambda x: x[1]['type'] == type_filter, GRANTS)
    else:
        grants = GRANTS

    return l10n_utils.render(request, "grants/index.html", {
            'grants': grants,
            'grant_labels': GRANT_LABELS
    })
