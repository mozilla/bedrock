# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import print_function, unicode_literals

import re

from django.core import urlresolvers
from django.conf import settings
from django.test.client import Client

from mock import patch, Mock
from django_medusa.renderers import StaticSiteRenderer

from bedrock.base.templatetags.helpers import alternate_url


@patch('bedrock.firefox.views.basket', Mock())
@patch('bedrock.newsletter.forms.NewsletterFooterForm', Mock())
@patch('bedrock.newsletter.views.basket', Mock())
@patch('bedrock.newsletter.utils.basket', Mock())
@patch('bedrock.newsletter.utils.cache', Mock())
def get_all_urls():
    client = Client()
    urls = {}
    excludes = [
        re.compile(r) for r in settings.NOINDEX_URLS + [
            r'.*%\(.*\).*',
            r'^media/',
            r'^newsletter/',
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

    # Now the urls dictionary contains path/locales pairs like this:
    # {'/firefox/new/': ['ach', 'af', 'ak', 'an', 'ar', 'ast', ...]}
    return urls


class BedrockRenderer(StaticSiteRenderer):
    def get_paths(self):
        urls = get_all_urls()
        localized_urls = []
        for url, locales in urls.iteritems():
            for locale in locales:
                localized_urls.append('/{}{}'.format(locale, url))

        return localized_urls


renderers = [BedrockRenderer]
