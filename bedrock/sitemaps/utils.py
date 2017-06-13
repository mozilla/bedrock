# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import print_function, unicode_literals

import json
import re
import sys

from django.core import urlresolvers
from django.conf import settings
from django.template.loader import get_template
from django.test.client import Client

from mock import patch, Mock

from bedrock.base.templatetags.helpers import alternate_url


@patch('bedrock.firefox.views.basket', Mock())
@patch('bedrock.newsletter.forms.NewsletterFooterForm', Mock())
@patch('bedrock.newsletter.views.basket', Mock())
@patch('bedrock.newsletter.utils.basket', Mock())
@patch('bedrock.newsletter.utils.cache', Mock())
def update_sitemaps():
    client = Client()
    urls = {}
    alt_urls = {}
    excludes = [
        re.compile(r) for r in settings.NOINDEX_URLS + [
            r'.*%\(.*\).*',
            r'^media/',
            r'^robots\.txt$',
        ]
    ]

    # get_resolver is an undocumented but convenient function.
    # Try to retrieve all valid URLs on this site.
    for key, value in urlresolvers.get_resolver(None).reverse_dict.iteritems():
        path = value[0][0][0]
        # Exclude pages that we don't want be indexed by search engines.
        # Some other URLs are also unnecessary for the sitemap.
        if any(exclude.search(path) for exclude in excludes):
            continue

        path_prefix = path.split('/', 2)[0]
        nonlocale = path_prefix in settings.SUPPORTED_NONLOCALES
        path = '/' + path
        if nonlocale:
            urls[path] = []
        else:
            # Send a request to each page. It takes a while to finish this process
            # but it's probably a reliable way to get complete data.
            with patch('lib.l10n_utils.django_render') as render:
                try:
                    alt_path = alternate_url(path, settings.LANGUAGE_CODE)
                    if alt_path:
                        # de seems most likely to exist
                        response = client.get('/de' + path)
                    else:
                        response = client.get('/' + settings.LANGUAGE_CODE + path)
                except Exception:
                    raise

            # Exclude redirects
            if isinstance(response.status_code, int):
                continue

            # Retrieve the translation list from the context data
            ctx = render.call_args[0][2]
            urls[path] = sorted(ctx['translations'].keys())

        sys.stdout.write('.')
        sys.stdout.flush()

    # Now the urls dictionary contains path/locales pairs like this:
    # {'/firefox/new/': ['ach', 'af', 'ak', 'an', 'ar', 'ast', ...]}

    # Output static files
    output_json(urls)
    output_xml(urls, alt_urls)


def output_json(urls):
    # Prepare a directory to save a JSON file
    output_file = settings.ROOT_PATH.joinpath('root_files', 'all-urls.json')

    # Output the data as a JSON file for convenience
    with output_file.open('wb') as json_file:
        json.dump(urls, json_file)


def output_xml(urls, alt_urls):
    # Prepare a directory to save XML files
    output_dir = settings.ROOT_PATH.joinpath('root_files')
    # index_tmpl = get_template('sitemaps/index.xml').template
    sitemap_tmpl = get_template('sitemaps/sitemap.xml').template

    # Output the XML sitemap index file
    # ctx = {'settings': settings}
    # index_tmpl.stream(ctx).dump(str(output_dir.joinpath('sitemap.xml')))

    # Output the XML sitemaps for each locale
    ctx = {'settings': settings, 'urls': urls, 'alt_urls': alt_urls}
    sitemap_tmpl.stream(ctx).dump(str(output_dir.joinpath('sitemap.xml')))
