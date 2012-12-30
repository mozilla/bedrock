# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *
from redirects.util import redirect
from mozorg.util import page

import views


urlpatterns = patterns('',
    url(r'^$', views.grants, name='grants'),
    url(r'^(?P<slug>[\w-]+).html$', views.grant_info, name='grant_info'),
    page('reports/gnome-haeger-report', 'grants/reports/gnome-haeger-report.html'),
    page('reports/ushahidi-chile-report', 'grants/reports/ushahidi-chile-report.html'),
    redirect(r'.*/$', views.grants),
)
