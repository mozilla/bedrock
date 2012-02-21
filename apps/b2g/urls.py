from django.conf.urls.defaults import *
from views import b2g, about, developerfaq

urlpatterns = patterns('',
    (r'^b2g/faq/', developerfaq),
    (r'^b2g/about/', about),
    (r'^b2g/', b2g),
)
