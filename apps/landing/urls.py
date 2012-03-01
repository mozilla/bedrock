from django.conf.urls.defaults import *

import views


urlpatterns = patterns('',
     url(r'^firefox/toolkit/download-to-your-devices$',
         views.devices, name='landing.devices'),
)
