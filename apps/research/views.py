# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import l10n_utils
from django.conf import settings

def research(request):
    return l10n_utils.render(request, "research/research.html")

def people(request):
    return l10n_utils.render(request, "research/people.html")

