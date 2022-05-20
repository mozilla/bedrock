# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.util import page

urlpatterns = (
    page(
        "firefox/",
        "landing/firefox.html",
        # ftl_files=["landing/firefox", "landing/shared"],
    ),
    page(
        "pocket/",
        "landing/pocket.html",
        # ftl_files=["landing/pocket", "landing/shared"],
    ),
    page(
        "vpn/",
        "landing/vpn.html",
        # ftl_files=["landing/vpn", "landing/shared"],
    ),
)
