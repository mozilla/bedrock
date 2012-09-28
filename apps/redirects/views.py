import l10n_utils

def b2g(request):
    return l10n_utils.render(request, "firefoxos/firefoxos.html")
