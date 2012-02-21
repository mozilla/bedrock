import l10n_utils
from django.conf import settings

def marketplace(request):
    return l10n_utils.render(request, "marketplace/marketplace.html")
