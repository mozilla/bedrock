import os
import sys
from contextlib import contextmanager
from cStringIO import StringIO
from tempfile import TemporaryFile
from textwrap import dedent

from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_jinja.backend import Jinja2
from mock import patch

from lib import l10n_utils


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')
TEMPLATE_DIRS = (os.path.join(ROOT, 'templates'),)
jinja_env = Jinja2.get_default()


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


@patch.object(jinja_env.env.loader, 'searchpath', TEMPLATE_DIRS)
@override_settings(ROOT=ROOT)
@override_settings(DEV=False)
class TestRender(TestCase):
    urls = 'lib.l10n_utils.tests.test_files.urls'

    def _test(self, path, template, locale, accept_lang, status, destination=None):
        request = RequestFactory().get(path)
        request.META['HTTP_ACCEPT_LANGUAGE'] = accept_lang
        request.locale = locale
        response = l10n_utils.render(request, template)

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
        with patch.object(l10n_utils, 'template_is_active') as active_mock:
            active_mock.return_value = True
            self._test(path, template, 'en-GB', 'en-gb,en;q=0.5',
                       200)

            active_mock.reset_mock()
            active_mock.side_effect = [False, True]
            # fr-FR should be treated as fr
            self._test(path, template, 'fr-FR', 'fr-fr',
                       302, '/fr/firefox/new/')

            active_mock.reset_mock()
            active_mock.side_effect = [False, False, True]
            # Should fallback to the user's second preferred language
            self._test(path, template, 'zu', 'zu,fr;q=0.7,en;q=0.3',
                       302, '/fr/firefox/new/')

            active_mock.reset_mock()
            active_mock.side_effect = [False, False, False, False, True]
            # Should fallback to one of the site's fallback languages
            self._test(path, template, 'es-CL', 'es-CL,es;q=0.7,en;q=0.3',
                       302, '/es-ES/firefox/new/')


class TestGetAcceptLanguages(TestCase):
    def _test(self, accept_lang, list):
        request = RequestFactory().get('/')
        request.META['HTTP_ACCEPT_LANGUAGE'] = accept_lang
        self.assertEqual(l10n_utils.get_accept_languages(request), list)

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
