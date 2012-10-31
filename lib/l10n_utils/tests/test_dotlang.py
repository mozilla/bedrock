# coding=utf-8

import os

from django.conf import settings
from django.core import mail

from mock import patch
from nose.tools import assert_not_equal, eq_
from tower.management.commands.extract import extract_tower_python

from l10n_utils.dotlang import _, FORMAT_IDENTIFIER_RE, parse, translate
from mozorg.tests import TestCase


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')
LANG_FILES = 'test_file'


class TestDotlang(TestCase):
    def test_parse(self):
        path = os.path.join(ROOT, 'test.lang')
        parsed = parse(path)
        expected = {
            u'Hooray! Your Firefox is up to date.':
                u'F\xe9licitations&nbsp;! '
                u'Votre Firefox a \xe9t\xe9 mis \xe0 jour.',
            u'Your Firefox is out of date.':
                u'Votre Firefox ne semble pas \xe0 jour.'
        }
        eq_(parsed, expected)

    def test_parse_utf8_error(self):
        path = os.path.join(ROOT, 'test_utf8_error.lang')
        parsed = parse(path)
        eq_(len(mail.outbox), 1)
        eq_(mail.outbox[0].subject, '[Django] %s is corrupted' % path)
        expected = {
            u'Update now': u'Niha rojane bike',
            u'Supported Devices': u'C�haz�n pi�tgiriy'
        }
        eq_(parsed, expected)
        mail.outbox = []

    def test_format_identifier_re(self):
        eq_(FORMAT_IDENTIFIER_RE.findall('%s %s'),
            [('%s', ''), ('%s', '')])

        eq_(FORMAT_IDENTIFIER_RE.findall('%(foo_bar)s %s'),
            [('%(foo_bar)s', 'foo_bar'), ('%s', '')])

    @patch.object(settings, 'ROOT', ROOT)
    def test_format_identifier_mismatch(self):
        path = 'format_identifier_mismatch'
        expected = '%(foo)s is the new %s'
        with self.activate('en-US'):
            result = translate(expected, [path])
        eq_(expected, result)
        eq_(len(mail.outbox), 1)
        eq_(mail.outbox[0].subject, '[Django] %s is corrupted' % path)
        mail.outbox = []

    @patch.object(settings, 'ROOT', ROOT)
    def test_format_identifier_order(self):
        """
        Test that the order in which the format identifier appears doesn't
        matter
        """
        path = 'format_identifier_mismatch'
        expected = '%(foo)s is the new %(bar)s'
        with self.activate('en-US'):
            result = translate(expected, [path])
        assert_not_equal(expected, result)
        eq_(len(mail.outbox), 0)

    @patch.object(settings, 'ROOT', ROOT)
    def test_extract_message_tweaks_do_not_break(self):
        """
        Extraction and translation matching should tweak msgids the same.
        """
        clean_string = u'Stuff about many things.'
        dirty_string = u'Stuff\xa0about\r\nmany\t   things.'
        trans_string = u'This is the translation.'

        # extraction
        with open(os.path.join(ROOT, 'extract_me.py')) as pyfile:
            vals = extract_tower_python(pyfile, ['_'], [], {}).next()
        eq_(vals[2], clean_string)

        # translation
        # path won't exist for en-US as there isn't a dir for that
        # in locale.
        result = translate(dirty_string, ['does_not_exist'])
        eq_(result, dirty_string)

        result = translate(dirty_string, ['tweaked_message_translation'])
        eq_(result, trans_string)

    @patch('l10n_utils.dotlang.translate')
    def test_new_lang_files_do_not_modify_settings(self, trans_patch):
        """
        Test to make sure that building the new lang files list does not
        modify `settings.DOTLANG_FILES`.
        """
        old_setting = settings.DOTLANG_FILES[:]
        trans_str = 'Translate me'
        _(trans_str)
        call_lang_files = [LANG_FILES] + settings.DOTLANG_FILES
        trans_patch.assert_called_with(trans_str, call_lang_files)
        eq_(old_setting, settings.DOTLANG_FILES)

    @patch('l10n_utils.dotlang.translate')
    def test_gettext_searches_specified_lang_files(self, trans_patch):
        """
        The `l10n_utils.dotlang._` function should search .lang files
        specified in the module from which it's called before the
        default files.
        """
        # use LANG_FILES global in this module
        global LANG_FILES
        old_lang_files = LANG_FILES

        # test the case when LANG_FILES is a string
        trans_str = 'Translate me'
        _(trans_str)
        call_lang_files = [LANG_FILES] + settings.DOTLANG_FILES
        trans_patch.assert_called_with(trans_str, call_lang_files)

        # test the case when LANG_FILES is a list
        LANG_FILES = ['dude', 'donnie', 'walter']
        _(trans_str)
        call_lang_files = LANG_FILES + settings.DOTLANG_FILES
        trans_patch.assert_called_with(trans_str, call_lang_files)

        # restore original value to avoid test leakage
        LANG_FILES = old_lang_files

    @patch('l10n_utils.dotlang.translate')
    def test_gettext_works_without_extra_lang_files(self, trans_patch):
        """
        The `l10n_utils.dotlang._` function should search the default .lang
        files if no others are specified.
        """
        from l10n_utils.tests.test_files import extract_me

        extract_me.do_translate()
        dirty_string = u'Stuff\xa0about\r\nmany\t   things.'
        trans_patch.assert_called_with(dirty_string, settings.DOTLANG_FILES)

    def test_gettext_str_interpolation(self):
        result = _('The %s %s.', 'dude', 'abides')
        eq_(result, 'The dude abides.')
