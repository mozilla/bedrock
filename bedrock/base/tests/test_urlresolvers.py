# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from bedrock.base.urlresolvers import find_supported, reverse, split_path, Prefixer
from mock import patch, Mock
from nose.tools import eq_


# split_path tests use a test generator, which cannot be used inside of a
# TestCase class
def test_split_path():
    testcases = [
        # Basic
        ('en-US/some/action', ('en-US', 'some/action')),
        # First slash doesn't matter
        ('/en-US/some/action', ('en-US', 'some/action')),
        # Nor does capitalization
        ('En-uS/some/action', ('en-US', 'some/action')),
        # Unsupported languages return a blank language
        ('unsupported/some/action', ('', 'unsupported/some/action')),
    ]

    for tc in testcases:
        yield check_split_path, tc[0], tc[1]


def check_split_path(path, result):
    res = split_path(path)
    eq_(res, result)


# Test urlpatterns
urlpatterns = patterns('',
    url(r'^test/$', lambda r: None, name='test.view')
)


class FakePrefixer(object):
    def __init__(self, fix):
        self.fix = fix


@patch('bedrock.base.urlresolvers.get_url_prefix')
class TestReverse(TestCase):
    urls = 'bedrock.base.tests.test_urlresolvers'

    def test_unicode_url(self, get_url_prefix):
        # If the prefixer returns a unicode URL it should be escaped and cast
        # as a str object.
        get_url_prefix.return_value = FakePrefixer(lambda p: u'/Françoi%s' % p)
        result = reverse('test.view')

        # Ensure that UTF-8 characters are escaped properly.
        self.assertEqual(result, '/Fran%C3%A7oi/test/')
        self.assertEqual(type(result), str)


class TestPrefixer(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(LANGUAGE_CODE='en-US')
    def test_get_language_default_language_code(self):
        """
        Should return default set by settings.LANGUAGE_CODE if no 'lang'
        url parameter and no Accept-Language header
        """
        request = self.factory.get('/')
        self.assertFalse('lang' in request.GET)
        self.assertFalse(request.META.get('HTTP_ACCEPT_LANGUAGE'))
        prefixer = Prefixer(request)
        eq_(prefixer.get_language(), 'en-US')

    def test_get_language_returns_best(self):
        """
        Should pass Accept-Language header value to get_best_language
        and return result
        """
        request = self.factory.get('/')
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'de, es'
        prefixer = Prefixer(request)
        prefixer.get_best_language = Mock(return_value='de')
        eq_(prefixer.get_language(), 'de')
        prefixer.get_best_language.assert_called_once_with('de, es')

    @override_settings(LANGUAGE_CODE='en-US')
    def test_get_language_no_best(self):
        """
        Should return default set by settings.LANGUAGE_CODE if
        get_best_language return value is None
        """
        request = self.factory.get('/')
        request.META['HTTP_ACCEPT_LANGUAGE'] = 'de, es'
        prefixer = Prefixer(request)
        prefixer.get_best_language = Mock(return_value=None)
        eq_(prefixer.get_language(), 'en-US')
        prefixer.get_best_language.assert_called_once_with('de, es')

    @override_settings(LANGUAGE_URL_MAP={'en-us': 'en-US', 'de': 'de'})
    def test_get_best_language_exact_match(self):
        """
        Should return exact match if it is in settings.LANGUAGE_URL_MAP
        """
        request = self.factory.get('/')
        prefixer = Prefixer(request)
        eq_(prefixer.get_best_language('de, es'), 'de')

    @override_settings(LANGUAGE_URL_MAP={'en-gb': 'en-GB', 'en-us': 'en-US', 'es-ar': 'es-AR'},
                       CANONICAL_LOCALES={'es': 'es-ES', 'en': 'en-US'})
    def test_get_best_language_prefix_match(self):
        """
        Should return a language with a matching prefix from
        settings.LANGUAGE_URL_MAP + settings.CANONICAL_LOCALES if it exists but
        no exact match does
        """
        request = self.factory.get('/')
        prefixer = Prefixer(request)
        eq_(prefixer.get_best_language('en'), 'en-US')
        eq_(prefixer.get_best_language('en-CA'), 'en-US')
        eq_(prefixer.get_best_language('en-GB'), 'en-GB')
        eq_(prefixer.get_best_language('en-US'), 'en-US')
        eq_(prefixer.get_best_language('es'), 'es-ES')
        eq_(prefixer.get_best_language('es-AR'), 'es-AR')
        eq_(prefixer.get_best_language('es-CL'), 'es-ES')
        eq_(prefixer.get_best_language('es-MX'), 'es-ES')

    @override_settings(LANGUAGE_URL_MAP={'en-us': 'en-US'})
    def test_get_best_language_no_match(self):
        """
        Should return None if there is no exact match or matching
        prefix
        """
        request = self.factory.get('/')
        prefixer = Prefixer(request)
        eq_(prefixer.get_best_language('de'), None)

    @override_settings(LANGUAGE_URL_MAP={'en-us': 'en-US'})
    def test_get_best_language_handles_parse_accept_lang_header_error(self):
        """
        Should return None despite error raised by bug described in
        https://code.djangoproject.com/ticket/21078
        """
        request = self.factory.get('/')
        prefixer = Prefixer(request)
        eq_(prefixer.get_best_language('en; q=1,'), None)

    @override_settings(LANGUAGE_URL_MAP={'en-ar': 'en-AR', 'en-gb': 'en-GB', 'en-us': 'en-US'},
                       CANONICAL_LOCALES={'en': 'en-US'})
    def test_prefixer_with_non_supported_locale(self):
        """
        Should set prefixer.locale to a supported locale that repects CANONICAL_LOCALES
        when given a URL with a non-supported locale.
        """
        request = self.factory.get('/en-CA/')
        prefixer = Prefixer(request)
        assert prefixer.locale == 'en-US'


@override_settings(LANGUAGE_URL_MAP={'es-ar': 'es-AR', 'en-gb': 'en-GB', 'es-us': 'es-US'},
                   CANONICAL_LOCALES={'es': 'es-ES', 'en': 'en-US'})
class TestFindSupported(TestCase):
    def test_find_supported(self):
        assert find_supported('en-CA') == 'en-US'
        assert find_supported('en-US') == 'en-US'
        assert find_supported('en-GB') == 'en-GB'
        assert find_supported('en') == 'en-US'
        assert find_supported('es-MX') == 'es-ES'
        assert find_supported('es-AR') == 'es-AR'
        assert find_supported('es') == 'es-ES'

    def test_find_supported_none(self):
        """
        Should return None if it can't find any supported locale.
        """
        assert find_supported('de') is None
        assert find_supported('fr') is None
        assert find_supported('dude') is None
