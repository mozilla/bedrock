# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest

from django.conf import settings
from django.test.client import Client

from mock import patch
from nose.tools import eq_


@patch.object(settings, 'ROOT_URLCONF', 'redirects.tests.urls')
class TestUrlPatterns(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_redirect(self):
        response = self.client.get('/en-US/gloubi-boulga/')
        eq_(response.status_code, 301)
        eq_(response['Location'], 'http://testserver/en-US/mock/view/')

    def test_temporary_redirect(self):
        response = self.client.get('/en-US/gloubi-boulga/tmp/')
        eq_(response.status_code, 302)
        eq_(response['Location'], 'http://testserver/en-US/mock/view/')

    def test_external_redirect(self):
        response = self.client.get('/en-US/gloubi-boulga/ext/')
        eq_(response.status_code, 301)
        eq_(response['Location'], 'https://marketplace.mozilla.org')
