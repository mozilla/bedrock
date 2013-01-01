from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url(r'^tabzilla\.js$', views.tabzilla_js, name='tabzilla'),
)
