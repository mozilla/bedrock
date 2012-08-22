from django.conf.urls.defaults import *

import views


urlpatterns = patterns('',
    url(r'^$', views.grants, name='grants'),
    url(r'^info/(?P<slug>[\w-]+)/$', views.grant_info, name='grant_info')
)
