from django.conf.urls.defaults import *

from mozorg.util import page

urlpatterns = patterns('',
    page('', 'privacy/index.html'),
    page('policies/firefox', 'privacy/firefox.html'),
    page('policies/firefox-third-party', 'privacy/firefox-third-party.html'),
    page('policies/websites', 'privacy/websites.html'),
    page('policies/thunderbird', 'privacy/thunderbird.html'),
    page('policies/marketplace', 'privacy/marketplace.html'),
    page('policies/persona', 'privacy/persona.html'),
    page('policies/sync', 'privacy/sync.html'),
    page('policies/test-pilot', 'privacy/test-pilot.html'),
    page('policies/archive/firefox-octobe-2006', 'privacy/archive/firefox-october-2006.html'),
    page('policies/archive/firefox-june-2008', 'privacy/archive/firefox-june-2008.html'),
    page('policies/archive/firefox-january-2009', 'privacy/archive/firefox-january-2009.html'),
    page('policies/archive/firefox-mobile-september-2009', 'privacy/archive/firefox-mobile-september-2009.html'),
    page('policies/archive/firefox-january-2010', 'privacy/archive/firefox-january-2010.html'),
    page('policies/archive/firefox-december-2010', 'privacy/archive/firefox-december-2010.html'),
)
