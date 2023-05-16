# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import path
from django.views.generic.base import RedirectView

from bedrock.legal_docs.views import LegalDocView
from bedrock.mozorg.util import page

urlpatterns = (
    page(
        "",
        "pocket/home.html",
        url_name="pocket.home",
        ftl_files=["pocket/home"],
    ),
    page(
        "about/",
        "pocket/about.html",
        url_name="pocket.about",
        ftl_files=["pocket/about"],
    ),
    page(
        "add/",
        "pocket/add.html",
        url_name="pocket.add",
        ftl_files=["pocket/add"],
    ),
    page(
        "android/",
        "pocket/android.html",
        url_name="pocket.android",
        ftl_files=["pocket/platforms"],
    ),
    page(
        "ios/",
        "pocket/ios.html",
        url_name="pocket.ios",
        ftl_files=["pocket/platforms"],
    ),
    page(
        "chrome/",
        "pocket/chrome.html",
        url_name="pocket.chrome",
        ftl_files=["pocket/platforms"],
    ),
    page(
        "safari/",
        "pocket/safari.html",
        url_name="pocket.safari",
        ftl_files=["pocket/platforms"],
    ),
    page(
        "opera/",
        "pocket/opera.html",
        url_name="pocket.opera",
        ftl_files=["pocket/platforms"],
    ),
    page(
        "edge/",
        "pocket/edge.html",
        url_name="pocket.edge",
        ftl_files=["pocket/platforms"],
    ),
    page(
        "welcome/",
        "pocket/welcome.html",
        url_name="pocket.welcome",
        ftl_files=["pocket/platforms"],
    ),
    page(
        "contact-info/",
        "pocket/contact-info.html",
        url_name="pocket.contact-info",
    ),
    page(
        "firefox/new_tab_learn_more/",
        "pocket/firefox/new-tab-learn-more.html",
        url_name="pocket.firefox-new-tab-learn-more",
        ftl_files=["pocket/firefox/new-tab"],
    ),
    page(
        "pocket-and-firefox/",
        "pocket/pocket-and-firefox.html",
        url_name="pocket.pocket-and-firefox",
        ftl_files=["pocket/feature-pages", "pocket/banners/pocket-premium"],
    ),
    page(
        "get-inspired/",
        "pocket/get-inspired.html",
        url_name="pocket.get-inspired",
        ftl_files=["pocket/feature-pages", "pocket/banners/pocket-premium"],
    ),
    page(
        "jobs/",
        "pocket/jobs.html",
        url_name="pocket.jobs",
    ),
    page(
        "save-to-pocket/",
        "pocket/save-to-pocket.html",
        url_name="pocket.save-to-pocket",
        ftl_files=["pocket/feature-pages", "pocket/banners/pocket-premium"],
    ),
    page(
        "opensource_licenses_ios/",
        "pocket/license-ios.html",
        url_name="pocket.opensource_licenses_ios",
    ),
    page(
        "pocket-updates-signup/pilot/",
        "pocket/updates-signup.html",
        url_name="pocket.updates-signup-pilot",
    ),
    path(
        "privacy/",
        LegalDocView.as_view(
            template_name="pocket/privacy.html",
            legal_doc_name="pocket_privacy_policy",
        ),
        name="pocket.privacy",
    ),
    path(
        "tos/",
        LegalDocView.as_view(
            template_name="pocket/tos.html",
            legal_doc_name="pocket_tos",
        ),
        name="pocket.tos",
    ),
    path(
        "pocket-updates-signup/",
        RedirectView.as_view(
            pattern_name="pocket.updates-signup-pilot",
            permanent=False,
        ),
    ),
)
