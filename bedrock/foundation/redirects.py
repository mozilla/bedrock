# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.redirects.util import redirect

redirectpatterns = (
    redirect(r"^foundation/?$", "https://foundation.mozilla.org/"),
    redirect(r"^foundation/about/?$", "https://foundation.mozilla.org/about/"),
    redirect(r"^foundation/documents/?$", "https://foundation.mozilla.org/about/public-records/"),
    redirect(r"^foundation/issues/?$", "https://foundation.mozilla.org/initiatives/"),
    redirect(r"^foundation/leadership-network/?$", "https://foundation.mozilla.org/"),
    redirect(r"^foundation/advocacy/?$", "https://foundation.mozilla.org/"),
    redirect(r"^foundation/trademarks/?$", "/foundation/trademarks/policy/"),
    redirect(r"^foundation/trademarks/faq/?$", "/foundation/trademarks/policy/"),
    redirect(r"^foundation/documents/domain-name-license\.pdf$", "/foundation/trademarks/policy/"),
    redirect(r"^foundation/trademarks/poweredby/faq/?$", "/foundation/trademarks/policy/"),
    redirect(r"^foundation/trademarks/l10n-website-policy/?$", "/foundation/trademarks/policy/"),
)
