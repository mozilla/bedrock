# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import url

from bedrock.mozorg.util import page
from bedrock.products import views

urlpatterns = (
    url(r'^vpn/$', views.vpn_landing_page, name='products.vpn.landing'),
    url(r'^vpn/invite/$', views.vpn_invite_page, name='products.vpn.invite'),
)
