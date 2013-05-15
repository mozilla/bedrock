# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib

from django.conf import settings
from django.utils.translation import get_language

from mock import Mock, patch
from nose.tools import eq_, ok_

from bedrock.facebookapps import utils
from bedrock.facebookapps import tests


DUMMY_FACEBOOK_LOCALES = ['en-GB', 'en-US', 'en', 'es-ES', 'es-MX']


class TestUnwrapSignedRequest(tests.TestCase):
    def setUp(self):
        self.request = Mock(['REQUEST'])
        self.request.REQUEST = {}

    def test_empty_signed_request(self):
        """
        If signed_request isn't set, should return empty dict.
        """
        eq_(utils.unwrap_signed_request(self.request), {})

    def test_change_locale_to_hyphen(self):
        """
        Should convert Facebook's underscore locales to hyphen locales.
        """
        payload = tests.create_payload(locale='en_GB')
        signed_request = tests.create_signed_request(payload)
        self.request.REQUEST['signed_request'] = signed_request
        unwrapped_payload = utils.unwrap_signed_request(self.request)
        eq_(unwrapped_payload['user']['locale'], 'en-GB')

    def test_normal_unwrap(self):
        """
        Should unwrap and return the encoded dictionary.
        """
        payload = tests.create_payload(locale='en_GB')
        signed_request = tests.create_signed_request(payload)
        self.request.REQUEST['signed_request'] = signed_request
        # Use hyphen in payload's locale to match util's transformation
        payload['user']['locale'] = 'en-GB'
        eq_(utils.unwrap_signed_request(self.request), payload)


class TestAppDataQueryStringEncode(tests.TestCase):
    def test_app_data_query_string_encode(self):
        app_data_dict = {
            'foo': 'bar!',
            'baz': 'fooz',
            'scene': 'some-scene',
        }

        query_string = utils.app_data_query_string_encode(app_data_dict)
        eq_(urllib.unquote(query_string), 'app_data[foo]=bar!&'
            'app_data[baz]=fooz&app_data[scene]=some-scene')


@patch.object(settings, 'FACEBOOK_LOCALES', DUMMY_FACEBOOK_LOCALES)
class TestGetBestLocale(tests.TestCase):
    """
    Locales should be compared in lowercase because get_best_locale can return
    lowercase from get_language or the expected lowercase language and upper
    case country, as taken directly from FACEBOOK_LOCALES.
    """
    def setUp(self):
        self.tested_locales = ['en-GB', 'en-ZA', 'es-AR', 'fu-BR']

    def test_supported_locale(self):
        """
        Return the given locale if supported.
        """
        eq_(utils.get_best_locale('en-GB').lower(), 'en-gb')

    def test_locale_for_activated_language(self):
        """
        If the locale isn't supported, try to activate just the language code
        and return the resulting locale if supported.
        """
        eq_(utils.get_best_locale('en-ZA').lower(), 'en')

    def test_first_supported_locale_for_language(self):
        """
        If neither the given locale or the locale resulting from activating the
        language code are supported, iterate through the supported locales and
        return the first one that matches the language.
        """
        eq_(utils.get_best_locale('es-AR').lower(), 'es-es')

    def test_unsupported_locale(self):
        """
        Return the default en-US when locale isn't supported.
        """
        eq_(utils.get_best_locale('ar-LB').lower(), 'en-us')

    def test_always_returns_supported_locale(self):
        """
        Always return a supported locale.
        """
        supported_locales = [locale.lower()
            for locale in settings.FACEBOOK_LOCALES]

        for locale in self.tested_locales:
            best_locale = utils.get_best_locale(locale).lower()
            ok_(best_locale in supported_locales, 'The locale {best} (returned'
                ' for {locale}) is not a supported locale {supported}.'
                .format(locale=locale, best=best_locale,
                    supported=supported_locales))

    def test_locale_remains_unchanged(self):
        """
        Always preserve the active locale.
        """
        lang = 'pt-BR'
        with self.activate(lang):
            for locale in self.tested_locales:
                utils.get_best_locale(locale)
                eq_(get_language().lower(), lang.lower())


class TestJsRedirect(tests.TestCase):
    def setUp(self):
        self.request = Mock(['locale'])
        self.request.locale = 'en-US'
        self.url = 'https://www.mozilla.org/'
        self.response = utils.js_redirect(self.url, self.request)

    def test_js_redirect(self):
        """
        Response should be HTML to be used by JavaScript redirect code.
        """
        self.assert_js_redirect(self.response, self.url)
