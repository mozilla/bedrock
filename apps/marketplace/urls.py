from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^$', views.marketplace, name='marketplace'),
    url(r'^partners/$', views.partners, name='partners')
)
