from django.conf.urls.defaults import *

from mozorg.util import page

urlpatterns = patterns('',
    page('privacy', 'privacy/index.html'),
    page('privacy/policies/firefox', 'privacy/firefox.html'),
    page('privacy/policies/websites', 'privacy/websites.html'),
    page('privacy/policies/thunderbird', 'privacy/thunderbird.html'),
    page('privacy/policies/marketplace', 'privacy/marketplace.html'),
    page('privacy/policies/persona', 'privacy/persona.html'),
    page('privacy/policies/sync', 'privacy/sync.html'),
    page('privacy/policies/test-pilot', 'privacy/test-pilot.html'),
)