from django.conf.urls.defaults import *
from views import persona, about, developerfaq, termsofservice, privacypolicy

urlpatterns = patterns('',
    (r'^developer-faq/$', developerfaq),
    (r'^terms-of-service/$', termsofservice),
    (r'^privacy-policy/$', privacypolicy),
    (r'^about/$', about),
    (r'^$', persona),
)
