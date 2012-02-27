import l10n_utils
from django.conf import settings

def collusion(request):
    return l10n_utils.render(request, "collusion/collusion.html")

def demo(request):
    return l10n_utils.render(request, "collusion/demo.html")
