import l10n_utils

def devices(request):
    return l10n_utils.render(request, "landing/devices.html")
