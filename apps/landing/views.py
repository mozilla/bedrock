# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import l10n_utils
from product_details import product_details

def devices(request):
    return l10n_utils.render(request, "landing/devices.html", {'latest_version': product_details.firefox_versions['LATEST_FIREFOX_VERSION']} )
