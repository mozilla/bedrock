# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import path

from bedrock.products import views
from bedrock.redirects.util import redirect

urlpatterns = (
    path("vpn/", views.vpn_landing_page, name="products.vpn.landing"),
    path("vpn/pricing/", views.vpn_pricing_page, name="products.vpn.pricing"),
    path("vpn/invite/", views.vpn_invite_page, name="products.vpn.invite"),
    # Pages that do not use allowed_countries or default_monthly_price contexts
    path("vpn/download/", views.vpn_download_page, name="products.vpn.download"),
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
    # Issue #12937 - updating VPN subnav
    redirect(r"^vpn/desktop/$", "products.vpn.download", permanent=True),
    redirect(r"^vpn/desktop/linux/$", "products.vpn.download", permanent=True),
    redirect(r"^vpn/desktop/mac/$", "products.vpn.download", permanent=True),
    redirect(r"^vpn/desktop/windows/$", "products.vpn.download", permanent=True),
    redirect(r"^vpn/mobile/$", "products.vpn.download", permanent=True),
    redirect(r"^vpn/mobile/android/$", "products.vpn.download", permanent=True),
    redirect(r"^vpn/mobile/ios/$", "products.vpn.download", permanent=True),
    redirect(r"^vpn/more/what-is-an-ip-address/$", "/products/vpn/resource-center/what-is-an-ip-address/", permanent=True),
    redirect(r"^vpn/more/what-is-a-vpn$", "/products/vpn/resource-center/what-is-a-vpn/", permanent=True),
    redirect(r"^vpn/more/vpn-or-proxy/$", "/products/vpn/resource-center/the-difference-between-a-vpn-and-a-web-proxy/", permanent=True),
    redirect(r"^vpn/more/when-to-use-a-vpn/$", "/products/vpn/resource-center/5-reasons-you-should-use-a-vpn/", permanent=True),
    redirect(r"^vpn/more/why-mozilla-vpn/$", "products.vpn.landing", permanent=True),
    redirect(r"^vpn/more/do-i-need-a-vpn/$", "/products/vpn/resource-center/do-you-need-a-vpn-at-home-here-are-5-reasons-you-might/", permanent=True),
    redirect(r"^vpn/more/what-is-a-vpn-v2/$", "/products/vpn/resource-center/what-is-a-vpn/", permanent=True),
)
