# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import re

from django.core.mail import EmailMessage
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect

import jingo
from commonware.response.decorators import xframe_allow
from bs4 import BeautifulSoup

from lib import l10n_utils
from .forms import PrivacyContactForm

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
        return process_legal_doc(doc)


firefox_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox.html',
    legal_doc_name='firefox_privacy_notice')

firefox_os_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox-os.html',
    legal_doc_name='firefox_os_privacy_notice')

firefox_cloud_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/firefox-cloud.html',
    legal_doc_name='firefox_cloud_services_PrivacyNotice')

websites_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/websites.html',
    legal_doc_name='websites_privacy_notice')

facebook_notices = PrivacyDocView.as_view(
    template_name='privacy/notices/facebook.html',
    legal_doc_name='facebook_privacy_info')
facebook_notices = xframe_allow(facebook_notices)


def submit_form(request, form):
    form_submitted = False

    if form.is_valid():
        form_submitted = True
        form_error = False

        honeypot = form.cleaned_data.pop('office_fax')

        if honeypot:
            form_error = True
        else:
            subject = 'Message sent from Privacy Hub'
            sender = form.cleaned_data['sender']
            to = ['yourprivacyis#1@mozilla.com']
            msg = jingo.render_to_string(request, 'privacy/includes/email-info.txt', form.cleaned_data)
            headers = {'Reply-To': sender}

            email = EmailMessage(subject, msg, sender, to, headers=headers)
            email.send()
    else:
        form_error = True

    return {'form_submitted': form_submitted, 'form_error': form_error}


@cache_page(60 * 60)  # cache for 1 hour
@csrf_protect
def privacy(request):
    form = PrivacyContactForm()

    form_submitted = False
    form_error = False

    if request.method == 'POST':
        form = PrivacyContactForm(request.POST)
        form_results = submit_form(request, form)

        form_submitted = form_results['form_submitted']
        form_error = form_results['form_error']

    template_vars = {
        'form': form,
        'form_submitted': form_submitted,
        'form_error': form_error,
        'doc': process_legal_doc(load_legal_doc('mozilla_privacy_policy',
                                                l10n_utils.get_locale(request))
        ),
    }

    return l10n_utils.render(request, 'privacy/index.html', template_vars)
