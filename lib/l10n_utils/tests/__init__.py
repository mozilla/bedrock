import os
import sys
from contextlib import contextmanager
from cStringIO import StringIO
from tempfile import TemporaryFile
from textwrap import dedent

from jingo import env
from jinja2 import FileSystemLoader
from mock import patch
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from l10n_utils import render, get_accept_languages


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')
TEMPLATE_DIRS = (os.path.join(ROOT, 'templates'),)


@contextmanager
def capture_stdio():
    oldout, olderr = sys.stdout, sys.stderr
    newio = [StringIO(), StringIO()]
    sys.stdout, sys.stderr = newio
    yield newio
    sys.stdout, sys.stderr = oldout, olderr
    newio[0] = newio[0].getvalue().rstrip()
    newio[1] = newio[1].getvalue().rstrip()


class TempFileMixin(object):
    """Provide a method for getting a temp file that is removed when closed."""
    def tempfile(self, data=None):
        tempf = TemporaryFile()
        if data:
            tempf.write(dedent(data))
            tempf.seek(0)
        return tempf


@patch.object(env, 'loader', FileSystemLoader(TEMPLATE_DIRS))
@override_settings(ROOT=ROOT)
@override_settings(ROOT_URLCONF='lib.l10n_utils.tests.test_files.urls')
@override_settings(DEV=False)
class TestRender(TestCase):
    def _test(self, path, template, locale, accept_lang, status, destination=None):
        request = RequestFactory().get(path)
        request.META['HTTP_ACCEPT_LANGUAGE'] = accept_lang
        request.locale = locale
        response = render(request, template)

        if status == 302:
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['Location'], destination)
            self.assertEqual(response['Vary'], 'Accept-Language')
        else:
            self.assertEqual(response.status_code, 200)

    def test_firefox(self):
        path = '/firefox/new/'
        template = 'firefox/new.html'

        # Nothing to do with a valid locale
        self._test(path, template, 'en-US', 'en-us,en;q=0.5',
                   200)
        # en-GB is activated on /firefox/new/
        self._test(path, template, 'en-GB', 'en-gb,en;q=0.5',
                   200)
        # fr-FR should be treated as fr
        self._test(path, template, 'fr-FR', 'fr-fr',
                   302, '/fr/firefox/new/')
        # Should fallback to the user's second preferred language
        self._test(path, template, 'zu', 'zu,fr;q=0.7,en;q=0.3',
                   302, '/fr/firefox/new/')


class TestGetAcceptLanguages(TestCase):
    def _test(self, accept_lang, list):
        request = RequestFactory().get('/')
        request.META['HTTP_ACCEPT_LANGUAGE'] = accept_lang
        self.assertEqual(get_accept_languages(request), list)

    def test_valid_lang_codes(self):
        """
        Should return a list of valid lang codes
        """
        self._test('fr-FR', ['fr'])
        self._test('en-us,en;q=0.5', ['en-US', 'en'])
        self._test('pt-pt,fr;q=0.8,it-it;q=0.5,de;q=0.3',
                   ['pt-PT', 'fr', 'it', 'de'])
        self._test('ja-JP-mac,ja-JP;q=0.7,ja;q=0.3', ['ja'])
        self._test('foo,bar;q=0.5', ['foo', 'bar'])

    def test_invalid_lang_codes(self):
        """
        Should return a list of valid lang codes or an empty list
        """
        self._test('', [])
        self._test('en_us,en*;q=0.5', [])
        self._test('Chinese,zh-cn;q=0.5', ['zh-CN'])
