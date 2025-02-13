# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re

from bs4 import BeautifulSoup

from bedrock.legal_docs.views import LegalDocView, load_legal_doc
from lib import l10n_utils

HN_PATTERN = re.compile(r"^h(\d)$")
HREF_PATTERN = re.compile(r"^https?\:\/\/www\.mozilla\.org")


def process_legal_doc(content):
    """
    Load a static Markdown file and return the document as a BeautifulSoup
    object for easier manipulation.

    :param content: HTML Content of the legal doc.
    """
    soup = BeautifulSoup(content, "lxml")

    # Convert the site's full URLs to absolute paths
    for link in soup.find_all(href=HREF_PATTERN):
        link["href"] = HREF_PATTERN.sub("", link["href"])

    # Return the HTML fragment as a BeautifulSoup object
    return soup


class PrivacyDocView(LegalDocView):
    def get_legal_doc(self):
        doc = super().get_legal_doc()
        if doc is not None:
            doc["content"] = process_legal_doc(doc["content"])
        return doc


class FirefoxPrivacyDocView(PrivacyDocView):
    ftl_files = ["privacy/firefox"]

    def get_legal_doc(self):
        doc = super().get_legal_doc()
        variant = self.request.GET.get("v", None)

        if variant == "product":
            if doc["content"].select("h1"):
                self.template_name = "privacy/notices/firefox-simple-2025.html"
            else:
                self.template_name = "privacy/notices/firefox-simple.html"
        else:
            if doc["content"].select("h1"):
                self.template_name = "privacy/notices/firefox-2025.html"
            else:
                self.template_name = "privacy/notices/firefox.html"

        return doc


firefox_notices = FirefoxPrivacyDocView.as_view(template_name="privacy/notices/firefox.html", legal_doc_name="firefox_privacy_notice")

firefox_focus_notices = PrivacyDocView.as_view(template_name="privacy/notices/firefox-focus.html", legal_doc_name="focus_privacy_notice")

thunderbird_notices = PrivacyDocView.as_view(template_name="privacy/notices/thunderbird.html", legal_doc_name="thunderbird_privacy_policy")

websites_notices = PrivacyDocView.as_view(template_name="privacy/notices/websites.html", legal_doc_name="websites_privacy_notice")

mdn_plus = PrivacyDocView.as_view(template_name="privacy/notices/mdn-plus.html", legal_doc_name="mdn_plus_privacy")

ad_targeting_guidelines = PrivacyDocView.as_view(
    template_name="privacy/notices/ad-targeting-guidelines.html", legal_doc_name="adtargeting_guidelines"
)

subscription_services = PrivacyDocView.as_view(
    template_name="privacy/notices/subscription-services.html", legal_doc_name="subscription_services_privacy_notice"
)

mozilla_accounts = PrivacyDocView.as_view(template_name="privacy/notices/mozilla-accounts.html", legal_doc_name="mozilla_accounts_privacy_notice")


def privacy(request):
    doc = load_legal_doc("mozilla_privacy_policy", l10n_utils.get_locale(request))

    template_vars = {
        "doc": process_legal_doc(doc["content"]),
        "active_locales": doc["active_locales"],
    }

    return l10n_utils.render(request, "privacy/index.html", template_vars, ftl_files="privacy/index")
