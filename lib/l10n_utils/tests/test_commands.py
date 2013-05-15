# coding: utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import codecs
from os import path
from StringIO import StringIO
from textwrap import dedent

from django.conf import settings
from django.utils import unittest

from mock import ANY, MagicMock, Mock, patch

from lib.l10n_utils.gettext import _append_to_lang_file, merge_lang_files
from lib.l10n_utils.management.commands.l10n_check import (
    get_todays_version,
    L10nParser,
    L10nTemplate,
    list_templates,
    update_templates,
)
from lib.l10n_utils.management.commands.l10n_extract import extract_from_files
from lib.l10n_utils.tests import capture_stdio


ROOT = path.join(path.dirname(path.abspath(__file__)), 'test_files')
TEMPLATE_DIRS = (path.join(ROOT, 'templates'),)

METHODS = [
    ('lib/l10n_utils/tests/test_files/templates/**.html',
     'tower.management.commands.extract.extract_tower_template'),
]


class TestL10nExtract(unittest.TestCase):
    def test_extract_from_files(self):
        """
        Should be able to extract strings from a specific file.
        """
        testfile = ('lib/l10n_utils/tests/test_files/templates/'
                    'even_more_lang_files.html',)
        with capture_stdio() as out:
            extracted = next(extract_from_files(testfile, method_map=METHODS))
        self.assertTupleEqual(extracted,
                              (testfile[0], 9, 'Mark it 8 Dude.', []))
        # test default callback
        self.assertEqual(out[0], '  %s' % testfile)

    def test_extract_from_multiple_files(self):
        """
        Should be able to extract strings from specific files.
        """
        basedir = 'lib/l10n_utils/tests/test_files/templates/'
        testfiles = (
            basedir + 'even_more_lang_files.html',
            basedir + 'some_lang_files.html',
        )
        good_extracts = (
            (testfiles[0], 9, 'Mark it 8 Dude.', []),
            (testfiles[1], 9, 'Is this your homework Larry?', []),
        )
        with capture_stdio() as out:
            for i, extracted in enumerate(
                    extract_from_files(testfiles, method_map=METHODS)):
                self.assertTupleEqual(extracted, good_extracts[i])
        self.assertEqual(out[0], '  %s\n  %s' % testfiles)

    def test_extract_from_files_no_match(self):
        """
        If the file path doesn't match a domain method, it should be skipped.
        """
        testfile = ('bedrock/mozorg/templates/mozorg/home.html',)
        with capture_stdio() as out:
            extracted = next(extract_from_files(testfile, method_map=METHODS),
                             None)
        self.assertIsNone(extracted)
        self.assertEqual(out[0],
                         '! %s does not match any domain methods!' % testfile)

    def test_extract_from_files_no_file(self):
        """
        If the file path doesn't exist, it should be skipped.
        """
        testfile = ('lib/l10n_utils/tests/test_files/templates/'
                    'file_does_not_exist.html',)
        with capture_stdio() as out:
            extracted = next(extract_from_files(testfile, method_map=METHODS),
                             None)
        self.assertIsNone(extracted)
        self.assertEqual(out[0], '! %s does not exist!' % testfile)

    @patch('lib.l10n_utils.management.commands.l10n_extract.extract_from_file')
    def test_extract_from_files_passes_args(self, eff):
        """The correct args should be passed through to extract_from_file"""
        testfile = ('lib/l10n_utils/tests/test_files/templates/'
                    'even_more_lang_files.html',)
        testfile_full = path.join(settings.ROOT, testfile[0])
        next(extract_from_files(testfile, method_map=METHODS), None)
        eff.assert_called_once_with(METHODS[0][1], testfile_full,
                                    keywords=ANY,
                                    comment_tags=ANY,
                                    options=ANY,
                                    strip_comment_tags=ANY)

    def test_extract_from_files_callback_works(self):
        """extract_from_files should call our callback"""
        testfile = ('lib/l10n_utils/tests/test_files/templates/'
                    'even_more_lang_files.html',)
        callback = Mock()
        next(extract_from_files(testfile, callback=callback,
                                method_map=METHODS), None)
        callback.assert_called_once_with(testfile[0], METHODS[0][1], ANY)


