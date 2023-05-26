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
    page("vpn/desktop/", "products/vpn/platforms/desktop.html", ftl_files=["products/vpn/platforms/desktop", "products/vpn/shared"]),
    page("vpn/desktop/linux/", "products/vpn/platforms/linux.html", ftl_files=["products/vpn/platforms/linux", "products/vpn/shared"]),
    page("vpn/desktop/mac/", "products/vpn/platforms/mac.html", ftl_files=["products/vpn/platforms/mac", "products/vpn/shared"]),
    page("vpn/desktop/windows/", "products/vpn/platforms/windows.html", ftl_files=["products/vpn/platforms/windows", "products/vpn/shared"]),
    path("vpn/download/", views.vpn_download_page, name="products.vpn.download"),
    path("vpn/download/mac/thanks/", views.vpn_mac_download_page, name="products.vpn.mac-download"),
    path("vpn/download/windows/thanks/", views.vpn_windows_download_page, name="products.vpn.windows-download"),
    page("vpn/mobile/", "products/vpn/platforms/mobile.html", ftl_files=["products/vpn/platforms/mobile", "products/vpn/shared"]),
    page("vpn/mobile/ios/", "products/vpn/platforms/ios.html", ftl_files=["products/vpn/platforms/ios", "products/vpn/shared"]),
    page("vpn/mobile/android/", "products/vpn/platforms/android.html", ftl_files=["products/vpn/platforms/android", "products/vpn/shared"]),
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
        path("relay/invite/", views.relay_invite_page, name="products.relay.invite"),
        path("relay/waitlist/vpn/", view=views.relay_vpn_waitlist__page, name="products.relay.waitlist.vpn"),
        path("relay/waitlist/phone/", view=views.relay_phone_waitlist__page, name="products.relay.waitlist.phone"),
        page("relay/faq/", "products/relay/faq.html", ftl_files=["products/relay/shared", "products/relay/faq"]),
    )
