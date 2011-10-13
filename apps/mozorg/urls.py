from django.conf.urls.defaults import *
from views import channel, button

urlpatterns = patterns('',
    (r'button/', button),
    (r'channel/', channel)
)
