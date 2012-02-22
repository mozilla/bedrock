from django.conf.urls.defaults import *
from views import persona, about, developerfaq, termsofservice, privacypolicy

urlpatterns = patterns('',
    (r'^persona/developer-faq/$', developerfaq),
    (r'^persona/terms-of-service/$', termsofservice),
    (r'^persona/privacy-policy/$', privacypolicy),
    (r'^persona/about/$', about),
    (r'^persona/$', persona),
)
