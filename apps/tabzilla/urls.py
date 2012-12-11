from django.conf.urls.defaults import *
from mozorg.util import page

import views

urlpatterns = patterns('',
    url(r'^tabzilla\.js$', views.tabzilla_js, name='tabzilla'),
)
