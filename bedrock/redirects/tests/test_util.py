# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from urlparse import parse_qs, urlparse

from django.conf.urls import RegexURLPattern
from django.test import TestCase
from django.test.client import RequestFactory

from mock import patch
from nose.tools import eq_, ok_

from bedrock.redirects.middleware import RedirectsMiddleware
from bedrock.redirects.util import (get_resolver, header_redirector, is_firefox_redirector,
                                    no_redirect, redirect, ua_redirector, platform_redirector)


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


class TestIsFirefoxRedirector(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_firefox_redirects(self):
        callback = is_firefox_redirector('/abide/', '/flout/')
        url = callback(self.rf.get('/take/comfort/', HTTP_USER_AGENT='Mozilla Firefox/42.0'))
        self.assertEqual(url, '/abide/')

    def test_non_firefox_redirects(self):
        callback = is_firefox_redirector('/abide/', '/flout/')
        url = callback(self.rf.get('/take/comfort/',
                                   HTTP_USER_AGENT='Mozilla Firefox/17.0 Iceweasel/17.0.1'))
        self.assertEqual(url, '/flout/')


class TestPlatformRedirector(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_desktop_redirects(self):
        callback = platform_redirector('/red/', '/green/', '/blue/')
        url = callback(self.rf.get('/take/comfort/',
                                   HTTP_USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; '
                                                   'rv:53.0) Gecko/20100101 Firefox/53.0'))
        self.assertEqual(url, '/red/')

    def test_android_redirects(self):
        callback = platform_redirector('/red/', '/green/', '/blue/')
        url = callback(self.rf.get('/take/comfort/',
                                   HTTP_USER_AGENT='Mozilla/5.0 (Android 6.0.1; Mobile; rv:51.0) '
                                                   'Gecko/51.0 Firefox/51.0'))
        self.assertEqual(url, '/green/')

    def test_ios_redirects(self):
        callback = platform_redirector('/red/', '/green/', '/blue/')
        url = callback(self.rf.get('/take/comfort/',
                                   HTTP_USER_AGENT='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like '
                                                   'Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, '
                                                   'like Gecko) Mobile/8F190'))
        self.assertEqual(url, '/blue/')


class TestNoRedirectUrlPattern(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_no_redirect(self):
        """Should be able to skip redirects."""
        resolver = get_resolver([
            no_redirect(r'^iam/the/walrus/$'),
            redirect(r'^iam/the/.*/$', '/coo/coo/cachoo/'),
        ])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/iam/the/walrus/'))
        self.assertIsNone(resp)

        # including locale
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/pt-BR/iam/the/walrus/'))
        self.assertIsNone(resp)

        resp = middleware.process_request(self.rf.get('/iam/the/marmot/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/coo/coo/cachoo/')

    def test_match_flags(self):
        """
        Should be able to set regex flags for redirect URL.
        """
        resolver = get_resolver([
            redirect(r'^iam/the/walrus/$', '/coo/coo/cachoo/'),
            no_redirect(r'^iam/the/walrus/$', re_flags='i'),
        ])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/IAm/The/Walrus/'))
        self.assertIsNone(resp)

        # also with locale
        resp = middleware.process_request(self.rf.get('/es-ES/Iam/The/Walrus/'))
        self.assertIsNone(resp)

        # sanity check
        resp = middleware.process_request(self.rf.get('/iam/the/walrus/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/coo/coo/cachoo/')


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

    def test_merge_query(self):
        """
        Should merge query params if requested
        """
        pattern = redirect(r'^the/dude$', 'abides',
                           query={'aggression': 'not_stand'}, merge_query=True)
        request = self.rf.get('the/dude?hates=the-eagles')
        response = pattern.callback(request)
        eq_(response.status_code, 301)
        url = urlparse(response['location'])
        query_dict = parse_qs(url.query)
        self.assertTrue(url.path, 'abides')
        self.assertEqual(query_dict, {'aggression': ['not_stand'], 'hates': ['the-eagles']})

    def test_merge_query_no_url_query(self):
        """
        Should merge query params if requested and no params in URL
        """
        pattern = redirect(r'^the/dude$', 'abides',
                           query={'aggression': 'not_stand'}, merge_query=True)
        request = self.rf.get('the/dude')
        response = pattern.callback(request)
        eq_(response.status_code, 301)
        url = urlparse(response['location'])
        query_dict = parse_qs(url.query)
        self.assertTrue(url.path, 'abides')
        self.assertEqual(query_dict, {'aggression': ['not_stand']})

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
        mock_reverse.assert_called_with('yeah.well.you.know.thats', args=None, kwargs=None)
        eq_(response.status_code, 301)
        eq_(response['Location'], '/just/your/opinion/man')

    @patch('bedrock.redirects.util.reverse')
    def test_to_view_args_kwargs(self, mock_reverse):
        """
        Should call reverse with specified args and/or kwargs.
        """
        mock_reverse.return_value = '/just/your/opinion/man'
        pattern = redirect(r'^the/dude$', 'yeah.well.you.know.thats',
                           to_args=['dude'], to_kwargs={'tapes': 'credence'})
        request = self.rf.get('the/dude')
        response = pattern.callback(request)
        mock_reverse.assert_called_with('yeah.well.you.know.thats',
                                        args=['dude'], kwargs={'tapes': 'credence'})
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
        pattern = redirect(r'^the/dude$', 'abides', vary='Accept-Language')
        request = self.rf.get('the/dude')
        response = pattern.callback(request)
        eq_(response.status_code, 301)
        eq_(response['Location'], 'abides')
        eq_(response['Vary'], 'Accept-Language')

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
        Should prepend locale value automatically.
        """
        resolver = get_resolver([redirect(r'^iam/the/(?P<name>.+)/$',
                                          '/donnie/the/{name}/')])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/pt-BR/iam/the/walrus/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/pt-BR/donnie/the/walrus/')

    def test_locale_value_capture_no_locale(self):
        """
        Should get locale value in kwargs and not break if no locale in URL.
        """
        resolver = get_resolver([redirect(r'^iam/the/(?P<name>.+)/$',
                                          '/donnie/the/{name}/')])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/iam/the/walrus/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/donnie/the/walrus/')

    def test_locale_value_capture_ignore_locale(self):
        """
        Should be able to ignore the original locale.
        """
        resolver = get_resolver([redirect(r'^iam/the/(?P<name>.+)/$',
                                          '/donnie/the/{name}/', prepend_locale=False)])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/zh-TW/iam/the/walrus/'))
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

    def test_match_flags(self):
        """
        Should be able to set regex flags for redirect URL.
        """
        resolver = get_resolver([
            redirect(r'^iam/the/walrus/$', '/coo/coo/cachoo/'),
            redirect(r'^iam/the/walrus/$', '/dammit/donnie/', re_flags='i'),
        ])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/IAm/The/Walrus/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/dammit/donnie/')

        # also with locale
        resp = middleware.process_request(self.rf.get('/es-ES/Iam/The/Walrus/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/es-ES/dammit/donnie/')

        # sanity check
        resp = middleware.process_request(self.rf.get('/iam/the/walrus/'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'], '/coo/coo/cachoo/')

    def test_non_ascii_strip_tags(self):
        """
        Should deal with non-ascii characters when there's a substitution as well as strip tags.

        This is from errors that happened in prod. The following URL caused a 500:

        https://www.mozilla.org/editor/midasdemo/securityprefs.html%3C/span%3E%3C/a%3E%C2%A0

        https://sentry.prod.mozaws.net/marketing/bedrock-prod-eu-west/issues/349078/
        """
        resolver = get_resolver([redirect(r'^editor/(?P<page>.*)$',
                                          'http://www-archive.mozilla.org/editor/{page}')])
        middleware = RedirectsMiddleware(resolver)
        resp = middleware.process_request(self.rf.get('/editor/midasdemo/securityprefs.html'
                                                      '%3C/span%3E%3C/a%3E%C2%A0'))
        eq_(resp.status_code, 301)
        eq_(resp['Location'],
            'http://www-archive.mozilla.org/editor/midasdemo/securityprefs.html%C2%A0')
