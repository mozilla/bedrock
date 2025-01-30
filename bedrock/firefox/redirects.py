# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.redirects.util import mobile_app_redirector, platform_redirector, redirect


def firefox_mobile_faq(request, *args, **kwargs):
    qs = request.META.get("QUERY_STRING", "")
    if "os=firefox-os" in qs:
        return "https://support.mozilla.org/products/firefox-os"

    return "https://support.mozilla.org/products/mobile"


def firefox_channel(*args, **kwargs):
    return platform_redirector("firefox.channel.desktop", "firefox.channel.android", "firefox.channel.ios")


def mobile_app(request, *args, **kwargs):
    campaign = None
    product = "firefox"

    product_options = ["firefox", "focus", "klar"]

    campaign_options = [
        "firefox-all",
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
    # bug 1299947, 1326383
    redirect(r"^firefox/channel/?$", firefox_channel(), cache_timeout=0),
    # issue https://github.com/mozilla/bedrock/issues/14172
    redirect(r"^firefox/browsers/mobile/app/?$", mobile_app, cache_timeout=0, query=False),
)
