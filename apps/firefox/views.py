import l10n_utils
from django.conf import settings
from product_details import product_details
from session_csrf import anonymous_csrf

import basket

from mozorg.forms import NewsletterForm

@anonymous_csrf

def central(request):
    return l10n_utils.render(request, "firefox/central.html")

def customize(request):
    return l10n_utils.render(request, "firefox/customize.html")

def features(request):
    return l10n_utils.render(request, "firefox/features.html")

def geolocation(request):
    return l10n_utils.render(request, "firefox/geolocation.html", 
                             {'gmap_api_key': settings.GMAP_API_KEY})

def happy(request):
    return l10n_utils.render(request, "firefox/happy.html")

def new(request):
    return l10n_utils.render(request, "firefox/new.html")

def organizations(request):
    return l10n_utils.render(request, "firefox/organizations/organizations.html")

def organizations_faq(request):
    return l10n_utils.render(request, "firefox/organizations/faq.html")

def performance(request):
    return l10n_utils.render(request, "firefox/performance.html")

def security(request):
    return l10n_utils.render(request, "firefox/security.html")

def speed(request):
    return l10n_utils.render(request, "firefox/speed.html", {'latest_version': product_details.versions['LATEST_FIREFOX_DEVEL_VERSION']})

def technology(request):
    return l10n_utils.render(request, "firefox/technology.html")

def update(request):
    return l10n_utils.render(request, "firefox/update.html")
