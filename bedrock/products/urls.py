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
    path("vpn/features/", views.vpn_features_page, name="products.vpn.features"),
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
    # Evergreen SEO articles (issue #10224)
    path(
        "vpn/more/what-is-an-ip-address/",
        views.vpn_resource_center_redirect,
        {
            "slug": "what-is-an-ip-address",
            "old_template": "products/vpn/more/ip-address.html",
            "ftl_files": ["products/vpn/more/ip-address", "products/vpn/shared"],
        },
        name="products.vpn.more.what-is-an-ip-address",
    ),
    path(
        "vpn/more/vpn-or-proxy/",
        views.vpn_resource_center_redirect,
        {
            "slug": "the-difference-between-a-vpn-and-a-web-proxy",
            "old_template": "products/vpn/more/vpn-or-proxy.html",
            "ftl_files": ["products/vpn/more/vpn-or-proxy", "products/vpn/shared"],
        },
        name="products.vpn.more.vpn-or-proxy",
    ),
    path(
        "vpn/more/what-is-a-vpn/",
        views.vpn_resource_center_redirect,
        {
            "slug": "what-is-a-vpn",
            "old_template": "products/vpn/more/what-is-a-vpn.html",
            "ftl_files": ["products/vpn/more/what-is-a-vpn", "products/vpn/shared"],
        },
        name="products.vpn.more.what-is-a-vpn",
    ),
    path(
        "vpn/more/when-to-use-a-vpn/",
        views.vpn_resource_center_redirect,
        {
            "slug": "5-reasons-you-should-use-a-vpn",
            "old_template": "products/vpn/more/when-to-use.html",
            "ftl_files": ["products/vpn/more/when-to-use-a-vpn", "products/vpn/shared"],
        },
        name="products.vpn.more.when-to-use-a-vpn",
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
    path("mozsocial/invite/", views.mozsocial_waitlist_page, name="products.mozsocial.invite"),
    path("monitor/waitlist-plus/", views.monitor_waitlist_plus_page, name="products.monitor.waitlist-plus"),
    path("monitor/waitlist-scan/", views.monitor_waitlist_scan_page, name="products.monitor.waitlist-scan"),
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
        path("monitor/", views.monitor_landing_page, name="products.monitor.landing"),
    )
