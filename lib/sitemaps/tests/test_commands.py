# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mock import Mock, patch
from nose.tools import eq_, ok_
from pyquery import PyQuery as pq
from django.conf import settings
from django.test import TestCase
from lib.sitemaps import update_sitemaps


# Prevent view from calling to salesforce.com
post_mock = Mock()
status_mock = post_mock.return_value.status_code = 200


@patch('bedrock.mozorg.views.requests.post', post_mock)
class TestUpdateSitemaps(TestCase):
    def setUp(self):
        update_sitemaps()

    def test_index(self):
        """
        index.xml should be a XML sitemap index containing the list of
        locale-based sitemap URLs.
        """
        # Use the HTML parser to ignore XML and XHTML namespaces
        doc = pq(filename=settings.ROOT + settings.XML_SITEMAP_INDEX,
                 parser='html')
        langs = settings.PROD_LANGUAGES

        eq_(len(doc('sitemap')), len(langs))
        eq_(doc('sitemap').eq(0).find('loc').text(),
            settings.CANONICAL_URL + '/media/sitemaps/' + langs[0] + '.xml')

    def test_locale(self):
        """
        {locale}.xml should be a locale-based XML sitemap containing the list of
        indexable pages with alternate URLs.
        """
        # Use the HTML parser to ignore XML and XHTML namespaces
        doc = pq(filename=settings.ROOT + settings.XML_SITEMAP_DIR + '/en-US.xml',
                 parser='html')

        # The first item should be the home page
        eq_(doc('url').eq(0).find('loc').text(),
            settings.CANONICAL_URL + '/en-US/')

        # And there should be the alternate URLs
        ok_(doc('url').eq(0).find('link').attr('href')
            .startswith(settings.CANONICAL_URL))
