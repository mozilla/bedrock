import l10n_utils
from django.conf import settings

def research(request):
    return l10n_utils.render(request, "research/research.html")

