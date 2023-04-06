# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.redirects.util import redirect

redirectpatterns = (
    # Issue 12937 -
    redirect(r"^vpn/more/what-is-an-ip-address/$", "/products/vpn/resource-center/what-is-an-ip-address/"),
    redirect(r"^vpn/more/what-is-a-vpn$", "/products/vpn/resource-center/what-is-a-vpn/"),
    redirect(r"^vpn/more/vpn-or-proxy/$", "/products/vpn/resource-center/the-difference-between-a-vpn-and-a-web-proxy/"),
    redirect(r"^vpn/more/when-to-use-a-vpn/$", "/products/vpn/resource-center/5-reasons-you-should-use-a-vpn/"),
    redirect(r"^vpn/more/why-mozilla-vpn/$", "products.vpn.landing"),
    redirect(r"^vpn/more/do-i-need-a-vpn/$", "/products/vpn/resource-center/do-you-need-a-vpn-at-home-here-are-5-reasons-you-might/"),
    redirect(r"^vpn/more/what-is-a-vpn-v2/$", "/products/vpn/resource-center/what-is-a-vpn/"),
)
