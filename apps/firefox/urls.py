from django.conf.urls.defaults import *
from views import performance, features, customize, happy, new, organizations, organizations_faq, security, speed, technology, geolocation, update


urlpatterns = patterns('',
    url(r'^firefox/customize/$', customize, name='firefox.customize'),
    url(r'^firefox/features/$', features, name='firefox.features'),
    url(r'^firefox/geolocation/$', geolocation, name='firefox.geolocation'),
    url(r'^firefox/happy/$', happy, name='firefox.happy'),
    url(r'^firefox/new/$', new, name='firefox.new'),
    url(r'^firefox/organizations/faq/$', organizations_faq, name='firefox.organizations_faq'),
    url(r'^firefox/organizations/$', organizations, name='firefox.organizations'),
    url(r'^firefox/performance/$', performance, name='firefox.performance'),
    url(r'^firefox/security/$', security, name='firefox.security'),
    url(r'^firefox/speed/$', speed, name='firefox.speed'),
    url(r'^firefox/technology/$', technology, name='firefox.technology'),
    url(r'^firefox/update/$', update, name='firefox.update'),
)
