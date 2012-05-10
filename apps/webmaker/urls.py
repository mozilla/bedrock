from django.conf.urls.defaults import *
from views import webmaker

urlpatterns = patterns('',
    url(r'^$', webmaker, name='webmaker_index'),
)
