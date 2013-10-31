# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.conf import settings
from django.test.utils import override_settings

from mock import ANY, MagicMock, Mock, patch
from nose.tools import eq_, ok_

from lib.l10n_utils.gettext import (_append_to_lang_file, langfiles_for_path,
                                    parse_python, parse_template,
                                    po_msgs, pot_to_langfiles, template_is_active)
from lib.l10n_utils.tests import TempFileMixin
from bedrock.mozorg.tests import TestCase


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')
TEMPLATE_DIRS = (os.path.join(ROOT, 'templates'))
DOTLANG_FILES = ['dude', 'walter', 'donny']

# doing this to keep @patch from passing a new mock
# we don't need to the decorated method.
TRUE_MOCK = Mock()
TRUE_MOCK.return_value = True


class TestTemplateIsActive(TestCase):
    @override_settings(DEV=False)
    @patch('lib.l10n_utils.gettext.parse_template')
    @patch('lib.l10n_utils.gettext.lang_file_is_active')
    @patch('lib.l10n_utils.gettext.cache.get')
    @patch('lib.l10n_utils.gettext.cache.set')
    def test_cache_hit(self, cache_set_mock, cache_get_mock, lang_active_mock,
                       parse_template_mock):
        """Should not call other methods on cache hit."""
        cache_get_mock.return_value = True
        self.assertTrue(template_is_active('the/dude', 'de'))
        cache_get_mock.assert_called_once_with('template_active:de:the/dude')
        self.assertFalse(lang_active_mock.called)
        self.assertFalse(parse_template_mock.called)
        self.assertFalse(cache_set_mock.called)

    @override_settings(DEV=False)
    @patch('lib.l10n_utils.gettext.parse_template')
    @patch('lib.l10n_utils.gettext.lang_file_is_active')
    @patch('lib.l10n_utils.gettext.cache.get')
    @patch('lib.l10n_utils.gettext.cache.set')
    def test_cache_miss(self, cache_set_mock, cache_get_mock, lang_active_mock,
                        parse_template_mock):
        """Should check the files and set the cache on cache miss."""
        cache_get_mock.return_value = None
        lang_active_mock.return_value = True
        self.assertTrue(template_is_active('the/dude', 'de'))
        cache_key = 'template_active:de:the/dude'
        cache_get_mock.assert_called_once_with(cache_key)
        self.assertTrue(lang_active_mock.called)
        self.assertFalse(parse_template_mock.called)
        cache_set_mock.assert_called_once_with(cache_key, True, settings.DOTLANG_CACHE)


class TestPOFiles(TestCase):
    good_messages = [
        [u'Said angrily, loudly, and repeatedly.',
         u'Is this your homework Larry?'],
        [None, u'The Dude minds!'],
    ]

    @override_settings(ROOT=ROOT)
    def test_parse_po(self):
        """Should return correct messages"""
        msgs = po_msgs()
        expected = {
            u'templates/some_lang_files.html': self.good_messages,
            u'templates/firefox/fx.html': [[None, u'Find out if your device '
                                                  u'is supported &nbsp;»']],
        }
        self.assertDictEqual(msgs, expected)

    @override_settings(ROOT=ROOT)
    @patch('lib.l10n_utils.gettext._append_to_lang_file')
    @patch('lib.l10n_utils.gettext.langfiles_for_path')
    def test_po_to_langfiles(self, langfiles_mock, append_mock):
        """Should get the correct messages for the correct langfile."""
        # This should exclude the supported device message from the pot file.
        langfiles_mock.return_value = ['some_lang_files',
                                       'firefox/fx']
        pot_to_langfiles()
        append_mock.assert_called_once_with(ANY, self.good_messages)

    @patch('os.path.exists', TRUE_MOCK)
    @patch('lib.l10n_utils.gettext.codecs')
    def test_append_to_lang_file(self, codecs_mock):
        """Should attempt to write a correctly formatted langfile."""
        _append_to_lang_file('dude.lang', self.good_messages)
        lang_vals = codecs_mock.open.return_value
        lang_vals = lang_vals.__enter__.return_value.write.call_args_list
        lang_vals = [call[0][0] for call in lang_vals]
        expected = [
            u'\n\n# Said angrily, loudly, and repeatedly.\n'
            u';Is this your homework Larry?\nIs this your homework Larry?\n',
            u'\n\n;The Dude minds!\nThe Dude minds!\n',
        ]
        self.assertListEqual(lang_vals, expected)

    @patch('os.makedirs')
    @patch('lib.l10n_utils.gettext.codecs')
    def test_append_to_lang_file_dir_creation(self, codecs_mock, md_mock):
        """Should create dirs if required."""
        path_exists = os.path.join(ROOT, 'locale', 'templates', 'firefox',
                                   'fx.lang')
        path_dir_exists = os.path.join(ROOT, 'locale', 'templates', 'firefox',
                                       'new.lang')
        path_new = os.path.join(ROOT, 'locale', 'de', 'does', 'not',
                                'exist.lang')
        with patch('os.path.dirname') as dn_mock:
            _append_to_lang_file(path_exists, {})
            ok_(not dn_mock.called)

            dn_mock.reset_mock()
            dn_mock.return_value = os.path.join(ROOT, 'locale', 'templates',
                                                'firefox')
            _append_to_lang_file(path_dir_exists, {})
            ok_(dn_mock.called)

        md_mock.reset_mock()
        _append_to_lang_file(path_dir_exists, {})
        ok_(not md_mock.called)

        md_mock.reset_mock()
        _append_to_lang_file(path_new, {})
        ok_(md_mock.called)

    @override_settings(ROOT=ROOT, DOTLANG_FILES=DOTLANG_FILES)
    @patch('lib.l10n_utils.gettext.parse_lang')
    @patch('lib.l10n_utils.gettext.codecs', MagicMock())
    def test_uses_default_lang_files(self, pl_mock):
        """Should use the default files from settings"""
        pl_mock.return_value = {}  # avoid side-effects
        pot_to_langfiles()
        calls = [(('{0}/locale/templates/{1}.lang'.format(ROOT, lf),),
                  {'skip_untranslated': False})
                 for lf in DOTLANG_FILES]
        pl_mock.assert_has_calls(calls)


