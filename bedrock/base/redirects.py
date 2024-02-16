# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.redirects.util import redirect

redirectpatterns = (
    # Issue 11875
    # Placed redirect here instead of products/redirects.py because of a conflicting redirect to `/firefox/new` happening in map_globalconf.py,
    # and this file would be placed before the file with the conflicting redirect
    redirect(r"^vpn/download/?$", "products.vpn.download"),
)
