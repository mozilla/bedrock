# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.conf.urls import url
from django.urls import path

from .util import page
from . import views
from bedrock.redirects.util import redirect


urlpatterns = (
    url(r'^$', views.home_view, name='mozorg.home'),
    page('about', 'mozorg/about.html'),
    page('about/manifesto', 'mozorg/about/manifesto.html'),
    page('about/manifesto/details', 'mozorg/about/manifesto-details.html'),
    page('about/leadership', 'mozorg/about/leadership.html'),
    page('about/policy/lean-data', 'mozorg/about/policy/lean-data/index.html'),
    page('about/policy/lean-data/build-security', 'mozorg/about/policy/lean-data/build-security.html'),
    page('about/policy/lean-data/stay-lean', 'mozorg/about/policy/lean-data/stay-lean.html'),
    page('about/policy/lean-data/engage-users', 'mozorg/about/policy/lean-data/engage-users.html'),
    page('about/policy/patents', 'mozorg/about/policy/patents/index.html'),
    page('about/policy/patents/license', 'mozorg/about/policy/patents/license.html'),
    page('about/policy/patents/license/1.0', 'mozorg/about/policy/patents/license-1.0.html'),
    page('about/policy/patents/guide', 'mozorg/about/policy/patents/guide.html'),
    page('book', 'mozorg/book.html'),
    url('^credits/$', views.credits_view, name='mozorg.credits'),
    page('credits/faq', 'mozorg/credits-faq.html'),
    page('about/history', 'mozorg/about/history.html'),
    # Bug 981063, catch all for old calendar urls.
    # must be here to avoid overriding the above
    redirect(r'^projects/calendar/', 'https://www.thunderbird.net/calendar/', locale_prefix=False),
    page('mission', 'mozorg/mission.html', ftl_files=['mozorg/mission']),
    url('^about/forums/$', views.forums_view, name='mozorg.about.forums.forums'),
    page('about/forums/etiquette', 'mozorg/about/forums/etiquette.html'),
    page('about/forums/cancellation', 'mozorg/about/forums/cancellation.html'),
    page('about/governance', 'mozorg/about/governance/governance.html'),
    page('about/governance/roles', 'mozorg/about/governance/roles.html'),
    page('about/governance/policies', 'mozorg/about/governance/policies/policies.html'),
    page('about/governance/policies/commit', 'mozorg/about/governance/policies/commit.html'),
    page('about/governance/policies/commit/access-policy',
         'mozorg/about/governance/policies/commit/access-policy.html'),
    page('about/governance/policies/commit/requirements',
         'mozorg/about/governance/policies/commit/requirements.html'),
    page('about/governance/policies/security-group/bugs',
         'mozorg/about/governance/policies/security/bugs.html'),
    page('about/governance/policies/security-group/membership',
         'mozorg/about/governance/policies/security/membership.html'),
    page('about/governance/policies/security-group/certs',
         'mozorg/about/governance/policies/security/certs/index.html'),
    page('about/governance/policies/security-group/certs/policy',
         'mozorg/about/governance/policies/security/certs/policy.html'),
    page('about/governance/organizations', 'mozorg/about/governance/organizations.html'),
    page('about/governance/policies/participation', 'mozorg/about/governance/policies/participation.html'),
    page('about/governance/policies/participation/reporting', 'mozorg/about/governance/policies/reporting.html'),
    page('about/governance/policies/participation/reporting/community-hotline', 'mozorg/about/governance/policies/community-hotline.html'),
    page('about/governance/policies/module-ownership',
         'mozorg/about/governance/policies/module-ownership.html'),
    page('about/governance/policies/regressions',
         'mozorg/about/governance/policies/regressions.html'),

    page('about/policy/transparency', 'mozorg/about/policy/transparency/index.html'),
    page('about/policy/transparency/jan-dec-2015',
         'mozorg/about/policy/transparency/jan-dec-2015.html'),
    page('about/policy/transparency/jan-jun-2016',
         'mozorg/about/policy/transparency/jan-jun-2016.html'),
    page('about/policy/transparency/jul-dec-2016',
         'mozorg/about/policy/transparency/jul-dec-2016.html'),
    page('about/policy/transparency/jan-jun-2017',
         'mozorg/about/policy/transparency/jan-jun-2017.html'),
    page('about/policy/transparency/jul-dec-2017',
         'mozorg/about/policy/transparency/jul-dec-2017.html'),
    page('about/policy/transparency/jan-jun-2018',
         'mozorg/about/policy/transparency/jan-jun-2018.html'),
    page('about/policy/transparency/jul-dec-2018',
         'mozorg/about/policy/transparency/jul-dec-2018.html'),
    page('about/policy/transparency/jan-jun-2019',
         'mozorg/about/policy/transparency/jan-jun-2019.html'),
    page('about/policy/transparency/jul-dec-2019',
         'mozorg/about/policy/transparency/jul-dec-2019.html'),
    page('about/policy/transparency/jan-jun-2020',
         'mozorg/about/policy/transparency/jan-jun-2020.html'),

    page('contact', 'mozorg/contact/contact-landing.html'),
    page('contact/spaces', 'mozorg/contact/spaces/spaces-landing.html'),
    page('contact/spaces/mountain-view', 'mozorg/contact/spaces/mountain-view.html'),
    page('contact/spaces/beijing', 'mozorg/contact/spaces/beijing.html'),
    page('contact/spaces/berlin', 'mozorg/contact/spaces/berlin.html'),
    page('contact/spaces/london', 'mozorg/contact/spaces/london.html'),
    page('contact/spaces/paris', 'mozorg/contact/spaces/paris.html'),
    page('contact/spaces/portland', 'mozorg/contact/spaces/portland.html'),
    page('contact/spaces/san-francisco', 'mozorg/contact/spaces/san-francisco.html'),
    page('contact/spaces/taipei', 'mozorg/contact/spaces/taipei.html'),
    page('contact/spaces/toronto', 'mozorg/contact/spaces/toronto.html'),
    page('contact/spaces/vancouver', 'mozorg/contact/spaces/vancouver.html'),

    page('MPL', 'mozorg/mpl/index.html'),
    page('MPL/historical', 'mozorg/mpl/historical.html'),
    page('MPL/license-policy', 'mozorg/mpl/license-policy.html'),
    page('MPL/headers', 'mozorg/mpl/headers/index.html'),
    page('MPL/1.1', 'mozorg/mpl/1.1/index.html'),
    page('MPL/1.1/FAQ', 'mozorg/mpl/1.1/faq.html'),
    page('MPL/1.1/annotated', 'mozorg/mpl/1.1/annotated/index.html'),
    page('MPL/2.0', 'mozorg/mpl/2.0/index.html'),
    page('MPL/2.0/FAQ', 'mozorg/mpl/2.0/faq.html'),
    page('MPL/2.0/Revision-FAQ', 'mozorg/mpl/2.0/revision-faq.html'),
    page('MPL/2.0/combining-mpl-and-gpl', 'mozorg/mpl/2.0/combining-mpl-and-gpl.html'),
    page('MPL/2.0/differences', 'mozorg/mpl/2.0/differences.html'),
    page('MPL/2.0/permissive-code-into-mpl', 'mozorg/mpl/2.0/permissive-code-into-mpl.html'),

    url('^contribute/$', views.ContributeView.as_view(), name='mozorg.contribute.index'),

    page('moss', 'mozorg/moss/index.html'),
    page('moss/foundational-technology', 'mozorg/moss/foundational-technology.html'),
    page('moss/mission-partners', 'mozorg/moss/mission-partners.html'),
    page('moss/secure-open-source', 'mozorg/moss/secure-open-source.html'),

    url(r'^robots\.txt$', views.Robots.as_view(), name='robots.txt'),

    # namespaces
    url(r'^2004/em-rdf$', views.namespaces, {'namespace': 'em-rdf'}),
    url(r'^2005/app-update$', views.namespaces, {'namespace': 'update'}),
    url(r'^2006/addons-blocklist$', views.namespaces, {'namespace': 'addons-bl'}),
    url(r'^2006/browser/search/$', views.namespaces, {'namespace': 'mozsearch'}),
    url(r'^keymaster/gatekeeper/there\.is\.only\.xul$', views.namespaces, {'namespace': 'xul'}),
    url(r'^microsummaries/0\.1$', views.namespaces, {'namespace': 'microsummaries'}),
    url(r'^projects/xforms/2005/type$', views.namespaces, {'namespace': 'xforms-type'}),
    url(r'^xbl$', views.namespaces, {'namespace': 'xbl'}),

    page('locales', 'mozorg/locales.html'),
)

if settings.DEV:
    urlpatterns += (
        path('homepage-preview/<content_id>/', views.HomePagePreviewView.as_view()),
    )
