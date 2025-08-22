# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.redirects.util import gone, redirect

redirectpatterns = (
    # bug 818323
    redirect(r"^projects/security/known-vulnerabilities\.html$", "security.known-vulnerabilities"),
    redirect(r"^projects/security/older-vulnerabilities\.html$", "security.older-vulnerabilities"),
    # bug 1090468
    redirect(
        r"^security/(?P<page>older-alerts|security-announcement|phishing-test(-results)?)\.html$",
        "http://website-archive.mozilla.org/www.mozilla.org/security/security/{page}.html",
    ),
    redirect(
        r"^security/iSECPartners_Phishing\.pdf$", "http://website-archive.mozilla.org/www.mozilla.org/security/security/iSECPartners_Phishing.pdf"
    ),
    # issue 16519
    gone(r"^security/advisories/cve-feed\.json$"),
)
