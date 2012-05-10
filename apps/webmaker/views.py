import l10n_utils
from django.conf import settings


def webmaker(request):
    return l10n_utils.render(request, "webmaker/index.html")

