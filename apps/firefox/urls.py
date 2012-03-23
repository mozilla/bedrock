from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^firefox/central/$', views.central, name='firefox.central'),
    url(r'^firefox/customize/$', views.customize, name='firefox.customize'),
    url(r'^firefox/features/$', views.features, name='firefox.features'),
    url(r'^firefox/fx/$', views.fx, name='firefox.fx'),
    url(r'^firefox/geolocation/$', views.geolocation, name='firefox.geolocation'),
    url(r'^firefox/happy/$', views.happy, name='firefox.happy'),
    url(r'^firefox/new/$', views.new, name='firefox.new'),
    url(r'^firefox/organizations/faq/$', views.organizations_faq, name='firefox.organizations_faq'),
    url(r'^firefox/organizations/$', views.organizations, name='firefox.organizations'),
    url(r'^firefox/performance/$', views.performance, name='firefox.performance'),
    url(r'^firefox/security/$', views.security, name='firefox.security'),
    url(r'^firefox/speed/$', views.speed, name='firefox.speed'),
    url(r'^firefox/technology/$', views.technology, name='firefox.technology'),
    url(r'^firefox/update/$', views.update, name='firefox.update'),
)
