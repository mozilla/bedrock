# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import l10n_utils
from django.conf import settings

def collusion(request):
    return l10n_utils.render(request, "collusion/collusion.html")

def demo(request):
    return l10n_utils.render(request, "collusion/demo.html")
