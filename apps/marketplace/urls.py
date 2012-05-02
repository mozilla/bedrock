from django.conf.urls.defaults import *
from views import marketplace, partners

urlpatterns = patterns('',
    (r'^$', marketplace),
    (r'^partners/$', partners),
)
