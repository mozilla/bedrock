# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import path

from bedrock.legal import views
from bedrock.legal_docs.views import LegalDocView
from bedrock.mozorg.util import page

urlpatterns = (
    page("", "legal/index.html", ftl_files=["mozorg/about/legal"]),
    page("eula/", "legal/eula.html"),
    page("eula/firefox-2/", "legal/eula/firefox-2-eula.html"),
    page("eula/firefox-3/", "legal/eula/firefox-3-eula.html"),
    page("eula/thunderbird-1.5/", "legal/eula/thunderbird-1.5-eula.html"),
    page("eula/thunderbird-2/", "legal/eula/thunderbird-2-eula.html"),
    # issue #11383 The template is hard-coded English
    page("firefox/", "legal/firefox.html"),
    # issue #12332 The template is hard-coded English
    page("terms/staycation/", "legal/terms/staycation.html", ftl_files=["mozorg/about/legal", "privacy/index"]),
    # The "impressum" page is intended for Germany. Redirect to German (de) if
    # requested in any other locale. (Bug 1248393)
    page("impressum/", "legal/impressum.html", active_locales=["de"], ftl_files=["mozorg/about/legal"]),
    path("terms/mozilla/", LegalDocView.as_view(template_name="legal/terms/mozilla.html", legal_doc_name="Websites_ToU"), name="legal.terms.mozilla"),
    page("terms/peopleofdeutschland/", "legal/terms/peopleofdeutschland.html", active_locales=["en-US", "de"], ftl_files=["mozorg/about/legal"]),
    # Builders AI Challenge - Terms and Conditions
    page("terms/builders-challenge/", "legal/terms/builders-challenge.html"),
    path(
        "terms/firefox/",
        LegalDocView.as_view(template_name="legal/terms/firefox.html", legal_doc_name="firefox_about_rights"),
        name="legal.terms.firefox",
    ),
    path(
        "terms/firefox-reality/",
        LegalDocView.as_view(template_name="legal/terms/firefox-reality.html", legal_doc_name="firefox_reality_about_rights"),
        name="legal.terms.firefox-reality",
    ),
    path(
        "terms/firefox-private-network/",
        LegalDocView.as_view(template_name="legal/terms/firefox-private-network.html", legal_doc_name="Firefox_Private_Network_ToS"),
        name="legal.terms.firefox-private-network",
    ),
    path(
        "terms/thunderbird/",
        LegalDocView.as_view(template_name="legal/terms/thunderbird.html", legal_doc_name="thunderbird_about_rights"),
        name="legal.terms.thunderbird",
    ),
    path(
        "terms/mdn-plus/",
        LegalDocView.as_view(template_name="legal/terms/mdn-plus.html", legal_doc_name="mdn_plus_terms"),
        name="legal.terms.mdn-plus",
    ),
    path(
        "terms/services/",
        LegalDocView.as_view(template_name="legal/terms/services.html", legal_doc_name="firefox_cloud_services_ToS"),
        name="legal.terms.services",
    ),
    path(
        "terms/hubs/",
        LegalDocView.as_view(template_name="legal/terms/hubs.html", legal_doc_name="hubs_tos"),
        name="legal.terms.hubs",
    ),
    path(
        "terms/subscription-services/",
        LegalDocView.as_view(template_name="legal/terms/subscription-services.html", legal_doc_name="subscription_services_tos"),
        name="legal.terms.subscription-services",
    ),
    path(
        "acceptable-use/",
        LegalDocView.as_view(template_name="legal/terms/acceptable-use.html", legal_doc_name="acceptable_use_policy"),
        name="legal.terms.acceptable-use",
    ),
    path(
        "report-infringement/",
        LegalDocView.as_view(template_name="legal/report-infringement.html", legal_doc_name="report_infringement"),
        name="legal.report-infringement",
    ),
    path("defend-mozilla-trademarks/", views.fraud_report, name="legal.fraud-report"),
)
