from django.conf.urls.defaults import *
from views import channel, button, new

urlpatterns = patterns('',
    (r'^button/', button),
    (r'^channel/', channel),
    (r'^new/', new)
)
