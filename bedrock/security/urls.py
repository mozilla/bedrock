# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import path, re_path

from bedrock.mozorg.util import page
from bedrock.security.views import (
    AdvisoriesView,
    AdvisoryView,
    HallOfFameView,
    KVRedirectsView,
    OldAdvisoriesListView,
    OldAdvisoriesView,
    ProductVersionView,
    ProductView,
    mitre_cve_feed,
)

urlpatterns = (
    page("", "security/index.html"),
    page("bug-bounty/", "security/bug-bounty.html"),
    page("client-bug-bounty/", "security/client-bug-bounty.html"),
    page("web-bug-bounty/", "security/web-bug-bounty.html"),
    page("bug-bounty/faq/", "security/bug-bounty/faq.html"),
    page("bug-bounty/faq-webapp/", "security/bug-bounty/faq-webapp.html"),
    page("bug-bounty/web-eligible-sites/", "security/bug-bounty/web-eligible-sites.html"),
    path("bug-bounty/hall-of-fame/", HallOfFameView.as_view(program="client"), name="security.bug-bounty.hall-of-fame"),
    path("bug-bounty/web-hall-of-fame/", HallOfFameView.as_view(program="web"), name="security.bug-bounty.web-hall-of-fame"),
    path("advisories/", AdvisoriesView.as_view(), name="security.advisories"),
    re_path(r"^advisories/mfsa(?P<pk>\d{4}-\d{2,3})/$", AdvisoryView.as_view(), name="security.advisory"),
    re_path(r"^advisories/cve-feed\.json$", mitre_cve_feed, name="security.advisories.cve_feed"),
    page("known-vulnerabilities/", "security/known-vulnerabilities.html"),
    page("known-vulnerabilities/older-vulnerabilities/", "security/older-vulnerabilities.html"),
    re_path(r"^known-vulnerabilities/(?P<slug>[a-z-]+)/$", ProductView.as_view(), name="security.product-advisories"),
    re_path(
        r"^known-vulnerabilities/(?P<product>[\w-]+)-(?P<version>\d{1,3}(\.\d{1,3})?)/$",
        ProductVersionView.as_view(),
        name="security.product-version-advisories",
    ),
    re_path(r"^known-vulnerabilities/(?P<filename>.*)\.html$", KVRedirectsView.as_view()),
    re_path(r"^(?:announce|advisories)(?:/.*)?/mfsa(?P<pk>\d{4}-\d{2,3})\.html$", OldAdvisoriesView.as_view()),
    path("announce/", OldAdvisoriesListView.as_view()),
    page("third-party-software-injection/", "security/third-party-injection-policy.html"),
)
