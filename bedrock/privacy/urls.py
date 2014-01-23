# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, url

from bedrock.mozorg.util import page
from bedrock.privacy import views

urlpatterns = patterns('',
    page('/policies/firefox', 'privacy/firefox.html'),
    page('/policies/websites', 'privacy/websites.html'),
    page('/policies/thunderbird', 'privacy/thunderbird.html'),
    page('/policies/marketplace', 'privacy/marketplace.html'),
    page('/policies/persona', 'privacy/persona.html'),
    page('/policies/sync', 'privacy/sync.html'),
    page('/policies/test-pilot', 'privacy/test-pilot.html'),
    url('^/policies/archive/(?P<archive_name>(.*))/?$', views.archive, name='privacy.archive'),
    url(r'^/$', views.privacy, name='privacy.index'),
    url(r'^/policies/firefox-os/$', views.firefoxos, name='privacy.firefoxos'),
    url(r'^/policies/facebook/$', views.facebook, name='privacy/facebook'),
)
