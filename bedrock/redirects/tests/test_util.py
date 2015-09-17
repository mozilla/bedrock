# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import RegexURLPattern
from django.test import TestCase
from django.test.client import RequestFactory

from mock import patch
from nose.tools import eq_, ok_

from bedrock.redirects.middleware import RedirectsMiddleware
from bedrock.redirects.util import get_resolver, header_redirector, redirect, ua_redirector


class TestHeaderRedirector(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_header_redirects(self):
        callback = header_redirector('user-agent', 'dude', '/abide/', '/flout/')
        url = callback(self.rf.get('/take/comfort/', HTTP_USER_AGENT='the dude browses'))
        self.assertEqual(url, '/abide/')

    def test_ua_redirector(self):
        callback = ua_redirector('dude', '/abide/', '/flout/')
        url = callback(self.rf.get('/take/comfort/', HTTP_USER_AGENT='the dude browses'))
        self.assertEqual(url, '/abide/')

    def test_header_redirects_case_sensitive(self):
        callback = header_redirector('user-agent', 'dude', '/abide/', '/flout/',
                                     case_sensitive=True)
        url = callback(self.rf.get('/take/comfort/', HTTP_USER_AGENT='The Dude Browses'))
        self.assertEqual(url, '/flout/')


class TestRedirectUrlPattern(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_name(self):
        """
        Should return a RegexURLPattern with a matching name attribute
        """
        url_pattern = redirect(r'^the/dude$', 'abides', name='Lebowski')
        ok_(isinstance(url_pattern, RegexURLPattern))
        eq_(url_pattern.name, 'Lebowski')

    def test_no_query(self):
        """
        Should return a 301 redirect
        """
        pattern = redirect(r'^the/dude$', 'abides')
        request = self.rf.get('the/dude')
        response = pattern.callback(request)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'abides')

    def test_preserve_query(self):
        """
        Should preserve querys from the original request by default
        """
        pattern = redirect(r'^the/dude$', 'abides')
        request = self.rf.get('the/dude?aggression=not_stand')
        response = pattern.callback(request)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'abides?aggression=not_stand')

    def test_replace_query(self):
        """
        Should replace query params if any are provided
        """
        pattern = redirect(r'^the/dude$', 'abides',
                           query={'aggression': 'not_stand'})
        request = self.rf.get('the/dude?aggression=unchecked')
        response = pattern.callback(request)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'abides?aggression=not_stand')

    def test_empty_query(self):
        """
        Should strip query params if called with empty query
        """
        pattern = redirect(r'^the/dude$', 'abides', query={})
        request = self.rf.get('the/dude?white=russian')
        response = pattern.callback(request)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'abides')

    def test_temporary_redirect(self):
        """
        Should use a temporary redirect (status code 302) if permanent == False
        """
        pattern = redirect(r'^the/dude$', 'abides', permanent=False)
        request = self.rf.get('the/dude')
        response = pattern.callback(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], 'abides')

    def test_anchor(self):
        """
        Should append anchor text to the end, including after any querystring
        """
        pattern = redirect(r'^the/dude$', 'abides', anchor='toe')
        request = self.rf.get('the/dude?want=a')
        response = pattern.callback(request)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'abides?want=a#toe')

    def test_callable(self):
        """
        Should use the return value of the callable as redirect location
        """
        def opinion(request):
            return '/just/your/opinion/man'

        pattern = redirect(r'^the/dude$', opinion)
        request = self.rf.get('the/dude')
        response = pattern.callback(request)
        eq_(response.status_code, 301)
        eq_(response['Location'], '/just/your/opinion/man')

    @patch('bedrock.redirects.util.reverse')
    def test_to_view(self, mock_reverse):
        """
        Should use return value of reverse as redirect location
        """
        mock_reverse.return_value = '/just/your/opinion/man'
        pattern = redirect(r'^the/dude$', 'yeah.well.you.know.thats')
        request = self.rf.get('the/dude')
        response = pattern.callback(request)
        mock_reverse.assert_called_with('yeah.well.you.know.thats')
        eq_(response.status_code, 301)
        eq_(response['Location'], '/just/your/opinion/man')

    def test_cache_headers(self):
        """
        Should add cache headers based on argument.
        """
        pattern = redirect(r'^the/dude$', 'abides', cache_timeout=2)
        request = self.rf.get('the/dude')
        response = pattern.callback(request)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'abides')
        eq_(response['cache-control'], 'max-age=7200')  # 2 hours

    def test_vary_header(self):
        """
        Should add vary header based on argument.
        """
        pattern = redirect(r'^the/dude$', 'abides', vary='User-Agent')
        request = self.rf.get('the/dude')
        response = pattern.callback(request)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'abides')
        eq_(response['Vary'], 'User-Agent')

    def test_value_capture_and_substitution(self):
        """
        Should be able to capture info from URL and use in redirection.
        """
        resolver = get_resolver([redirect(r'^iam/the/(?P<name>.+)/$', '/donnie/the/{name}/')])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/iam/the/walrus/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/donnie/the/walrus/')

    def test_locale_value_capture(self):
        """
        Should get locale value in kwargs.
        """
        resolver = get_resolver([redirect(r'^iam/the/(?P<name>.+)/$',
                                          '/{locale}donnie/the/{name}/')])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/pt-BR/iam/the/walrus/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/pt-BR/donnie/the/walrus/')

    def test_locale_value_capture_no_locale(self):
        """
        Should get locale value in kwargs and not break if no locale in URL.
        """
        resolver = get_resolver([redirect(r'^iam/the/(?P<name>.+)/$',
                                          '/{locale}donnie/the/{name}/')])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/iam/the/walrus/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/donnie/the/walrus/')

    def test_no_locale_prefix(self):
        """
        Should be able to define a redirect that ignores locale prefix.

        Also when not using any named captures (like implied locale) unnamed
        captures should work. For some reason Django only allows unnamed captures
        to pass through if there are no named ones.
        """
        resolver = get_resolver([redirect(r'^iam/the/(.+)/$', '/donnie/the/{}/',
                                          locale_prefix=False)])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/iam/the/walrus/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/donnie/the/walrus/')

    def test_empty_unnamed_captures(self):
        """
        Should be able to define an optional unnamed capture.
        """
        resolver = get_resolver([redirect(r'^iam/the(/.+)?/$', '/donnie/the{}/',
                                          locale_prefix=False)])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/iam/the/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/donnie/the/')
