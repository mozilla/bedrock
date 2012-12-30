# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import l10n_utils
from django.conf import settings

def persona(request):
    return l10n_utils.render(request, "persona/persona.html")

def about(request):
    return l10n_utils.render(request, "persona/about.html")

def developerfaq(request):
    return l10n_utils.render(request, "persona/developer-faq.html")

def termsofservice(request):
    return l10n_utils.render(request, "persona/terms-of-service.html")

def privacypolicy(request):
    return l10n_utils.render(request, "persona/privacy-policy.html")

