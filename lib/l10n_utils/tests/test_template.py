# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.template import TemplateDoesNotExist
from django.test import RequestFactory, override_settings

from django_jinja.backend import Jinja2
from jinja2.nodes import Block
from mock import patch, ANY, Mock
from pathlib import Path
from pyquery import PyQuery as pq
import pytest

from lib.l10n_utils import render
from bedrock.mozorg.tests import TestCase


ROOT_PATH = Path(__file__).with_name('test_files')
ROOT = str(ROOT_PATH)
TEMPLATE_DIRS = [str(ROOT_PATH.joinpath('templates'))]
jinja_env = Jinja2.get_default().env


class TestL10nBlocks(TestCase):
    def test_l10n_block_locales(self):
        """
        Parsing an l10n block with locales info should put that info
        on the node.
        """
        tree = jinja_env.parse("""{% l10n dude locales=ru,es-ES,fr 20121212 %}
                                    This stuff is totally translated.
                                  {% endl10n %}""")
        l10n_block = tree.find(Block)
        self.assertEqual(l10n_block.locales, ['ru', 'es-ES', 'fr'])
        self.assertEqual(l10n_block.version, 20121212)


@patch.object(jinja_env.loader, 'searchpath', TEMPLATE_DIRS)
@override_settings(
    ROOT=ROOT,
    ROOT_URLCONF='lib.l10n_utils.tests.test_files.urls',
)
class TestTransBlocks(TestCase):

    def test_trans_block_works(self):
        """ Sanity check to make sure translations work at all. """
        response = self.client.get('/de/trans-block-reload-test/')
        doc = pq(response.content)
        gettext_call = doc('h1')
        trans_block = doc('p')
        assert gettext_call.text() == 'Die Lage von Mozilla'
        assert trans_block.text().startswith('Mozillas Vision des Internets ist')

    def test_trans_block_works_reload(self):
        """
        Translation should work after a reload.

        bug 808580
        """
        self.test_trans_block_works()
        self.test_trans_block_works()


@patch.object(jinja_env.loader, 'searchpath', TEMPLATE_DIRS)
@override_settings(
    ROOT=ROOT,
    ROOT_URLCONF='lib.l10n_utils.tests.test_files.urls',
)
class TestTemplateLangFiles(TestCase):

    def test_added_lang_files(self):
        """
        Lang files specified in the template should be added to the defaults.
        """
        template = jinja_env.get_template('some_lang_files.html')
        # make a dummy object capable of having arbitrary attrs assigned
        request = type('request', (), {})()
        template.render({'request': request})
        assert request.langfiles == [
            'dude', 'walter', 'navigation', 'download_button', 'main', 'footer']

    @pytest.mark.skip(
        reason='does not pick up the files from the parent. captured in '
        'bug 797984.')
    def test_added_lang_files_inheritance(self):
        """
        Lang files specified in the template should be added to the defaults
        and any specified in parent templates.
        """
        # TODO fix this. it is broken. hence the skip.
        template = jinja_env.get_template('even_more_lang_files.html')
        # make a dummy object capable of having arbitrary attrs assigned
        request = type('request', (), {})()
        template.render(request=request)
        assert request.langfiles == [
            'donnie', 'smokey', 'jesus', 'dude', 'walter', 'main',
            'download_button']

    @patch('lib.l10n_utils.settings.DEV', True)
    @patch('lib.l10n_utils.templatetags.helpers.translate')
    def test_lang_files_order(self, translate):
        """
        Lang files should be queried in order they appear in the file,
        excluding defaults and then the defaults.
        """
        self.client.get('/de/some-lang-files/')
        translate.assert_called_with(ANY, ['dude', 'walter', 'some_lang_files',
                                           'navigation', 'download_button', 'main', 'footer'])

    @patch('lib.l10n_utils.settings.DEV', True)
    @patch('lib.l10n_utils.templatetags.helpers.translate')
    def test_lang_files_default_order(self, translate):
        """
        The template-specific lang file should come before the defaults.
        """
        self.client.get('/de/active-de-lang-file/')
        translate.assert_called_with(ANY, ['inactive_de_lang_file', 'active_de_lang_file',
                                           'navigation', 'download_button', 'main', 'footer'])


class TestNoLocale(TestCase):
    @patch('lib.l10n_utils.get_l10n_path')
    @patch('lib.l10n_utils.django_render')
    def test_render_no_locale(self, django_render, get_l10n_path):
        # Our render method doesn't blow up if the request has no .locale
        # (can happen on 500 error path, for example)
        get_l10n_path.return_value = None
        request = Mock(spec=object)
        # Note: no .locale on request
        # Should not cause an exception
        render(request, '500.html')


@patch.object(jinja_env.loader, 'searchpath', TEMPLATE_DIRS)
@patch('lib.l10n_utils.django_render')
class TestLocaleTemplates(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_enUS_render(self, django_render):
        """
        en-US requests without l10n or locale template should render the
        originally requested template.
        """
        django_render.side_effect = [TemplateDoesNotExist(''), TemplateDoesNotExist(''), True]
        request = self.rf.get('/')
        request.locale = 'en-US'
        render(request, 'firefox/new.html', {'active_locales': ['en-US']})
        django_render.assert_called_with(request, 'firefox/new.html', ANY)

    def test_bedrock_enUS_render(self, django_render):
        """
        en-US requests with a locale-specific template should render the
        locale-specific template.
        """
        django_render.side_effect = [TemplateDoesNotExist(''), True]
        request = self.rf.get('/')
        request.locale = 'en-US'
        render(request, 'firefox/new.html', {'active_locales': ['en-US']})
        django_render.assert_called_with(request, 'firefox/new.en-US.html', ANY)

    def test_enUS_l10n_render(self, django_render):
        """
        en-US requests with an l10n template should render the l10n template.
        """
        request = self.rf.get('/')
        request.locale = 'en-US'
        render(request, 'firefox/new.html', {'active_locales': ['en-US']})
        django_render.assert_called_with(request, 'en-US/templates/firefox/new.html', ANY)

    def test_default_render(self, django_render):
        """
        Non en-US requests without l10n or locale template should render the
        originally requested template.
        """
        django_render.side_effect = [TemplateDoesNotExist(''), TemplateDoesNotExist(''), True]
        request = self.rf.get('/')
        request.locale = 'de'
        render(request, 'firefox/new.html', {'active_locales': ['de']})
        django_render.assert_called_with(request, 'firefox/new.html', ANY)

    def test_bedrock_locale_render(self, django_render):
        """
        Non en-US requests with a locale-specific template should render the
        locale-specific template.
        """
        django_render.side_effect = [TemplateDoesNotExist(''), True]
        request = self.rf.get('/')
        request.locale = 'es-ES'
        render(request, 'firefox/new.html', {'active_locales': ['es-ES']})
        django_render.assert_called_with(request, 'firefox/new.es-ES.html', ANY)

    def test_l10n_render(self, django_render):
        """
        Non en-US requests with an l10n template should render the l10n
        template.
        """
        request = self.rf.get('/')
        request.locale = 'es-ES'
        render(request, 'firefox/new.html', {'active_locales': ['es-ES']})
        django_render.assert_called_with(request, 'es-ES/templates/firefox/new.html', ANY)
