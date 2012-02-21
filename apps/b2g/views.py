import l10n_utils
from django.conf import settings

def b2g(request):
    return l10n_utils.render(request, "b2g/b2g.html")

def about(request):
    return l10n_utils.render(request, "b2g/about.html")

def developerfaq(request):
    return l10n_utils.render(request, "b2g/faq.html")