class TestParseTemplate(TempFileMixin, TestCase):
    @patch('lib.l10n_utils.gettext.codecs')
    def test_single_lang_file_added(self, codecs_mock):
        tempf = self.tempfile("""
            {% add_lang_files "lebowski" %}

            {% block title %}El Dudarino{% endblock %}
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_template('file/doesnt/matter.html')
        eq_(lang_files, ['lebowski'])

    @patch('lib.l10n_utils.gettext.codecs')
    def test_multiple_lang_files_added(self, codecs_mock):
        tempf = self.tempfile("""
            {% add_lang_files "lebowski" "walter" "dude" %}

            {% block title %}El Dudarino{% endblock %}
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_template('file/doesnt/matter.html')
        eq_(lang_files, ['lebowski', 'walter', 'dude'])


class TestParsePython(TempFileMixin, TestCase):
    @patch('lib.l10n_utils.gettext.codecs')
    def test_new_lang_file_defined_list(self, codecs_mock):
        """
        If `LANG_FILES` is defined as a single item list it should be returned.
        """
        tempf = self.tempfile("""
            from lib.l10n_utils.dotlang import _


            LANG_FILES = ['lebowski']

            walter_says = _("Donnie you're outa your element!")
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_python('file/doesnt/matter.py')
        eq_(lang_files, ['lebowski'])

    @patch('lib.l10n_utils.gettext.codecs')
    def test_new_multiple_lang_files_defined_list(self, codecs_mock):
        """
        If `LANG_FILES` is defined as a list it should be returned.
        """
        tempf = self.tempfile("""
            from lib.l10n_utils.dotlang import _


            LANG_FILES = ['lebowski', 'dude']

            walter_says = _("Donnie you're outa your element!")
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_python('file/doesnt/matter.py')
        eq_(lang_files, ['lebowski', 'dude'])

    @patch('lib.l10n_utils.gettext.codecs')
    def test_new_multiple_lang_files_multi_line(self, codecs_mock):
        """
        If `LANG_FILES` is defined as a multiline list it should be returned.
        """
        tempf = self.tempfile("""
            from lib.l10n_utils.dotlang import _


            LANG_FILES = [
                'lebowski',
                'dude',
            ]

            walter_says = _("Donnie you're outa your element!")
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_python('file/doesnt/matter.py')
        eq_(lang_files, ['lebowski', 'dude'])

    @patch('lib.l10n_utils.gettext.codecs')
    def test_new_single_lang_file_defined(self, codecs_mock):
        """
        If `LANG_FILES` is defined as a string it should be returned as a
        list of length 1.
        """
        tempf = self.tempfile("""
            from lib.l10n_utils.dotlang import _


            LANG_FILES = 'lebowski'

            walter_says = _("I'm stayin... Finishin' my coffee.")
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_python('file/doesnt/matter.py')
        eq_(lang_files, ['lebowski'])

    @patch('lib.l10n_utils.gettext.codecs')
    def test_new_single_lang_file_defined_dbl_quote(self, codecs_mock):
        """
        If `LANG_FILES` is defined as a double quoted string it should be
        returned as a list of length 1.
        """
        tempf = self.tempfile("""
            from lib.l10n_utils.dotlang import _


            LANG_FILES = "lebowski"

            walter_says = _("I'm stayin... Finishin' my coffee.")
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_python('file/doesnt/matter.py')
        eq_(lang_files, ['lebowski'])

    @patch('lib.l10n_utils.gettext.codecs')
    def test_no_lang_files_defined(self, codecs_mock):
        """
        If `LANG_FILES` is not defined an empty list should be returned.
        """
        tempf = self.tempfile("""
            from lib.l10n_utils.dotlang import _


            stuff = _('whatnot')
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_python('file/doesnt/matter.py')
        eq_(lang_files, [])


class TestLangfilesForPath(TestCase):
    def test_tmpl_no_lang_files_defined(self):
        """
        If no lang files are set, a lang file name derived from the template
        path should be used.
        """
        lang_files = langfiles_for_path('lib/l10n_utils/tests/test_files/'
                                        'templates/no_lang_files.html')
        eq_(lang_files, ['no_lang_files'])

    def test_templ_lang_files_defined(self):
        """ If lang files are set, they should be returned. """
        lang_files = langfiles_for_path('lib/l10n_utils/tests/test_files/'
                                        'templates/some_lang_files.html')
        eq_(lang_files, ['dude', 'walter', 'main'])

    def test_py_no_lang_files_defined(self):
        """
        If `LANG_FILES` is not defined a list containing the first item in
        `settings.DOTLANG_FILES` should be returned.
        """
        lang_files = langfiles_for_path('lib/l10n_utils/tests/test_files/'
                                        'extract_me.py')
        eq_(lang_files, [settings.DOTLANG_FILES[0]])

    def test_py_lang_files_defined(self):
        """
        If `LANG_FILES` is defined a list of the values should be returned.
        """
        lang_files = langfiles_for_path('lib/l10n_utils/tests/test_files/'
                                        'extract_me_with_langfiles.py')
        eq_(lang_files, ['lebowski', 'dude'])
