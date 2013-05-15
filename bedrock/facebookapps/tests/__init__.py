# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import cgi
import hashlib
import hmac
import json
from base64 import urlsafe_b64encode
from time import time

from bedrock.mozorg import tests as mozorg_tests
from nose.tools import eq_, ok_
from pyquery import PyQuery as pq


DUMMY_CONTENT = 'I like pie.'
DUMMY_DICT = {'pie': 'pumpkin', 'pizza': 'yes'}
DUMMY_APP_DATA_QUERY = 'app_data[pie]=pumpkin&app_data[pizza]=yes'
DUMMY_PATH = '/dummy-path'


class TestCase(mozorg_tests.TestCase):
    def assert_response_redirect(self, response, url, status_code=302):
        eq_(response.status_code, status_code, 'Redirect response status_code'
            ' should be {code}. Received {bad_code}.'.format(
                code=status_code, bad_code=response.status_code))
        ok_(response.has_header('Location'), 'No `Location` header found in '
            'response:\n\n{response}.'.format(response=response))
        eq_(response['Location'], url)

    def assert_js_redirect(self, response, url, status_code=200,
                           selector='#redirect', data_attr='redirect-url'):
        eq_(response.status_code, status_code, 'JavaScript redirect '
            'status_code should be {code}. Received {bad_code}.'
            .format(code=status_code, bad_code=response.status_code))

        doc = pq(response.content)
        element = doc(selector)
        ok_(element, 'No element with selector `{selector}` found in response:'
            '\n\n{response}'.format(selector=selector,
                response=response.content))

        escaped_url = cgi.escape(url)
        data_value = element.attr('data-{attr}'.format(attr=data_attr))
        eq_(data_value, escaped_url, 'Attribute `data-{attr}` should be '
            '{value}. Received `{bad_value}`.'.format(attr=data_attr,
                value=escaped_url, bad_value=data_value))

    def assert_iframe_able(self, response):
        header = 'X-Frame-Options'
        self.assertFalse(response.has_header(header),
            '{header} header present in response.'.format(header=header))


def create_payload(user_id=None, algorithm='HMAC-SHA256', country='us',
                   locale='en_US', app_data=None):
    """
    Creates a signed request payload with the proper structure.

    Adapted from Affiliates' `facebook` app tests (http://bit.ly/11kieLq).
    """
    payload = {
        'algorithm': algorithm,
        'issued_at': int(time()),
        'user': {
            'country': country,
            'locale': locale
        }
    }

    if user_id:
        payload['user_id'] = user_id
    if app_data:
        payload['app_data'] = app_data
    return payload


def create_signed_request(payload):
    """
    Creates an encoded signed request like the one Facebook sends to iframe
    apps.

    Adapted from Affiliates' `facebook` app tests (http://bit.ly/XWH98V).
    """
    payload = create_payload() if not payload else payload
    json_payload = json.dumps(payload)
    encoded_json = urlsafe_b64encode(json_payload)

    signature = hmac.new('APP_SECRET', encoded_json, hashlib.sha256).digest()
    encoded_signature = urlsafe_b64encode(signature)

    return '.'.join((encoded_signature, encoded_json))
