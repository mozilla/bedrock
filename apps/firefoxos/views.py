import l10n_utils
from django.conf import settings

def b2g(request):
    return l10n_utils.render(request, "firefoxos/firefoxos.html")

def about(request):
    return l10n_utils.render(request, "firefoxos/about.html")

def faq(request):
    return l10n_utils.render(request, "firefoxos/faq.html")

