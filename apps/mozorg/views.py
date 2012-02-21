import l10n_utils
from django.conf import settings

def index(request):
    return l10n_utils.render(request, "mozorg/index.html")

def contribute(request):
    return l10n_utils.render(request, "mozorg/contribute.html")

def channel(request):
    data = {}

    if 'mobile_first' in request.GET:
        data['mobile_first'] = True

    return l10n_utils.render(request, "mozorg/channel.html", data)

def button(request):
    return l10n_utils.render(request, "mozorg/button.html")

def new(request):
    return l10n_utils.render(request, "mozorg/new.html")

def styleguide(request):
    return l10n_utils.render(request, "mozorg/styleguide.html")

def geolocation(request):
    return l10n_utils.render(request, "mozorg/geolocation.html", 
                             {'gmap_api_key': settings.GMAP_API_KEY})
