# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import print_function, unicode_literals

import json
import re

from django.core import urlresolvers
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.test import override_settings
from django.test.client import Client

from mock import patch

from bedrock.grants import grants_db
from bedrock.releasenotes.models import ProductRelease
from bedrock.security.models import SecurityAdvisory


SEC_KNOWN_VULNS = [
    '/security/known-vulnerabilities/firefox/',
    '/security/known-vulnerabilities/firefox-esr/',
    '/security/known-vulnerabilities/firefox-os/',
    '/security/known-vulnerabilities/thunderbird/',
    '/security/known-vulnerabilities/thunderbird-esr/',
    '/security/known-vulnerabilities/seamonkey/',
    '/security/known-vulnerabilities/firefox-3.6/',
    '/security/known-vulnerabilities/firefox-3.5/',
    '/security/known-vulnerabilities/firefox-3.0/',
    '/security/known-vulnerabilities/firefox-2.0/',
    '/security/known-vulnerabilities/firefox-1.5/',
    '/security/known-vulnerabilities/firefox-1.0/',
    '/security/known-vulnerabilities/thunderbird-3.1/',
    '/security/known-vulnerabilities/thunderbird-3.0/',
    '/security/known-vulnerabilities/thunderbird-2.0/',
    '/security/known-vulnerabilities/thunderbird-1.5/',
    '/security/known-vulnerabilities/thunderbird-1.0/',
    '/security/known-vulnerabilities/seamonkey-2.0/',
    '/security/known-vulnerabilities/seamonkey-1.1/',
    '/security/known-vulnerabilities/seamonkey-1.0/',
    '/security/known-vulnerabilities/mozilla-suite/',
]


def get_grants_urls():
    urls = {}
    for grant in grants_db.GRANTS:
        urls['/grants/{}.html'.format(grant.url)] = ['en-US']

    return urls


def get_security_urls():
    urls = {url: ['en-US'] for url in SEC_KNOWN_VULNS}
    for advisory in SecurityAdvisory.objects.all():
        try:
            adv_url = advisory.get_absolute_url()
        except urlresolvers.NoReverseMatch:
            continue

        # strip "/en-US" off the front
        if adv_url.startswith('/en-US'):
            adv_url = adv_url[6:]

        urls[adv_url] = ['en-US']

    return urls


def get_release_notes_urls():
    urls = {}
    for release in ProductRelease.objects.exclude(product='Thunderbird'):
        # we redirect all release notes for versions 28.x and below to an archive
        # and Firefox for iOS uses a different version numbering scheme
        if release.product != 'Firefox for iOS' and release.major_version_int < 29:
            continue

        try:
            rel_path = release.get_absolute_url()
            req_path = release.get_sysreq_url()
        except urlresolvers.NoReverseMatch:
            continue

        # strip "/en-US" off the front
        if rel_path.startswith('/en-US'):
            rel_path = rel_path[6:]
        if req_path.startswith('/en-US'):
            req_path = req_path[6:]

        urls[rel_path] = ['en-US']
        urls[req_path] = ['en-US']

    return urls


# DEV should always be False for this to avoid some URLs that are only present in DEV=True mode
@override_settings(DEV=False)
def get_static_urls():
    urls = {}
    client = Client()
    excludes = [
        re.compile(r) for r in settings.NOINDEX_URLS + [
            r'.*%\(.*\).*',
            r'.*//$',
            r'^media/',
            r'^robots\.txt$',
            # Redirects in en-US. Added via EXTRA_INDEX_URLS
            r'firefox-klar/$',
        ]
    ]

    # start with the ones we know we want
    urls.update(settings.EXTRA_INDEX_URLS)

    # get_resolver is an undocumented but convenient function.
    # Try to retrieve all valid URLs on this site.
    # NOTE: have to use `iterlists()` here since the standard
    # `iteritems()` only returns the first item in the list for the
    # view since `reverse_dict` is a `MultiValueDict`.
    for key, values in urlresolvers.get_resolver(None).reverse_dict.iterlists():
        for value in values:
            path = value[0][0][0]
            # Exclude pages that we don't want be indexed by search engines.
            # Some other URLs are also unnecessary for the sitemap.
            if any(exclude.search(path) for exclude in excludes):
                continue

            path_prefix = path.split('/', 2)[0]
            nonlocale = path_prefix in settings.SUPPORTED_NONLOCALES
            path = '/%s' % path
            if nonlocale:
                locales = []
            else:
                with patch('lib.l10n_utils.django_render') as render:
                    render.return_value = HttpResponse()
                    client.get('/' + settings.LANGUAGE_CODE + path)

                # Exclude urls that did not call render
                if not render.called:
                    continue

                locales = render.call_args[0][2]['translations'].keys()

                # zh-CN is a redirect on the homepage
                if path == '/':
                    locales.remove('zh-CN')

                # Firefox Focus has a different URL in German
                if path == '/privacy/firefox-focus/':
                    locales.remove('de')

                # just remove any locales not in our prod list
                locales = list(set(locales).intersection(settings.PROD_LANGUAGES))

            if path not in urls:
                urls[path] = locales

    return urls


def update_sitemaps():
    urls = get_static_urls()
    urls.update(get_release_notes_urls())
    urls.update(get_security_urls())
    urls.update(get_grants_urls())
    # Output static files
    output_json(urls)
    output_xml(urls)


def output_json(urls):
    output_file = settings.ROOT_PATH.joinpath('root_files', 'sitemap.json')

    # Output the data as a JSON file for convenience
    with output_file.open('wb') as json_file:
        json.dump(urls, json_file)


def output_xml(urls):
    urls_by_locale = {}
    for url, locales in urls.iteritems():
        if not locales:
            urls_by_locale.setdefault('none', [])
            urls_by_locale['none'].append(url)

        for locale in locales:
            urls_by_locale.setdefault(locale, [])
            urls_by_locale[locale].append(url)

    for locale, urls in urls_by_locale.iteritems():
        if locale != 'none':
            output_file = settings.ROOT_PATH.joinpath('root_files', locale, 'sitemap.xml')
            output_file.parent.mkdir(exist_ok=True)
        else:
            output_file = settings.ROOT_PATH.joinpath('root_files', 'sitemap_none.xml')

        sitemap_tmpl = get_template('sitemaps/sitemap.xml').template
        ctx = {
            'canonical_url': settings.CANONICAL_URL,
            'paths': sorted(urls),
            'locale': locale,
        }
        sitemap_tmpl.stream(ctx).dump(str(output_file))

    output_file = settings.ROOT_PATH.joinpath('root_files', 'sitemap.xml')
    sitemap_tmpl = get_template('sitemaps/sitemap_index.xml').template

    ctx = {'canonical_url': settings.CANONICAL_URL, 'locales': sorted(urls_by_locale.keys())}
    sitemap_tmpl.stream(ctx).dump(str(output_file))