class TestL10nCheck(unittest.TestCase):
    def _get_block(self, blocks, name):
        """Out of all blocks, grab the one with the specified name."""
        return next((b for b in blocks if b['name'] == name), None)

    def test_list_templates(self):
        """Make sure we capture both html and txt templates."""
        TEMPLATES = ['mozorg/home.html',
                     'mozorg/emails/other.txt']
        tmpls = [t for t in list_templates()
                 if L10nTemplate(t).rel_path in TEMPLATES]
        assert len(tmpls) == len(TEMPLATES)

    def test_parse_templates(self):
        """Make sure the parser grabs the l10n block content
        correctly."""

        parser = L10nParser()
        blocks = parser.parse("""
            foo bar bizzle what?
            {% l10n baz, 20110914 %}
            mumble
            {% was %}
            wased
            {% endl10n %}
            qux
        """, only_blocks=True)

        baz = self._get_block(blocks, 'baz')

        self.assertEqual(baz['main'], 'mumble')
        self.assertEqual(baz['was'], 'wased')
        self.assertEqual(baz['version'], 20110914)

        blocks = parser.parse("""
            foo bar bizzle what?
            {% l10n baz locales=ru,bn-IN,fr 20110914 %}
            mumble
            {% endl10n %}
            qux
        """, only_blocks=True)

        baz = self._get_block(blocks, 'baz')
        self.assertEqual(baz['main'], 'mumble')
        self.assertEqual(baz['locales'], ['ru', 'bn-IN', 'fr'])
        self.assertEqual(baz['version'], 20110914)

    def test_content_halt(self):
        """Make sure the parser will halt on the content block if told
        to do so."""

        parser = L10nParser()
        content_str = 'foo bar {% block content %}baz{% endblock %} hello'
        last_token = None

        for token in parser.parse(content_str, halt_on_content=True):
            last_token = token

        self.assertEqual(last_token, False)

    def test_filter_blocks(self):
        """Should return a list of blocks appropriate for a given lang"""
        template = L10nTemplate(source="""
            {% l10n dude locales=fr,es-ES,ru 20121212 %}
                This aggression will not stand, man.
            {% endl10n %}
            {% l10n walter, locales=es-ES,ru 20121212 %}
                I'm stayin'. Finishin' my coffee.
            {% endl10n %}
            {% l10n donnie 20121212 %}
                Phone's ringing Dude.
            {% endl10n %}
        """)

        lang_blocks = template.blocks_for_lang('fr')
        self.assertEqual(len(lang_blocks), 2)
        self.assertEqual(lang_blocks[0]['name'], 'dude')
        self.assertEqual(lang_blocks[1]['name'], 'donnie')

        lang_blocks = template.blocks_for_lang('es-ES')
        self.assertEqual(len(lang_blocks), 3)
        self.assertEqual(lang_blocks[0]['name'], 'dude')
        self.assertEqual(lang_blocks[1]['name'], 'walter')
        self.assertEqual(lang_blocks[2]['name'], 'donnie')

        lang_blocks = template.blocks_for_lang('pt-BR')
        self.assertEqual(len(lang_blocks), 1)
        self.assertEqual(lang_blocks[0]['name'], 'donnie')

    @patch('lib.l10n_utils.management.commands.l10n_check.settings.ROOT', ROOT)
    @patch('lib.l10n_utils.management.commands.l10n_check.list_templates')
    @patch('lib.l10n_utils.management.commands.l10n_check.L10nTemplate.copy')
    @patch('lib.l10n_utils.management.commands.l10n_check.L10nTemplate.update')
    def test_process_template(self, update_mock, copy_mock, lt_mock):
        """
        template.process() should update existing templates and create missing
        ones. It should only do so for the right locales.
        """
        lt_mock.return_value = [
            path.join(TEMPLATE_DIRS[0], 'l10n_blocks_with_langs.html'),
            path.join(TEMPLATE_DIRS[0], 'l10n_blocks_without_langs.html'),
        ]
        update_templates(['de'])
        copy_mock.assert_called_once_with('de')
        update_mock.assert_called_once_with('de')

    def test_blocks_called_once(self):
        """
        Test that the cached_property decorator really works in our situation.
        """
        template = L10nTemplate(source="""
            {% l10n donnie 20121212 %}
                Phone's ringing Dude.
            {% endl10n %}
        """)
        with patch.object(template, 'parser') as mock_parser:
            template.blocks
            template.blocks_for_lang('de')
            template.blocks
            self.assertEqual(mock_parser.parse.call_count, 1)

    def test_update_template_no_lang(self):
        """
        template.update() should skip files without blocks for the given locale.
        """
        template = L10nTemplate(path.join(TEMPLATE_DIRS[0],
                                          'l10n_blocks_with_langs.html'))
        # cause the template to be read and parsed before mocking open
        template.blocks
        codecs_open = 'lib.l10n_utils.management.commands.l10n_check.codecs.open'
        open_mock = MagicMock(spec=file)
        with patch(codecs_open, open_mock):
            template.update('zh-TW')
            file_handle = open_mock.return_value.__enter__.return_value
            assert not file_handle.write.called
            template.update('de')
            assert file_handle.write.called

    @patch('lib.l10n_utils.management.commands.l10n_check.settings.ROOT', ROOT)
    def test_update_template(self):
        """
        template.update() should update lang specific templates.
        """
        template = L10nTemplate(path.join(TEMPLATE_DIRS[0],
                                          'l10n_blocks_with_langs.html'))
        # cause the template to be read and parsed before mocking open
        template.blocks
        codecs_open = 'lib.l10n_utils.management.commands.l10n_check.codecs.open'
        open_mock = MagicMock(spec=file)
        open_buffer = StringIO()
        # for writing the new file
        open_mock.return_value.__enter__.return_value = open_buffer
        # for reading the old file
        open_mock().read.return_value = codecs.open(
            template.l10n_path('de')).read()

        with patch(codecs_open, open_mock):
            template.update('de')

        # braces doubled for .format()
        good_value = dedent("""\
            {{# Version: {0} #}}

            {{% extends "l10n_blocks_with_langs.html" %}}

            {{% l10n donnie %}}
            Phone's ringing Dude.
            {{% was %}}
            I am the walrus.
            {{% endl10n %}}\n\n
        """.format(get_todays_version()))
        self.assertEqual(open_buffer.getvalue(), good_value)

    def test_copy_template_no_lang(self):
        """
        template.copy() should skip files with no blocks for the given locale.
        :return:
        """
        template = L10nTemplate(path.join(TEMPLATE_DIRS[0],
                                          'l10n_blocks_with_langs.html'))
        # cause the template to be read and parsed before mocking open
        template.blocks
        codecs_open = 'lib.l10n_utils.management.commands.l10n_check.codecs.open'
        open_mock = MagicMock(spec=file)
        with patch(codecs_open, open_mock):
            template.copy('zh-TW')
            file_handle = open_mock.return_value.__enter__.return_value
            assert not file_handle.write.called
            template.copy('de')
            assert file_handle.write.called

    def test_copy_template(self):
        """
        template.copy() should create missing lang specific templates.
        """
        template = L10nTemplate(path.join(TEMPLATE_DIRS[0],
                                          'l10n_blocks_without_langs.html'))
        # cause the template to be read and parsed before mocking open
        template.blocks
        codecs_open = 'lib.l10n_utils.management.commands.l10n_check.codecs.open'
        open_mock = MagicMock(spec=file)
        open_buffer = StringIO()
        open_mock.return_value.__enter__.return_value = open_buffer
        with patch(codecs_open, open_mock):
            template.copy('de')

        # braces doubled for .format()
        good_value = dedent("""\
            {{# Version: {0} #}}

            {{% extends "l10n_blocks_without_langs.html" %}}

            {{% l10n donnie %}}
            Phone's ringing Dude.
            {{% endl10n %}}\n
        """.format(get_todays_version()))
        self.assertEqual(open_buffer.getvalue(), good_value)


