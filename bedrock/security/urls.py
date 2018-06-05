# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import url

from bedrock.mozorg.util import page
from bedrock.security.views import (
    mitre_cve_feed,
    AdvisoriesView,
    AdvisoryView,
    HallOfFameView,
    KVRedirectsView,
    OldAdvisoriesListView,
    OldAdvisoriesView,
    ProductView,
    ProductVersionView,
)


urlpatterns = (
    page('', 'security/index.html'),
    page('bug-bounty', 'security/bug-bounty.html'),
    page('client-bug-bounty', 'security/client-bug-bounty.html'),
    page('web-bug-bounty', 'security/web-bug-bounty.html'),
    page('bug-bounty/faq', 'security/bug-bounty/faq.html'),
    page('bug-bounty/faq-webapp', 'security/bug-bounty/faq-webapp.html'),
    page('bug-bounty/web-eligible-sites', 'security/bug-bounty/web-eligible-sites.html'),

    url(r'^bug-bounty/hall-of-fame/$',
        HallOfFameView.as_view(program='client'), name='security.bug-bounty.hall-of-fame'),
    url(r'^bug-bounty/web-hall-of-fame/$',
        HallOfFameView.as_view(program='web'), name='security.bug-bounty.web-hall-of-fame'),
    url(r'^advisories/$',
        AdvisoriesView.as_view(), name='security.advisories'),
    url(r'^advisories/mfsa(?P<pk>\d{4}-\d{2,3})/$',
        AdvisoryView.as_view(), name='security.advisory'),
    url(r'^advisories/cve-feed\.json$', mitre_cve_feed, name='security.advisories.cve_feed'),

    page('known-vulnerabilities', 'security/known-vulnerabilities.html'),
    page('known-vulnerabilities/older-vulnerabilities', 'security/older-vulnerabilities.html'),
    url(r'^known-vulnerabilities/(?P<slug>[a-z-]+)/$',
        ProductView.as_view(), name='security.product-advisories'),
    url(r'^known-vulnerabilities/(?P<product>[\w-]+)-(?P<version>\d{1,3}(\.\d{1,3})?)/$',
        ProductVersionView.as_view(), name='security.product-version-advisories'),
    url(r'^known-vulnerabilities/(?P<filename>.*)\.html$', KVRedirectsView.as_view()),

    url(r'^(?:announce|advisories)(?:/.*)?/mfsa(?P<pk>\d{4}-\d{2,3})\.html$',
        OldAdvisoriesView.as_view()),
    url(r'^announce/$', OldAdvisoriesListView.as_view()),
)
