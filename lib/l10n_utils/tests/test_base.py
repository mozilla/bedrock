import os

from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_jinja.backend import Jinja2
from mock import ANY, patch

from lib import l10n_utils


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')
TEMPLATE_DIRS = (os.path.join(ROOT, 'templates'),)
jinja_env = Jinja2.get_default()


@patch.object(jinja_env.env.loader, 'searchpath', TEMPLATE_DIRS)
@override_settings(
    ROOT=ROOT,
    DEV=False,
    ROOT_URLCONF='lib.l10n_utils.tests.test_files.urls',
)
class TestRender(TestCase):

    def _test(self, path, template, locale, accept_lang, status, destination=None,
              active_locales=None, add_active_locales=None):
        request = RequestFactory().get(path)
        request.META['HTTP_ACCEPT_LANGUAGE'] = accept_lang
        request.locale = locale
        ctx = {}
        if active_locales:
            ctx['active_locales'] = active_locales

        if add_active_locales:
            ctx['add_active_locales'] = add_active_locales

        response = l10n_utils.render(request, template, ctx)

        if status == 302:
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['Location'], destination)
            self.assertEqual(response['Vary'], 'Accept-Language')
        else:
            self.assertEqual(response.status_code, 200)

    def test_firefox(self):
        path = '/firefox/new/'
        template = 'firefox/new.html'
        locales = ['en-US', 'en-GB', 'fr', 'es-ES']

        # Nothing to do with a valid locale
        self._test(path, template, 'en-US', 'en-us,en;q=0.5',
                   200, active_locales=locales)
        # en-GB is activated on /firefox/new/
        self._test(path, template, 'en-GB', 'en-gb,en;q=0.5',
                   200, active_locales=locales)

        # fr-FR should be treated as fr
        self._test(path, template, 'fr-FR', 'fr-fr',
                   302, '/fr/firefox/new/', active_locales=locales)

        # Should fallback to the user's second preferred language
        self._test(path, template, 'zu', 'zu,fr;q=0.7,en;q=0.3',
                   302, '/fr/firefox/new/', active_locales=locales)

        # Should fallback to one of the site's fallback languages
        self._test(path, template, 'es-CL', 'es-CL,es;q=0.7,en;q=0.3',
                   302, '/es-ES/firefox/new/', active_locales=locales)

    @patch.object(l10n_utils, 'translations_for_template')
    def test_add_active_locales(self, tft_mock):
        path = '/firefox/new/'
        template = 'firefox/new.html'
        locales = ['en-US', 'en-GB']
        tft_mock.return_value = ['fr', 'es-ES']
        # expect same results as above, but with locales from different sources

        # Nothing to do with a valid locale
        self._test(path, template, 'en-US', 'en-us,en;q=0.5',
                   200, add_active_locales=locales)
        # en-GB is activated on /firefox/new/
        self._test(path, template, 'en-GB', 'en-gb,en;q=0.5',
                   200, add_active_locales=locales)

        # fr-FR should be treated as fr
        self._test(path, template, 'fr-FR', 'fr-fr',
                   302, '/fr/firefox/new/', add_active_locales=locales)

        # Should fallback to the user's second preferred language
        self._test(path, template, 'zu', 'zu,fr;q=0.7,en;q=0.3',
                   302, '/fr/firefox/new/', add_active_locales=locales)

        # Should fallback to one of the site's fallback languages
        self._test(path, template, 'es-CL', 'es-CL,es;q=0.7,en;q=0.3',
                   302, '/es-ES/firefox/new/', add_active_locales=locales)

    def test_ftl_files_unmodified(self):
        """A list passed to the ftl_files parameter should not be modified in place"""
        ftl_files = ['dude', 'walter']
        path = '/firefox/new/'
        template = 'firefox/new.html'
        req = RequestFactory().get(path)
        l10n_utils.render(req, template, ftl_files=ftl_files)
        assert ftl_files == ['dude', 'walter']


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


@patch.object(l10n_utils, 'render')
class TestL10nTemplateView(TestCase):
    def setUp(self):
        self.req = RequestFactory().get('/')

    def test_ftl_files(self, render_mock):
        view = l10n_utils.L10nTemplateView.as_view(template_name='dude.html',
                                                   ftl_files='dude')
        view(self.req)
        render_mock.assert_called_with(self.req, ['dude.html'], ANY, ftl_files='dude', ftl_activations=None)

    def test_ftl_files_map(self, render_mock):
        view = l10n_utils.L10nTemplateView.as_view(template_name='dude.html',
                                                   ftl_files_map={'dude.html': 'dude'})
        view(self.req)
        render_mock.assert_called_with(self.req, ['dude.html'], ANY, ftl_files='dude', ftl_activations=None)
        # no match means no FTL files
        view = l10n_utils.L10nTemplateView.as_view(template_name='dude.html',
                                                   ftl_files_map={'donny.html': 'donny'})
        view(self.req)
        render_mock.assert_called_with(self.req, ['dude.html'], ANY, ftl_files=None, ftl_activations=None)

    def test_ftl_activations(self, render_mock):
        view = l10n_utils.L10nTemplateView.as_view(template_name='dude.html',
                                                   ftl_files='dude',
                                                   ftl_activations=['dude', 'donny'])
        view(self.req)
        render_mock.assert_called_with(self.req, ['dude.html'], ANY, ftl_files='dude',
                                       ftl_activations=['dude', 'donny'])
