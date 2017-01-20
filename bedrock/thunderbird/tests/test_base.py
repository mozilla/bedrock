# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

from django.conf import settings

from mock import patch, Mock
from nose.tools import eq_, ok_
from pyquery import PyQuery as pq

from bedrock.base.urlresolvers import reverse
from bedrock.thunderbird.details import ThunderbirdDesktop
from bedrock.mozorg.tests import TestCase


TEST_DATA_DIR = os.path.join(settings.ROOT, 'bedrock', 'firefox', 'tests', 'test_data')
PROD_DETAILS_DIR = os.path.join(TEST_DATA_DIR, 'product_details_json')
GOOD_PLATS = {'Windows': {}, 'OS X': {}, 'Linux': {}}

thunderbird_desktop = ThunderbirdDesktop(json_dir=PROD_DETAILS_DIR)


@patch('bedrock.thunderbird.views.thunderbird_desktop._storage.data',
       Mock(side_effect=thunderbird_desktop._storage.data))
class TestThunderbirdAll(TestCase):
    def _get_url(self, channel='release'):
        with self.activate('en-US'):
            kwargs = {}

            if channel != 'release':
                kwargs['channel'] = channel

            return reverse('thunderbird.latest.all', kwargs=kwargs)

    def test_no_search_results(self):
        """
        Tables should be gone and not-found message should be shown when there
        are no search results.
        """
        resp = self.client.get(self._get_url() + '?q=DOES_NOT_EXIST')
        doc = pq(resp.content)
        ok_(not doc('table.build-table'))
        ok_(not doc('.not-found.hide'))

    def test_no_search_query(self):
        """
        When not searching all builds should show.
        """
        resp = self.client.get(self._get_url())
        doc = pq(resp.content)
        eq_(len(doc('.build-table')), 1)
        eq_(len(doc('.not-found.hide')), 1)

        num_builds = len(thunderbird_desktop.get_filtered_full_builds('release'))
        eq_(len(doc('tr[data-search]')), num_builds)
        eq_(len(doc('tr#en-US a')), 5)
