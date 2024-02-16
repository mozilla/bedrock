# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.redirects.util import redirect

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
)
