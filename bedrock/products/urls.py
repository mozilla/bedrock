# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.urls import path

from bedrock.mozorg.util import page
from bedrock.products import views

urlpatterns = (
    path("vpn/", views.vpn_landing_page, name="products.vpn.landing"),
    path("vpn/pricing/", views.vpn_pricing_page, name="products.vpn.pricing"),
    path("vpn/invite/", views.vpn_invite_page, name="products.vpn.invite"),
    # Pages that do not use allowed_countries or default_monthly_price contexts
    path("vpn/desktop/", views.VPNDesktopView.as_view(), name="products.vpn.platforms.desktop"),
    path("vpn/desktop/linux/", views.VPNLinuxView.as_view(), name="products.vpn.platforms.linux"),
    path("vpn/desktop/mac/", views.VPNMacView.as_view(), name="products.vpn.platforms.mac"),
    path("vpn/desktop/windows/", views.VPNWindowsView.as_view(), name="products.vpn.platforms.windows"),
    path("vpn/download/", views.vpn_download_page, name="products.vpn.download"),
    path("vpn/download/mac/thanks/", views.vpn_mac_download_page, name="products.vpn.mac-download"),
    path("vpn/download/windows/thanks/", views.vpn_windows_download_page, name="products.vpn.windows-download"),
    path("vpn/mobile/", views.VPNMobileView.as_view(), name="products.vpn.platforms.mobile"),
    path("vpn/mobile/ios/", views.VPNIosView.as_view(), name="products.vpn.platforms.ios"),
    path("vpn/mobile/android/", views.VPNAndroidView.as_view(), name="products.vpn.platforms.android"),
    page("vpn/ipad/", "products/vpn/platforms/ipad.html", ftl_files=["products/vpn/platforms/ipad", "products/vpn/shared"]),
    # VPN Resource Center
    path(
        "vpn/resource-center/",
        views.resource_center_landing_view,
        name="products.vpn.resource-center.landing",
    ),
    path(
        "vpn/resource-center/<slug:slug>/",
        views.resource_center_article_view,
        name="products.vpn.resource-center.article",
    ),
)

if settings.DEV:
    urlpatterns += (
        path("relay/", views.relay_landing_page, name="products.relay.landing"),
        path("relay/waitlist/", view=views.relay_premium_waitlist__page, name="products.relay.waitlist.premium"),
        path("relay/waitlist/phone/", view=views.relay_phone_waitlist__page, name="products.relay.waitlist.phone"),
        path("relay/waitlist/bundle/", view=views.relay_bundle_waitlist__page, name="products.relay.waitlist.bundle"),
        page("relay/faq/", "products/relay/faq.html", ftl_files=["products/relay/shared", "products/relay/faq"]),
        path("relay/premium/", views.relay_premium_page, name="products.relay.premium"),
        path("relay/pricing/", views.relay_pricing_page, name="products.relay.pricing"),
    )
