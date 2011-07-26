from django.conf.urls.defaults import *
from views import channel

urlpatterns = patterns('',
    (r'channel/', channel)
)
