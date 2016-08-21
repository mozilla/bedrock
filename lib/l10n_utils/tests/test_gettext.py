# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.conf import settings
from django.core.cache import caches
from django.test.utils import override_settings

from mock import ANY, MagicMock, Mock, patch
from nose.tools import eq_, ok_

from lib.l10n_utils.gettext import (_append_to_lang_file, langfiles_for_path,
                                    parse_python, parse_template,
                                    po_msgs, pot_to_langfiles, template_is_active,
                                    _get_template_tag_set, template_has_tag)
from lib.l10n_utils.tests import TempFileMixin
from bedrock.mozorg.tests import TestCase

cache = caches['l10n']
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')
TEMPLATE_DIRS = (os.path.join(ROOT, 'templates'))
DOTLANG_FILES = ['dude', 'walter', 'donny']

# doing this to keep @patch from passing a new mock
# we don't need to the decorated method.
TRUE_MOCK = Mock()
TRUE_MOCK.return_value = True


@override_settings(DEV=False)
class TestTemplateTagFuncs(TestCase):
    @patch('lib.l10n_utils.gettext._get_template_tag_set')
    @patch('lib.l10n_utils.gettext.cache.get')
    @patch('lib.l10n_utils.gettext.cache.set')
    def test_cache_hit(self, cache_set_mock, cache_get_mock, template_tags_mock):
        """Should not call other methods on cache hit."""
        cache_get_mock.return_value = set(['active'])
        self.assertTrue(template_is_active('the/dude', 'de'))
        cache_get_mock.assert_called_once_with('template_tag_set:the/dude:de')
        self.assertFalse(template_tags_mock.called)
        self.assertFalse(cache_set_mock.called)

    @patch('lib.l10n_utils.gettext._get_template_tag_set')
    @patch('lib.l10n_utils.gettext.cache.get')
    @patch('lib.l10n_utils.gettext.cache.set')
    def test_cache_miss(self, cache_set_mock, cache_get_mock, template_tags_mock):
        """Should check the files and set the cache on cache miss."""
        cache_get_mock.return_value = None
        template_tags_mock.return_value = set(['active'])
        self.assertTrue(template_is_active('the/dude', 'de'))
        cache_key = 'template_tag_set:the/dude:de'
        cache_get_mock.assert_called_once_with(cache_key)
        self.assertTrue(template_tags_mock.called)
        cache_set_mock.assert_called_once_with(cache_key, set(['active']),
                                               settings.DOTLANG_CACHE)

    @patch('lib.l10n_utils.gettext.get_lang_path')
    @patch('lib.l10n_utils.gettext.get_template')
    @patch('lib.l10n_utils.gettext.parse_template')
    @patch('lib.l10n_utils.gettext.lang_file_tag_set')
    def test_get_template_tag_set(self, lang_file_tag_set, parse_template_mock, get_template,
                                  get_lang_path):
        """Should return a unique set of tags from all lang files."""
        parse_template_mock.return_value = ['dude', 'walter']
        lang_file_tag_set.side_effect = [set(['dude', 'donny']),
                                         set(['dude', 'uli', 'bunny']),
                                         set(['walter', 'brandt'])]
        self.assertSetEqual(_get_template_tag_set('stuff', 'es'),
                            set(['dude', 'walter', 'donny', 'uli', 'bunny', 'brandt']))

    @override_settings(LANGUAGE_CODE='en-US')
    def test_template_tag_set_default_locale(self):
        """The default language should always have every tag."""
        ok_(template_has_tag('the_dude', 'en-US', 'active'))


class TestPOFiles(TestCase):
    good_messages = [
        [u'Said angrily, loudly, and repeatedly.',
         u'Is this your homework Larry?'],
        [None, u'The Dude minds!'],
    ]

    @override_settings(ROOT=ROOT)
    def test_parse_po(self):
        """Should return correct messages"""
        msgs = po_msgs('messages')
        expected = {
            u'templates/some_lang_files.html': self.good_messages,
            u'templates/firefox/fx.html': [[None, u'Find out if your device '
                                                  u'is supported &nbsp;»']],
            u'bedrock/firefox/templates/firefox/os/notes-1.3.html': [[
                u'For bug 982755',
                u'The WebIccManager API, which allows support for multiple sim cards, '
                u'has had updates: iccChangeEvent has been added using using event '
                u'generator <a href="%(url1)s">bug 814637</a>'
            ]],
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
        pot_to_langfiles('messages')
        append_mock.assert_called_with(ANY, self.good_messages)

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
    def setUp(self):
        cache.clear()

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
