# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import re

from django.views.decorators.cache import cache_page

from commonware.response.decorators import xframe_allow
from bs4 import BeautifulSoup

from lib import l10n_utils

from bedrock.legal_docs.views import LegalDocView, load_legal_doc


HN_PATTERN = re.compile(r'^h(\d)$')
HREF_PATTERN = re.compile(r'^https?\:\/\/www\.mozilla\.org')


def process_legal_doc(content):
    """
    Load a static Markdown file and return the document as a BeautifulSoup
    object for easier manipulation.

    :param content: HTML Content of the legal doc.
    """
    soup = BeautifulSoup(content)

    # Manipulate the markup
    for section in soup.find_all('section'):
        level = 0
        header = soup.new_tag('header')
        div = soup.new_tag('div')

        section.insert(0, header)
        section.insert(1, div)

        # Append elements to <header> or <div>
        for tag in section.children:
            if not tag.name:
                continue
            match = HN_PATTERN.match(tag.name)
            if match:
                header.append(tag)
                level = int(match.group(1))
            if tag.name == 'p':
                (header if level == 1 else div).append(tag)
            if tag.name in ['ul', 'hr']:
                div.append(tag)

        if level > 3:
            section.parent.div.append(section)

        # Remove empty <div>s
        if len(div.contents) == 0:
            div.extract()

    # Convert the site's full URLs to absolute paths
    for link in soup.find_all(href=HREF_PATTERN):
        link['href'] = HREF_PATTERN.sub('', link['href'])

    # Return the HTML fragment as a BeautifulSoup object
    return soup


class PrivacyDocView(LegalDocView):
    def get_legal_doc(self):
        doc = super(PrivacyDocView, self).get_legal_doc()
        doc['content'] = process_legal_doc(doc['content'])
        return doc


class FirefoxPrivacyDocView(PrivacyDocView):
    template_name = 'privacy/notices/firefox.html'

    def get_legal_doc(self):
        doc = super(FirefoxPrivacyDocView, self).get_legal_doc()
        if len(doc['content'].select('.privacy-header-firefox')) > 0:
            self.template_name = 'privacy/notices/firefox-quantum.html'
        return doc


firefox_notices = FirefoxPrivacyDocView.as_view(
    legal_doc_name='firefox_privacy_notice')

firefox_os_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox-os.html',
    legal_doc_name='firefox_os_privacy_notice')

firefox_fire_tv_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox-fire-tv.html',
    legal_doc_name='Firefox_FireTV_Privacy_Notice')

firefox_cloud_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox-cloud.html',
    legal_doc_name='firefox_cloud_services_PrivacyNotice')

firefox_hello_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox-hello.html',
    legal_doc_name='WebRTC_PrivacyNotice')

firefox_focus_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox-focus.html',
    legal_doc_name='focus_privacy_notice')

firefox_lite_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox-lite.html',
    legal_doc_name='firefox_lite_privacy_notice')

firefox_reality_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox-reality.html',
    legal_doc_name='firefox_reality_privacy_notice')

firefox_screenshotgo_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox-screenshotgo.html',
    legal_doc_name='firefox_screenshotgo_privacy_notice')

thunderbird_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/thunderbird.html',
    legal_doc_name='thunderbird_privacy_policy')

websites_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/websites.html',
    legal_doc_name='websites_privacy_notice')

facebook_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/facebook.html',
    legal_doc_name='facebook_privacy_info')
facebook_notices = xframe_allow(facebook_notices)

firefox_monitor_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox-monitor.html',
    legal_doc_name='firefox_monitor_terms_privacy')


@cache_page(60 * 60)  # cache for 1 hour
def privacy(request):
    doc = load_legal_doc('mozilla_privacy_policy', l10n_utils.get_locale(request))

    template_vars = {
        'doc': process_legal_doc(doc['content']),
        'active_locales': doc['active_locales'],
    }

    return l10n_utils.render(request, 'privacy/index.html', template_vars)
