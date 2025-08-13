# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

from bedrock.redirects.util import redirect

FXC = settings.FXC_BASE_URL + "/"  # no locale-respectign redirect in play here

redirectpatterns = (
    # Issue 11875
    # Placed redirect here instead of products/redirects.py because of a conflicting redirect to `/firefox/new` happening in map_globalconf.py,
    # and this file would be placed before the file with the conflicting redirect
    redirect(r"^vpn/download/?$", "products.vpn.download"),
    # Issue 16089
    # These /exp/ redirects need to come before both mozorg and firefox app redirects to avoid conflicts.
    # Keeping them in once place also helps make the redirect logic easier to follow.
    redirect(r"^/exp/?$", "mozorg.home"),
    redirect(r"^/exp/opt-out/?$", "https://www.convert.com/opt-out/"),
    redirect(r"^/exp/firefox/?$", f"{FXC}"),
    redirect(r"^/exp/firefox/new/?$", f"{FXC}"),
    redirect(r"^/exp/firefox/accounts/?$", "mozorg.account"),
    redirect(r"^/exp/firefox/mobile/?$", "firefox.browsers.mobile.index"),
)
