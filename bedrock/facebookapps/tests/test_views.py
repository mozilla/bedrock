# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib

from django.conf import settings
from django.test.client import Client

from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import eq_, ok_
from pyquery import PyQuery as pq

from bedrock.facebookapps import tests


@patch.object(settings, 'FACEBOOK_PAGE_NAMESPACE', 'some-namespace')
@patch.object(settings, 'FACEBOOK_APP_ID', '123456789')
class TestTabRedirect(tests.TestCase):
    def setUp(self):
        self.tab_url = '//www.facebook.com/some-namespace/app_123456789'
        self.client = Client()

    def create_response(self, js_redirect=False, method='get', data={}):
        kwargs = {'redirect_type': 'js'} if js_redirect else None

        with self.activate('en-US'):
            url = reverse('facebookapps.tab_redirect', kwargs=kwargs)
        return getattr(self.client, method)(url, data)

    def test_facebook_tab_url(self):
        eq_(settings.FACEBOOK_TAB_URL, self.tab_url)

    def test_normal_redirect(self):
        """
        Redirect to Facebook tab URL.
        """
        response = self.create_response()
        # Django's redirect adds the protocol
        url = 'http:{url}'.format(url=self.tab_url)
        self.assert_response_redirect(response, url)

    def test_iframe_header(self):
        """
        Should allow rendering in iframe.
        """
        response = self.create_response(method='post')
        self.assert_iframe_able(response)

    def test_js_redirect(self):
        """
        Redirect using JavaScript and window.top.location if `redirect_type`
        is `js`.
        """
        response = self.create_response(js_redirect=True, method='post')
        self.assert_js_redirect(response, self.tab_url)

    def test_convert_query_string(self):
        """
        Convert query string to app_data query string.
        """
        response = self.create_response(data=tests.DUMMY_DICT)
        url = 'http:{url}?{query_string}'.format(url=self.tab_url,
            query_string=tests.DUMMY_APP_DATA_QUERY)
        eq_(urllib.unquote(response['Location']), url)


class TestDownloadTab(tests.TestCase):
    def setUp(self):
        self.client = Client()

    def create_response(self):
        with self.activate('en-US'):
            url = reverse('facebookapps.downloadtab')
        return self.client.post(url)

    def test_normal_downloadtab(self):
        """
        Should have normal Download Tab response code and content.
        """
        response = self.create_response()
        eq_(response.status_code, 200)
        doc = pq(response.content)
        download_selector = '.download-button'
        share_selector = '.js-share'
        invite_selector = '.js-invite'
        ok_(doc(download_selector), 'Download Button element with selector'
            ' `{sel}` not found.'.format(sel=download_selector))
        ok_(doc(share_selector), 'Facebook share button with selector `{sel}` '
            'not found.'.format(sel=share_selector))
        ok_(doc(invite_selector), 'Facebook friend invite button with selector'
            ' `{sel}` not found.'.format(sel=invite_selector))

    def test_iframe_header(self):
        """
        Should allow rendering in iframe.
        """
        response = self.create_response()
        self.assert_iframe_able(response)
