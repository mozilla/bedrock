# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import path

from bedrock.mozorg.util import page
from bedrock.products import views

urlpatterns = (
    page("", "products/landing.html", ftl_files=["firefox/products"]),
    path("vpn/", views.vpn_landing_page, name="products.vpn.landing"),
    path("vpn/pricing/", views.vpn_pricing_page, name="products.vpn.pricing"),
    path("vpn/features/", views.vpn_features_page, name="products.vpn.features"),
    path("vpn/invite/", views.vpn_invite_page, name="products.vpn.invite"),
    # Pages that do not use allowed_countries or default_monthly_price contexts
    page("vpn/desktop/", "products/vpn/platforms/desktop.html", ftl_files=["products/vpn/platforms/desktop_v2", "products/vpn/shared"]),
    page("vpn/desktop/linux/", "products/vpn/platforms/linux.html", ftl_files=["products/vpn/platforms/linux_v2", "products/vpn/shared"]),
    page("vpn/desktop/mac/", "products/vpn/platforms/mac.html", ftl_files=["products/vpn/platforms/mac_v2", "products/vpn/shared"]),
    page("vpn/desktop/windows/", "products/vpn/platforms/windows.html", ftl_files=["products/vpn/platforms/windows_v2", "products/vpn/shared"]),
    path("vpn/download/", views.vpn_download_page, name="products.vpn.download"),
    path("vpn/download/mac/thanks/", views.vpn_mac_download_page, name="products.vpn.mac-download"),
    path("vpn/download/windows/thanks/", views.vpn_windows_download_page, name="products.vpn.windows-download"),
    page("vpn/mobile/", "products/vpn/platforms/mobile.html", ftl_files=["products/vpn/platforms/mobile_v2", "products/vpn/shared"]),
    page("vpn/mobile/ios/", "products/vpn/platforms/ios.html", ftl_files=["products/vpn/platforms/ios_v2", "products/vpn/shared"]),
    page("vpn/mobile/android/", "products/vpn/platforms/android.html", ftl_files=["products/vpn/platforms/android_v2", "products/vpn/shared"]),
    page("vpn/ipad/", "products/vpn/platforms/ipad.html", ftl_files=["products/vpn/platforms/ipad", "products/vpn/shared"]),
    path("monitor/waitlist-plus/", views.monitor_waitlist_plus_page, name="products.monitor.waitlist-plus"),
    path("monitor/waitlist-scan/", views.monitor_waitlist_scan_page, name="products.monitor.waitlist-scan"),
)
