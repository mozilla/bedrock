# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from tempfile import TemporaryFile
from textwrap import dedent

from django.conf import settings

from mock import patch
from nose.tools import eq_

from l10n_utils.gettext import langfiles_for_path, parse_python, parse_template
from mozorg.tests import TestCase


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')
TEMPLATE_DIRS = (os.path.join(ROOT, 'templates'))


class TempFileMixin(object):
    """Provide a method for getting a temp file that is removed when closed."""
    def tempfile(self, data):
        tempf = TemporaryFile()
        tempf.write(dedent(data))
        tempf.seek(0)
        return tempf


class TestParseTemplate(TempFileMixin, TestCase):
    @patch('l10n_utils.gettext.codecs')
    def test_single_lang_file_added(self, codecs_mock):
        tempf = self.tempfile("""
            {% add_lang_files "lebowski" %}

            {% block title %}El Dudarino{% endblock %}
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_template('file/doesnt/matter.html')
        eq_(lang_files, ['lebowski'])

    @patch('l10n_utils.gettext.codecs')
    def test_multiple_lang_files_added(self, codecs_mock):
        tempf = self.tempfile("""
            {% add_lang_files "lebowski" "walter" "dude" %}

            {% block title %}El Dudarino{% endblock %}
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_template('file/doesnt/matter.html')
        eq_(lang_files, ['lebowski', 'walter', 'dude'])


class TestParsePython(TempFileMixin, TestCase):
    @patch('l10n_utils.gettext.codecs')
    def test_new_lang_file_defined_list(self, codecs_mock):
        """
        If `LANG_FILES` is defined as a single item list it should be returned.
        """
        tempf = self.tempfile("""
            from l10n_utils.dotlang import _


            LANG_FILES = ['lebowski']

            walter_says = _("Donnie you're outa your element!")
        """)
        codecs_mock.open.return_value = tempf
        lang_files = parse_python('file/doesnt/matter.py')
        eq_(lang_files, ['lebowski'])

    @patch('l10n_utils.gettext.codecs')
    def test_new_multiple_lang_files_defined_list(self, codecs_mock):
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
    def test_new_single_lang_file_defined_dbl_quote(self, codecs_mock):
        """
        If `LANG_FILES` is defined as a double quoted string it should be
        returned as a list of length 1.
        """
        tempf = self.tempfile("""
            from l10n_utils.dotlang import _


            LANG_FILES = "lebowski"

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
        eq_(lang_files, ['dude', 'walter'])

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
