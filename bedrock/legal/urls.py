# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, url

from bedrock.mozorg.util import page
from bedrock.legal import views

urlpatterns = patterns('',
    page('eula', 'legal/eula.html'),
    page('firefox', 'legal/firefox.html'),
    url('^fraud-report/$', views.fraud_report, name='legal.fraud-report'),
)
