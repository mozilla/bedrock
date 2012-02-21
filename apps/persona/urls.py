from django.conf.urls.defaults import *
from views import persona, about, developerfaq

urlpatterns = patterns('',
    (r'^persona/developer-faq/$', developerfaq),
    (r'^persona/about/$', about),
    (r'^persona/$', persona),
)
