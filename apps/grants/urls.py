from django.conf.urls.defaults import *

import views


urlpatterns = patterns('',
    url(r'^$', views.grants, name='grants'),
    # attempt to not break existing URLS
    url(r'^(?P<slug>[\w-]+).html$', views.grant_info, name='grant_info')
)
