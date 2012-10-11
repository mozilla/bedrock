from django.conf.urls.defaults import *
from django.http import HttpResponsePermanentRedirect

urlpatterns = patterns('',
    url('videos', lambda request: HttpResponsePermanentRedirect('https://webmaker.org/videos/')),
    url('', lambda request: HttpResponsePermanentRedirect('https://webmaker.org')),
)
