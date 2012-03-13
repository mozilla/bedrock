import l10n_utils
from django.conf import settings
from product_details import product_details
from session_csrf import anonymous_csrf

import basket

from mozorg.forms import NewsletterForm

@anonymous_csrf

def index(request):
    return l10n_utils.render(request, "mozorg/index.html")

def home(request):
    success = False
    form = NewsletterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            basket.subscribe(data['email'], 'app-dev', format=data['fmt'])
            success = True
            
    return l10n_utils.render(request,
                             "mozorg/home.html",
                             {'form': form,
                              'success': success})

def contribute(request):
    return l10n_utils.render(request, "mozorg/contribute.html")

def firefox_customize(request):
    return l10n_utils.render(request, "mozorg/firefox/customize.html")

def firefox_features(request):
    return l10n_utils.render(request, "mozorg/firefox/features.html")

def firefox_happy(request):
    return l10n_utils.render(request, "mozorg/firefox/happy.html")

def firefox_technology(request):
    return l10n_utils.render(request, "mozorg/firefox/technology.html")

def firefox_security(request):
    return l10n_utils.render(request, "mozorg/firefox/security.html")

def firefox_speed(request):
    return l10n_utils.render(request, "mozorg/firefox/speed.html", {'latest_version': product_details.firefox_versions['LATEST_FIREFOX_DEVEL_VERSION']})

def firefox_performance(request):
    return l10n_utils.render(request, "mozorg/firefox/performance.html")

def channel(request):
    data = {}

    if 'mobile_first' in request.GET:
        data['mobile_first'] = True

    return l10n_utils.render(request, "mozorg/channel.html", data)

def button(request):
    return l10n_utils.render(request, "mozorg/button.html")

def new(request):
    return l10n_utils.render(request, "mozorg/new.html")

def sandstone(request):
    return l10n_utils.render(request, "mozorg/sandstone.html")

def geolocation(request):
    return l10n_utils.render(request, "mozorg/geolocation.html", 
                             {'gmap_api_key': settings.GMAP_API_KEY})
