from django.conf.urls.defaults import *
from views import channel, button, new, geolocation

urlpatterns = patterns('',
    (r'^button/', button),
    (r'^channel/', channel),
    (r'^new/', new),

    (r'^firefox/geolocation/', geolocation)
)
