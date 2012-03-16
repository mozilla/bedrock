import l10n_utils
from product_details import product_details

def devices(request):
    return l10n_utils.render(request, "landing/devices.html", {'latest_version': product_details.firefox_versions['LATEST_FIREFOX_VERSION']} )
