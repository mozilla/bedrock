from django.conf.urls.defaults import *
from mozorg.util import page

import views

urlpatterns = patterns('',
    page('', 'marketplace/marketplace.html'),
    page('partners', 'marketplace/partners.html')
)
