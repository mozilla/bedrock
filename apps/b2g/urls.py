# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *

import views


urlpatterns = patterns('',
    url(r'^$', views.b2g, name='b2g'),
    url(r'^faq/$', views.faq, name='b2g.faq'),
    url(r'^about/$', views.about, name='b2g.about'),
)
