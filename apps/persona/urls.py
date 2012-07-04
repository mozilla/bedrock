from django.conf.urls.defaults import *
from mozorg.util import page

urlpatterns = patterns('',
    page('', 'persona/persona.html'),
    page('about', 'persona/about.html'),
    page('privacy-policy', 'persona/privacy-policy.html'),
    page('terms-of-service', 'persona/terms-of-service.html'),
    page('developer-faq', 'persona/developer-faq.html')
)
