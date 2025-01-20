# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.redirects.util import mobile_app_redirector, redirect


def mobile_app(request, *args, **kwargs):
    campaign = None
    product = "vpn"

    product_options = ["vpn"]

    campaign_options = [
        "vpn-landing-page",
        "vpn-pricing-page",
    ]

    for p in product_options:
        if p == request.GET.get("product"):
            product = p
            break

    for c in campaign_options:
        if c == request.GET.get("campaign"):
            campaign = c
            break

    return mobile_app_redirector(request, product, campaign)


redirectpatterns = (
    # Issue 10335
    redirect(r"^vpn/?$", "products.vpn.landing"),
    # Issue 12937
    redirect(r"^products/vpn/more/why-mozilla-vpn/$", "products.vpn.landing"),
    redirect(r"^products/vpn/more/do-i-need-a-vpn/$", "/products/vpn/resource-center/do-you-need-a-vpn-at-home-here-are-5-reasons-you-might/"),
    redirect(r"^products/vpn/more/what-is-a-vpn-v2/$", "/products/vpn/resource-center/what-is-a-vpn/"),
    # Issue 11875
    redirect(r"^vpn/download/windows/?$", "products.vpn.windows-download"),
    redirect(r"^vpn/download/mac/?$", "products.vpn.mac-download"),
    redirect(r"^products/mozsocial/invite/?$", "products.landing"),
    redirect(r"^products/vpn/mobile/app/?$", mobile_app, cache_timeout=0, query=False),
    # Issue 15386
    redirect(r"^products/vpn/resource-center/no-Logging-vpn-from-mozilla/$", "/products/vpn/resource-center/no-logging-vpn-from-mozilla/"),
    # Issue 15843
    redirect("/products/vpn/more/what-is-an-ip-address/", "/products/vpn/resource-center/what-is-an-ip-address/"),
    redirect(
        "/products/vpn/more/the-difference-between-a-vpn-and-a-web-proxy/",
        "/products/vpn/resource-center/the-difference-between-a-vpn-and-a-web-proxy/",
    ),
    redirect("/products/vpn/more/what-is-a-vpn/", "/products/vpn/resource-center/what-is-a-vpn/"),
    redirect("/products/vpn/more/5-reasons-you-should-use-a-vpn/", "/products/vpn/resource-center/5-reasons-you-should-use-a-vpn/"),
)
