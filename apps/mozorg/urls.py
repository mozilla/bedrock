from django.conf.urls.defaults import *
from views import contribute, channel, firefox_performance, firefox_features, firefox_customize, firefox_security, firefox_technology, button, new, sandstone, geolocation


urlpatterns = patterns('',
    (r'^button/', button),
    (r'^channel/', channel),
    (r'^contribute/', contribute),
    (r'^new/', new),
    (r'^sandstone/', sandstone),

    (r'^firefox/geolocation/', geolocation),
    url(r'^firefox/features/', firefox_features, name='mozorg.firefox_features'),
    url(r'^firefox/customize/', firefox_customize, name='mozorg.firefox_customize'),
    url(r'^firefox/security/', firefox_security, name='mozorg.firefox_security'),
    url(r'^firefox/technology/', firefox_technology, name='mozorg.firefox_technology'),
    url(r'^firefox/performance/', firefox_performance, name='mozorg.firefox_performance'),
)
