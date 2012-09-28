import l10n_utils
from django.conf import settings

def firefoxos(request):
    return l10n_utils.render(request, "firefoxos/firefoxos.html")
    
def b2g(request):
    return l10n_utils.render(request, "firefoxos/firefoxos.html")

def about(request):
    return l10n_utils.render(request, "firefoxos/firefoxos.html")

def faq(request):
    return l10n_utils.render(request, "firefoxos/firefoxos.html")

