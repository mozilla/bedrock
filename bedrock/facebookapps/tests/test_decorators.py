# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib

from django.conf import settings
from django.http import QueryDict
from django.test import RequestFactory

from mock import patch
from nose.tools import eq_, ok_

from bedrock.facebookapps import tests
from bedrock.facebookapps.tests import views as test_views


def create_response(view, locale='en_US', remove_locale=False, get=None,
                    app_data=None):
    payload = tests.create_payload(locale=locale, app_data=app_data)
    if remove_locale:
        del payload['user']['locale']

    request_factory = RequestFactory()
    request = request_factory.post(tests.DUMMY_PATH,
        {'signed_request': tests.create_signed_request(payload)})
    if get:
        query_dict = QueryDict('').copy()
        query_dict.update(get)
        request.GET = query_dict

    return view(request), request


@patch.object(settings, 'FACEBOOK_LOCALES', ['en-US', 'es-ES'])
class TestFacebookLocale(tests.TestCase):
    def _locale_url(self, locale):
        return '/{locale}{path}'.format(locale=locale.lower(),
            path=tests.DUMMY_PATH)

    def _create_response(self, *args, **kwargs):
        return create_response(*args, **kwargs)[0]

    def assert_response_unchanged(self, response, content=tests.DUMMY_CONTENT):
        eq_(response.status_code, 200)
        eq_(response.content, content)

    def test_empty_locale(self):
        """
        Leave request unchanged if locale isn't present in signed_request.
        """
        response = self._create_response(test_views.dummy_locale_view,
            remove_locale=True)
        self.assert_response_unchanged(response)

    def test_unsupported_locale(self):
        """
        Leave request unchanged if using an unsupported locale.
        """
        with self.activate('en-US'):
            response = self._create_response(test_views.dummy_locale_view,
                locale='ar_LB')
            self.assert_response_unchanged(response)

    def test_already_using_locale(self):
        """
        Leave request unchanged if already using the Facebook locale.
        """
        with self.activate('en-US'):
            response = self._create_response(test_views.dummy_locale_view,
                locale='en_US')
            self.assert_response_unchanged(response)

    def test_not_using_locale(self):
        """
        Redirect to Facebook locale URL if not already using that locale.
        """
        with self.activate('en-US'):
            response = self._create_response(test_views.dummy_locale_view,
                locale='es_ES')
            self.assert_response_redirect(response, self._locale_url('es-es'))

    def test_preserve_get_parameters(self):
        """
        Send GET query string through to redirect URL.
        """
        with self.activate('en-US'):
            get = tests.DUMMY_DICT
            response = self._create_response(test_views.dummy_locale_view,
                locale='es_ES', get=get)
            encoded_get = urllib.urlencode(get)
            query_string = '?{get}'.format(get=encoded_get)
            ok_(query_string in response['Location'], 'GET parameters {get} '
                'should be present in redirect URL {url}.'.format(get=get,
                    url=response['Location']))


class TestExtractAppData(tests.TestCase):
    def setUp(self):
        self.query_dict = QueryDict('').copy()
        self.app_data = tests.DUMMY_DICT
        self.query_dict.update(self.app_data)

    def test_empty_app_data(self):
        """
        Leave request.GET unchanged if app_data isn't present in
        signed_request.
        """
        response, request = create_response(test_views.dummy_app_data_view)
        self.assertFalse(request.GET, 'GET dict {get} should be empty if there'
            ' isn‘t any app_data.'.format(get=request.GET))

    def test_normal_extraction(self):
        """
        Should place content of app_data in request.GET.
        """
        response, request = create_response(test_views.dummy_app_data_view,
            app_data=self.app_data)
        eq_(request.GET, self.query_dict)

    def test_preserve_old_get(self):
        """
        Preserve previous content of request.GET.
        """
        get = {'foo': 'bar!', 'baz': 'fooz!'}
        self.query_dict.update(get)

        response, request = create_response(test_views.dummy_app_data_view,
            get=get, app_data=self.app_data)
        eq_(request.GET, self.query_dict)
