# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.urls import path

from bedrock.mozorg.util import page
from bedrock.products import views

urlpatterns = (
    path('vpn/', views.vpn_landing_page, name='products.vpn.landing'),
    path('vpn/invite/', views.vpn_invite_page, name='products.vpn.invite'),
    path('vpn/invite/waitlist/', views.vpn_invite_waitlist, name='products.vpn.invite.waitlist'),

    # Pages that do not use allowed_countries or default_monthly_price contexts
    page('vpn/desktop', 'products/vpn/platforms/desktop.html',
         ftl_files=['products/vpn/platforms/desktop', 'products/vpn/platforms/shared']),
    page('vpn/desktop/linux', 'products/vpn/platforms/linux.html',
         ftl_files=['products/vpn/platforms/linux', 'products/vpn/platforms/shared']),
    page('vpn/desktop/mac', 'products/vpn/platforms/mac.html',
         ftl_files=['products/vpn/platforms/mac', 'products/vpn/platforms/shared']),
    page('vpn/desktop/windows', 'products/vpn/platforms/windows.html',
         ftl_files=['products/vpn/platforms/windows', 'products/vpn/platforms/shared']),
    page('vpn/mobile', 'products/vpn/platforms/mobile.html',
         ftl_files=['products/vpn/platforms/mobile', 'products/vpn/platforms/shared']),
    page('vpn/mobile/ios', 'products/vpn/platforms/ios.html',
         ftl_files=['products/vpn/platforms/ios', 'products/vpn/platforms/shared']),
)
