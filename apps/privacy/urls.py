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
    page('privacy/policies/archive/firefox-octobe-2006', 'privacy/archive/firefox-october-2006.html'),
    page('privacy/policies/archive/firefox-june-2008', 'privacy/archive/firefox-june-2008.html'),
    page('privacy/policies/archive/firefox-january-2009', 'privacy/archive/firefox-january-2009.html'),
    page('privacy/policies/archive/firefox-mobile-september-2009', 'privacy/archive/firefox-mobile-september-2009.html'),
    page('privacy/policies/archive/firefox-january-2010', 'privacy/archive/firefox-january-2010.html'),
    page('privacy/policies/archive/firefox-december-2010', 'privacy/archive/firefox-december-2010.html'),
    page('privacy/policies/facebook', 'privacy/facebook.html'),
)
