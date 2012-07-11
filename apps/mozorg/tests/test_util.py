import unittest

from django.conf import settings
from django.test.client import Client

from mock import patch
from nose.tools import eq_


@patch.object(settings, 'ROOT_URLCONF', 'mozorg.tests.urls')
class TestUrlPatterns(unittest.TestCase):
    def test_redirect(self):
        c = Client()
        response = c.get('/en-US/gloubi-boulga/')
        eq_(response.status_code, 301)
        eq_(response['Location'], 'http://testserver/en-US/mock/view/')

    def test_temporary_redirect(self):
        c = Client()
        response = c.get('/en-US/gloubi-boulga/tmp/')
        eq_(response.status_code, 302)
        eq_(response['Location'], 'http://testserver/en-US/mock/view/')
