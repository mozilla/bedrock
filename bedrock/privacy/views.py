# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from os import path
import re
import StringIO

import jingo
import markdown as md
from bs4 import BeautifulSoup

from commonware.response.decorators import xframe_allow

from django.core.mail import EmailMessage
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect

from lib import l10n_utils
from funfactory.settings_base import path as base_path
from forms import PrivacyContactForm


LEGAL_DOCS_PATH = base_path('vendor-local', 'src', 'legal-docs')


def load_legal_doc(request, doc_name):
    """
    Load a static Markdown file and return the document as a BeautifulSoup
    object for easier manipulation.
    """
    locale = l10n_utils.get_locale(request)
    source = path.join(LEGAL_DOCS_PATH, doc_name, locale + '.md')
    output = StringIO.StringIO()

    if not path.exists(source):
        source = path.join(LEGAL_DOCS_PATH, doc_name, 'en-US.md')

    # Parse the Markdown file
    md.markdownFromFile(input=source, output=output,
                        extensions=['attr_list', 'outline(wrapper_cls=)'])
    content = output.getvalue().decode('utf8')
    output.close()

    soup = BeautifulSoup(content)
    hn_pattern = re.compile(r'^h(\d)$')
    href_pattern = re.compile(r'^https?\:\/\/www\.mozilla\.org')

    # Manipulate the markup
    for section in soup.find_all('section'):
        level = 0
        header = soup.new_tag('header')
        div = soup.new_tag('div')

        section.insert(0, header)
        section.insert(1, div)

        # Append elements to <header> or <div>
        for tag in section.children:
            match = hn_pattern.match(tag.name)
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
    for link in soup.find_all(href=href_pattern):
        link['href'] = href_pattern.sub('', link['href'])

    # Return the HTML flagment as a BeautifulSoup object
    return soup


@cache_page(60 * 60)  # cache for 1 hour
def firefox_notices(request):
    return l10n_utils.render(request, 'privacy/notices/firefox.html',
                             {'doc': load_legal_doc(request, 'firefox_privacy_notice')})


@cache_page(60 * 60)  # cache for 1 hour
def firefox_os_notices(request):
    return l10n_utils.render(request, 'privacy/notices/firefox-os.html',
                             {'doc': load_legal_doc(request, 'firefox_os_privacy_notice')})


@cache_page(60 * 60)  # cache for 1 hour
def firefox_cloud_notices(request):
    return l10n_utils.render(request, 'privacy/notices/firefox-cloud.html',
                             {'doc': load_legal_doc(request, 'firefox_cloud_services_PrivacyNotice')})


@cache_page(60 * 60)  # cache for 1 hour
def websites_notices(request):
    return l10n_utils.render(request, 'privacy/notices/websites.html',
                             {'doc': load_legal_doc(request, 'websites_privacy_notice')})


@cache_page(60 * 60)  # cache for 1 hour
@xframe_allow
def facebook_notices(request):
    return l10n_utils.render(request, 'privacy/notices/facebook.html',
                             {'doc': load_legal_doc(request, 'facebook_privacy_info')})


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
        'doc': load_legal_doc(request, 'mozilla_privacy_policy'),
    }

    return l10n_utils.render(request, 'privacy/index.html', template_vars)