class Testl10nMerge(unittest.TestCase):

    @patch('lib.l10n_utils.gettext.settings.ROOT', ROOT)
    @patch('lib.l10n_utils.gettext._append_to_lang_file')
    def test_merge_lang_files(self, write_mock):
        """
        `merge_lang_files()` should see all strings, not skip the untranslated.
        Bug 861168.
        """
        merge_lang_files(['de'])
        dest_file = path.join(ROOT, 'locale', 'de', 'firefox', 'fx.lang')
        write_mock.assert_called_once_with(dest_file,
                                           [u'Find out if your device is '
                                            u'supported &nbsp;\xbb'])

    @patch('lib.l10n_utils.gettext.codecs.open')
    def test_append_to_lang_file(self, open_mock):
        """
        `_append_to_lang_file()` should append any new messages to a lang file.
        """
        _append_to_lang_file('dude.lang', ['The Dude abides, man.'])
        mock_write = open_mock.return_value.__enter__.return_value.write
        mock_write.assert_called_once_with(u'\n\n;The Dude abides, man.\n'
                                           u'The Dude abides, man.\n')

        # make sure writing multiple strings works.
        mock_write.reset_mock()
        msgs = ['The Dude abides, man.', 'Dammit Walter!']
        _append_to_lang_file('dude.lang', msgs)
        expected = [((u'\n\n;{msg}\n{msg}\n'.format(msg=msg),),)
                    for msg in msgs]
        self.assertEqual(expected, mock_write.call_args_list)

    @patch('lib.l10n_utils.gettext.codecs.open')
    def test_merge_unicode_strings(self, open_mock):
        """
        Bug 869538: Exception when merging unicode.
        """
        mock_write = open_mock.return_value.__enter__.return_value.write
        msgs = [u"Désintéressé et fier de l'être"]
        _append_to_lang_file('dude.lang', msgs)
        mock_write.assert_called_once_with(
            u'\n\n;{msg}\n{msg}\n'.format(msg=msgs[0]))
