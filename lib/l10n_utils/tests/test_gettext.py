import os
from tempfile import TemporaryFile
from textwrap import dedent

from django.conf import settings

from mock import patch
from nose.tools import eq_

from l10n_utils.gettext import langfiles_for_path, parse_python
from mozorg.tests import TestCase


ROOT = os.path.dirname(os.path.abspath(__file__))


class TestParsePython(TestCase):
    def tempfile(self, data):
        tempf = TemporaryFile()
        tempf.write(dedent(data))
        tempf.seek(0)
        return tempf

    @patch('l10n_utils.gettext.codecs')
    def test_new_multiple_lang_files_defined(self, codecs_mock):
        """
        If `LANG_FILES` is defined as a list it should be returned.
        """
        tempf = self.tempfile("""
            from l10n_utils.dotlang import _


            LANG_FILES = ['lebowski', 'dude']

            walter_says = _("Donnie you're outa your element!")
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_python('file/doesnt/matter.py')
        eq_(lang_files, ['lebowski', 'dude'])

    @patch('l10n_utils.gettext.codecs')
    def test_new_multiple_lang_files_multi_line(self, codecs_mock):
        """
        If `LANG_FILES` is defined as a multiline list it should be returned.
        """
        tempf = self.tempfile("""
            from l10n_utils.dotlang import _


            LANG_FILES = [
                'lebowski',
                'dude',
            ]

            walter_says = _("Donnie you're outa your element!")
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_python('file/doesnt/matter.py')
        eq_(lang_files, ['lebowski', 'dude'])

    @patch('l10n_utils.gettext.codecs')
    def test_new_single_lang_file_defined(self, codecs_mock):
        """
        If `LANG_FILES` is defined as a string it should be returned as a
        list of length 1.
        """
        tempf = self.tempfile("""
            from l10n_utils.dotlang import _


            LANG_FILES = 'lebowski'

            walter_says = _("I'm stayin... Finishin' my coffee.")
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_python('file/doesnt/matter.py')
        eq_(lang_files, ['lebowski'])

    @patch('l10n_utils.gettext.codecs')
    def test_no_lang_files_defined(self, codecs_mock):
        """
        If `LANG_FILES` is not defined an empty list should be returned.
        """
        tempf = self.tempfile("""
            from l10n_utils.dotlang import _


            stuff = _('whatnot')
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_python('file/doesnt/matter.py')
        eq_(lang_files, [])


class TestLangfilesForPath(TestCase):
    def test_no_lang_files_defined(self):
        """
        If `LANG_FILES` is not defined a list containing the first item in
        `settings.DOTLANG_FILES` should be returned.
        """
        lang_files = langfiles_for_path('lib/l10n_utils/tests/extract_me.py')
        eq_(lang_files, [settings.DOTLANG_FILES[0]])

    def test_lang_files_defined(self):
        """
        If `LANG_FILES` is defined a list of the values should be returned.
        """
        lang_files = langfiles_for_path(
            'lib/l10n_utils/tests/extract_me_with_langfiles.py')
        eq_(lang_files, ['lebowski', 'dude'])
