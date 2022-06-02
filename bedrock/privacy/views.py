# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import re

from django.views.decorators.cache import cache_page

from bs4 import BeautifulSoup
from commonware.response.decorators import xframe_allow

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
    def get_legal_doc(self):
        doc = super().get_legal_doc()
        if len(doc["content"].select(".privacy-header-firefox")) > 0:
            self.template_name = "privacy/notices/firefox.html"
        else:
            self.template_name = "privacy/notices/firefox-old-style-notice.html"
        return doc


firefox_notices = FirefoxPrivacyDocView.as_view(legal_doc_name="firefox_privacy_notice")

firefox_betterweb_notices = PrivacyDocView.as_view(template_name="privacy/notices/firefox-betterweb.html", legal_doc_name="better_web_privacy")

firefox_fire_tv_notices = PrivacyDocView.as_view(template_name="privacy/notices/firefox-fire-tv.html", legal_doc_name="Firefox_FireTV_Privacy_Notice")

firefox_focus_notices = PrivacyDocView.as_view(template_name="privacy/notices/firefox-focus.html", legal_doc_name="focus_privacy_notice")

firefox_reality_notices = PrivacyDocView.as_view(
    template_name="privacy/notices/firefox-reality.html", legal_doc_name="firefox_reality_privacy_notice"
)

hubs_notices = PrivacyDocView.as_view(template_name="privacy/notices/hubs.html", legal_doc_name="mozilla_hubs_privacy_notice")

thunderbird_notices = PrivacyDocView.as_view(template_name="privacy/notices/thunderbird.html", legal_doc_name="thunderbird_privacy_policy")

websites_notices = PrivacyDocView.as_view(template_name="privacy/notices/websites.html", legal_doc_name="websites_privacy_notice")

facebook_notices = PrivacyDocView.as_view(template_name="privacy/notices/facebook.html", legal_doc_name="facebook_privacy_info")
facebook_notices = xframe_allow(facebook_notices)

firefox_monitor_notices = PrivacyDocView.as_view(template_name="privacy/notices/firefox-monitor.html", legal_doc_name="firefox_monitor_terms_privacy")

firefox_relay_notices = PrivacyDocView.as_view(template_name="privacy/notices/firefox-relay.html", legal_doc_name="firefox_relay_privacy_notice")

firefox_private_network = PrivacyDocView.as_view(
    template_name="privacy/notices/firefox-private-network.html", legal_doc_name="Firefox_Private_Network_Beta_Privacy_Notice"
)

mozilla_vpn = PrivacyDocView.as_view(template_name="privacy/notices/mozilla-vpn.html", legal_doc_name="mozilla_vpn_privacy_notice")

mdn_plus = PrivacyDocView.as_view(template_name="privacy/notices/mdn-plus.html", legal_doc_name="mdn_plus_privacy")


@cache_page(60 * 60)  # cache for 1 hour
def privacy(request):
    doc = load_legal_doc("mozilla_privacy_policy", l10n_utils.get_locale(request))

    template_vars = {
        "doc": process_legal_doc(doc["content"]),
        "active_locales": doc["active_locales"],
    }

    return l10n_utils.render(request, "privacy/index.html", template_vars, ftl_files="privacy/index")
