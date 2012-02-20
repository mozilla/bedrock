from django.conf.urls.defaults import *
from views import contribute, channel, button, new, persona, styleguide, geolocation

urlpatterns = patterns('',
    (r'^button/', button),
    (r'^channel/', channel),
    (r'^contribute/', contribute),
    (r'^new/', new),
    (r'^persona/', persona),
    (r'^styleguide/', styleguide),

    (r'^firefox/geolocation/', geolocation)
)
