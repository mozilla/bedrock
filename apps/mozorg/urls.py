from django.conf.urls.defaults import *
from views import home, contribute, channel, firefox_performance, firefox_features, firefox_customize, firefox_happy, firefox_security, firefox_speed, firefox_technology, button, new, sandstone, geolocation


urlpatterns = patterns('',
    url(r'^home/', home, name='mozorg.home'),

    (r'^button/', button),
    (r'^channel/', channel),
    (r'^new/', new),
    (r'^sandstone/', sandstone),
    url(r'^contribute/', contribute, name='mozorg.contribute'),

    (r'^firefox/geolocation/', geolocation),
    url(r'^firefox/customize/', firefox_customize, name='mozorg.firefox_customize'),
    url(r'^firefox/features/', firefox_features, name='mozorg.firefox_features'),
    url(r'^firefox/happy/', firefox_happy, name='mozorg.firefox_happy'),
    url(r'^firefox/performance/', firefox_performance, name='mozorg.firefox_performance'),
    url(r'^firefox/security/', firefox_security, name='mozorg.firefox_security'),
    url(r'^firefox/speed/', firefox_speed, name='mozorg.firefox_speed'),
    url(r'^firefox/technology/', firefox_technology, name='mozorg.firefox_technology'),
)
