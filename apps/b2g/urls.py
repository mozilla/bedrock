from django.conf.urls.defaults import *
from views import b2g, about, faq

urlpatterns = patterns('',
    (r'^faq/$', faq),
    (r'^about/$', about),
    (r'^$', b2g),
)
