# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import RegexURLPattern
from django.test import TestCase
from django.test.client import RequestFactory

from mock import patch
from nose.tools import eq_, ok_

from bedrock.redirects.util import redirect


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
        Should use return value of our locale-aware reverse as redirect location
        """
        mock_reverse.return_value = '/just/your/opinion/man'
        pattern = redirect(r'^the/dude$', 'yeah.well.you.know.thats')
        request = self.rf.get('the/dude')
        response = pattern.callback(request)
        mock_reverse.assert_called_with('yeah.well.you.know.thats')
        eq_(response.status_code, 301)
        eq_(response['Location'], '/just/your/opinion/man')
