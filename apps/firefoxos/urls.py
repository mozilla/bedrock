from django.conf.urls.defaults import *

import views


urlpatterns = patterns('',
    url(r'^$', views.b2g, name='firefoxos'),
    url(r'^faq/$', views.faq, name='firefoxos.faq'),
    url(r'^about/$', views.about, name='firefoxos.about'),
)
