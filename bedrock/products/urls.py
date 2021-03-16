# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.urls import path

from bedrock.mozorg.util import page
from bedrock.products import views
from bedrock.redirects.util import redirect

urlpatterns = (
    path('vpn/', views.vpn_landing_page, name='products.vpn.landing'),
    path('vpn/invite/', views.vpn_invite_page, name='products.vpn.invite'),
    path('vpn/invite/waitlist/', views.vpn_invite_waitlist, name='products.vpn.invite.waitlist'),
)

if settings.DEV:
    urlpatterns += (
        # Pages that do not use allowed_countries or default_monthly_price contexts
        page('vpn/desktop', 'products/vpn/platforms/desktop.html',
             ftl_files=['products/vpn/platforms/shared', 'products/vpn/platforms/desktop']),
    )
else:
    urlpatterns += (
        redirect(r'^vpn/desktop(/.*)?', 'products.vpn.landing', permanent=False),
    )
