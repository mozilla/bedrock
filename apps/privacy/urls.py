# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *

from mozorg.util import page
from privacy import views

urlpatterns = patterns('',
    page('/policies/firefox', 'privacy/firefox.html'),
    page('/policies/websites', 'privacy/websites.html'),
    page('/policies/thunderbird', 'privacy/thunderbird.html'),
    page('/policies/marketplace', 'privacy/marketplace.html'),
    page('/policies/persona', 'privacy/persona.html'),
    page('/policies/sync', 'privacy/sync.html'),
    page('/policies/test-pilot', 'privacy/test-pilot.html'),
    page('/policies/archive/firefox-octobe-2006', 'privacy/archive/firefox-october-2006.html'),
    page('/policies/archive/firefox-june-2008', 'privacy/archive/firefox-june-2008.html'),
    page('/policies/archive/firefox-january-2009', 'privacy/archive/firefox-january-2009.html'),
    page('/policies/archive/firefox-mobile-september-2009', 'privacy/archive/firefox-mobile-september-2009.html'),
    page('/policies/archive/firefox-january-2010', 'privacy/archive/firefox-january-2010.html'),
    page('/policies/archive/firefox-december-2010', 'privacy/archive/firefox-december-2010.html'),
    url(r'^/$', views.privacy, name='privacy.index'),
    url(r'^/policies/facebook/$', views.facebook, name='privacy/facebook'),
)
