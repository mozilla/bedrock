from django.conf.urls.defaults import *
from views import marketplace

urlpatterns = patterns('',
    (r'^$', marketplace),
)
