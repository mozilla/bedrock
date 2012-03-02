from django.conf.urls.defaults import *
from views import contribute, channel, firefoxPerformance, firefoxSecurity, button, new, sandstone, geolocation

urlpatterns = patterns('',
    (r'^button/', button),
    (r'^channel/', channel),
    (r'^contribute/', contribute),
    (r'^new/', new),
    (r'^sandstone/', sandstone),

    (r'^firefox/geolocation/', geolocation),
    (r'^firefox/security/', firefoxSecurity),
    (r'^firefox/performance/', firefoxPerformance),
)
