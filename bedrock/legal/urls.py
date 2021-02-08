# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import url

from bedrock.mozorg.util import page
from bedrock.legal import views

from bedrock.legal_docs.views import LegalDocView

urlpatterns = (
    page('', 'legal/index.html', ftl_files=['mozorg/about/legal']),

    page('eula', 'legal/eula.html'),
    page('eula/firefox-2', 'legal/eula/firefox-2-eula.html'),
    page('eula/firefox-3', 'legal/eula/firefox-3-eula.html'),
    page('eula/thunderbird-1.5', 'legal/eula/thunderbird-1.5-eula.html'),
    page('eula/thunderbird-2', 'legal/eula/thunderbird-2-eula.html'),
    page('firefox', 'legal/firefox.html'),
    # The "impressum" page is intended for Germany. Redirect to German (de) if
    # requested in any other locale. (Bug 1248393)
    page('impressum', 'legal/impressum.html', active_locales=['de']),

    url(r'^terms/betterweb/$', LegalDocView.as_view(template_name='legal/terms/betterweb.html', legal_doc_name='better_web_terms'),
        name='legal.terms.betterweb'),

    url(r'^terms/mozilla/$', LegalDocView.as_view(template_name='legal/terms/mozilla.html', legal_doc_name='Websites_ToU'),
        name='legal.terms.mozilla'),

    url(r'^terms/mozilla-vpn/$', LegalDocView.as_view(template_name='legal/terms/mozilla-vpn.html',
        legal_doc_name='Mozilla_VPN_ToS'), name='legal.terms.mozilla-vpn'),

    url(r'^terms/firefox/$', LegalDocView.as_view(template_name='legal/terms/firefox.html', legal_doc_name='firefox_about_rights'),
        name='legal.terms.firefox'),

    url(r'^terms/firefox-lite/$', LegalDocView.as_view(template_name='legal/terms/firefox-lite.html',
        legal_doc_name='firefox_lite_contentservices_ToS'), name='legal.terms.firefox-lite'),

    url(r'^terms/firefox-lite/reward/$', LegalDocView.as_view(template_name='legal/terms/firefox-lite-reward.html',
        legal_doc_name='firefox_lite_contentservices_reward'), name='legal.terms.firefox-lite-reward'),

    url(r'^terms/firefox-reality/$', LegalDocView.as_view(template_name='legal/terms/firefox-reality.html',
        legal_doc_name='firefox_reality_about_rights'), name='legal.terms.firefox-reality'),

    url(r'^terms/firefox-private-network/$', LegalDocView.as_view(template_name='legal/terms/firefox-private-network.html',
        legal_doc_name='Firefox_Private_Network_ToS'), name='legal.terms.firefox-private-network'),

    url(r'^terms/firefox-relay/$', LegalDocView.as_view(template_name='legal/terms/firefox-relay.html',
        legal_doc_name='firefox_relay_ToS'), name='legal.terms.firefox-relay'),

    url(r'^terms/thunderbird/$', LegalDocView.as_view(template_name='legal/terms/thunderbird.html', legal_doc_name='thunderbird_about_rights'),
        name='legal.terms.thunderbird'),

    url(r'^terms/services/$', LegalDocView.as_view(template_name='legal/terms/services.html', legal_doc_name='firefox_cloud_services_ToS'),
        name='legal.terms.services'),

    page('terms/vpn', 'legal/terms/vpn.html'),

    url(r'^acceptable-use/$', LegalDocView.as_view(template_name='legal/terms/acceptable-use.html', legal_doc_name='acceptable_use_policy'),
        name='legal.terms.acceptable-use'),

    url(r'^report-infringement/$', LegalDocView.as_view(template_name='legal/report-infringement.html', legal_doc_name='report_infringement'),
        name='legal.report-infringement'),

    url('^fraud-report/$', views.fraud_report, name='legal.fraud-report'),
)
