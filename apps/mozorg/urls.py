from django.conf.urls.defaults import *
from views import contribute, channel, firefox_performance, firefox_security, button, new, sandstone, geolocation


urlpatterns = patterns('',
    (r'^button/', button),
    (r'^channel/', channel),
    (r'^contribute/', contribute),
    (r'^new/', new),
    (r'^sandstone/', sandstone),

    (r'^firefox/geolocation/', geolocation),
    url(r'^firefox/security/', firefox_security, name='mozorg.firefox_security'),
    url(r'^firefox/performance/', firefox_performance, name='mozorg.firefox_performance'),
)
