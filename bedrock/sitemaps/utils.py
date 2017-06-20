# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import print_function, unicode_literals

import json
import re

from django.core import urlresolvers
from django.conf import settings
from django.template.loader import get_template
from django.test import override_settings


# DEV should always be False for this to avoid some URLs that are only present in DEV=True mode
@override_settings(DEV=False)
def update_sitemaps():
    urls = []
    excludes = [
        re.compile(r) for r in settings.NOINDEX_URLS + [
            r'.*%\(.*\).*',
            r'.*//$',
            r'^media/',
            r'^robots\.txt$',
        ]
    ]

    # start with the ones we know we want
    urls.extend(settings.EXTRA_INDEX_URLS)

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
        if nonlocale:
            path = '/%s' % path
        else:
            path = '/%s/%s' % (settings.LANGUAGE_CODE, path)

        if path not in urls:
            urls.append(path)

    urls.sort()
    # Output static files
    output_json(urls)
    output_xml(urls)


def output_json(urls):
    output_file = settings.ROOT_PATH.joinpath('root_files', 'default-urls.json')

    # Output the data as a JSON file for convenience
    with output_file.open('wb') as json_file:
        json.dump(urls, json_file)


def output_xml(urls):
    output_file = settings.ROOT_PATH.joinpath('root_files', 'sitemap.xml')
    sitemap_tmpl = get_template('sitemaps/sitemap.xml').template

    ctx = {'canonical_url': settings.CANONICAL_URL, 'paths': urls}
    sitemap_tmpl.stream(ctx).dump(str(output_file))
