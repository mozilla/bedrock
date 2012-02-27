from django.conf.urls.defaults import *

import views


urlpatterns = patterns('',
    url(r'^$', views.b2g, name='b2g'),
    url(r'^faq/$', views.faq, name='b2g.faq'),
    url(r'^about/$', views.about, name='b2g.about'),
)
