from django.conf.urls.defaults import *
from views import research

urlpatterns = patterns('',
    (r'^research/', research)
)
