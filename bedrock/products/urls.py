# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import path

from bedrock.mozorg.util import page
from bedrock.products import views

urlpatterns = (
    path("vpn/", views.vpn_landing_page, name="products.vpn.landing"),
    path("vpn/invite/", views.vpn_invite_page, name="products.vpn.invite"),
    path("vpn/invite/waitlist/", views.vpn_invite_waitlist, name="products.vpn.invite.waitlist"),
    # Pages that do not use allowed_countries or default_monthly_price contexts
    page("vpn/desktop/", "products/vpn/platforms/desktop.html", ftl_files=["products/vpn/platforms/desktop", "products/vpn/shared"]),
    page("vpn/desktop/linux/", "products/vpn/platforms/linux.html", ftl_files=["products/vpn/platforms/linux", "products/vpn/shared"]),
    page("vpn/desktop/mac/", "products/vpn/platforms/mac.html", ftl_files=["products/vpn/platforms/mac", "products/vpn/shared"]),
    page("vpn/desktop/windows/", "products/vpn/platforms/windows.html", ftl_files=["products/vpn/platforms/windows", "products/vpn/shared"]),
    path("vpn/download/", views.vpn_download_page, name="products.vpn.download"),
    page("vpn/mobile/", "products/vpn/platforms/mobile.html", ftl_files=["products/vpn/platforms/mobile", "products/vpn/shared"]),
    page("vpn/mobile/ios/", "products/vpn/platforms/ios.html", ftl_files=["products/vpn/platforms/ios", "products/vpn/shared"]),
    page("vpn/mobile/android/", "products/vpn/platforms/android.html", ftl_files=["products/vpn/platforms/android", "products/vpn/shared"]),
    # Evergreen SEO articles (issue #10224)
    page("vpn/more/what-is-an-ip-address/", "products/vpn/more/ip-address.html", ftl_files=["products/vpn/more/ip-address", "products/vpn/shared"]),
    page("vpn/more/vpn-or-proxy/", "products/vpn/more/vpn-or-proxy.html", ftl_files=["products/vpn/more/vpn-or-proxy", "products/vpn/shared"]),
    page("vpn/more/what-is-a-vpn/", "products/vpn/more/what-is-a-vpn.html", ftl_files=["products/vpn/more/what-is-a-vpn", "products/vpn/shared"]),
    page(
        "vpn/more/when-to-use-a-vpn/", "products/vpn/more/when-to-use.html", ftl_files=["products/vpn/more/when-to-use-a-vpn", "products/vpn/shared"]
    ),
    # VPN pages for Product team (issue #10388)
    page("vpn/more/why-mozilla-vpn/", "products/vpn/more/why-mozilla-vpn.html", ftl_files=["products/vpn/shared"], active_locales=["en-US"]),
    page("vpn/more/do-i-need-a-vpn/", "products/vpn/more/do-i-need.html", ftl_files=["products/vpn/shared"], active_locales=["en-US"]),
    page("vpn/more/what-is-a-vpn-v2/", "products/vpn/more/what-is-a-vpn-v2.html", ftl_files=["products/vpn/shared"], active_locales=["en-US"]),
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
