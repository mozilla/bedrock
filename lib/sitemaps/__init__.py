# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
import re

from jingo import env
from jinja2 import FileSystemLoader
from django.core import urlresolvers
from django.conf import settings
from django.test.client import Client
from mock import Mock, patch


TEMPLATE_DIRS = (os.path.join(settings.ROOT, 'lib', 'sitemaps', 'templates'),)


# Prevent view from calling to salesforce.com
post_mock = Mock()
status_mock = post_mock.return_value.status_code = 200


@patch('bedrock.mozorg.views.requests.post', post_mock)
def update_sitemaps():
    client = Client()
    urls = {}
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
        if (not isinstance(key, basestring) or
                any(exclude.match(path) for exclude in excludes)):
            continue
        path = '/' + path
        # Send a request to each page. It takes a while to finish this process
        # but it's probably a reliable way to get complete data.
        with patch('lib.l10n_utils.django_render') as render:
            response = client.get('/' + settings.LANGUAGE_CODE + path)
        # Exclude redirects
        if isinstance(response.status_code, int):
            continue
        # Retrieve the translation list from the context data
        urls[path] = render.call_args[0][2]['translations'].keys()

    # Now the urls dictionary contains path/locales pairs like this:
    # {'/firefox/new/': ['ach', 'af', 'ak', 'an', 'ar', 'ast', ...]}

    # Output static files
    output_json(urls)
    output_xml(urls)


def output_json(urls):
    # Prepare a directory to save a JSON file
    output_dir = os.path.join(settings.ROOT, 'lib', 'sitemaps', 'json')
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # Output the data as a JSON file for convenience
    with open(os.path.join(output_dir, 'urls.json'), 'w') as json_file:
        json.dump(urls, json_file)


@patch.object(env, 'loader', FileSystemLoader(TEMPLATE_DIRS))
def output_xml(urls):
    # Prepare a directory to save XML files
    output_dir = os.path.join(settings.ROOT, 'media', 'sitemaps')
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # Output the XML sitemap index file
    template = env.get_template('index.xml')
    ctx = {'settings': settings}
    template.stream(ctx).dump(os.path.join(output_dir, 'index.xml'))

    # Output the XML sitemaps for each locale
    template = env.get_template('sitemap.xml')
    for locale in settings.PROD_LANGUAGES:
        if locale == settings.LANGUAGE_CODE:
            localized_urls = urls
        else:
            # Filter the complete URL list to remove unlocalized URLs
            localized_urls = dict((url, locales)
                for url, locales in urls.iteritems() if locale in locales)
        ctx = {'settings': settings, 'locale': locale, 'urls': localized_urls}
        template.stream(ctx).dump(os.path.join(output_dir, locale + '.xml'))
