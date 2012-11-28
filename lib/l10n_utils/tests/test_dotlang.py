# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import clear_url_caches
from django.test.client import Client

from jingo import env
from jinja2 import FileSystemLoader
from mock import patch
from nose.plugins.skip import SkipTest
from nose.tools import assert_not_equal, eq_, ok_
from pyquery import PyQuery as pq
from tower.management.commands.extract import extract_tower_python

from l10n_utils.dotlang import (_, FORMAT_IDENTIFIER_RE, lang_file_is_active,
                                parse, translate)
from mozorg.tests import TestCase


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')
LANG_FILES = 'test_file'
TEMPLATE_DIRS = (os.path.join(ROOT, 'templates'),)


@patch.object(env, 'loader', FileSystemLoader(TEMPLATE_DIRS))
@patch.object(settings, 'ROOT_URLCONF', 'l10n_utils.tests.test_files.urls')
@patch.object(settings, 'ROOT', ROOT)
class TestLangFilesActivation(TestCase):
    def setUp(self):
        clear_url_caches()
        self.client = Client()

    @patch.object(settings, 'DEV', False)
    def test_lang_file_is_active(self):
        """
        `lang_file_is_active` should return true if lang file has the
        comment, and false otherwise.
        """
        ok_(lang_file_is_active('active_de_lang_file', 'de'))
        ok_(not lang_file_is_active('active_de_lang_file', 'es'))
        ok_(not lang_file_is_active('inactive_de_lang_file', 'de'))
        ok_(not lang_file_is_active('does_not_exist', 'de'))

    @patch.object(settings, 'DEV', False)
    def test_active_locale_not_redirected(self):
        """ Active lang file should render correctly. """
        response = self.client.get('/de/active-de-lang-file/')
        eq_(response.status_code, 200)
        doc = pq(response.content)
        eq_(doc('h1').text(), 'Die Lage von Mozilla')

    @patch.object(settings, 'DEV', False)
    @patch.object(settings, 'LANGUAGE_CODE', 'en-US')
    def test_inactive_locale_redirected(self):
        """ Inactive locale should redirect to en-US. """
        response = self.client.get('/de/inactive-de-lang-file/')
        eq_(response.status_code, 302)
        eq_(response['location'],
            'http://testserver/en-US/inactive-de-lang-file/')
        response = self.client.get('/de/inactive-de-lang-file/', follow=True)
        doc = pq(response.content)
        eq_(doc('h1').text(), 'The State of Mozilla')

    @patch.object(settings, 'DEV', True)
    def test_inactive_locale_not_redirected_dev_true(self):
        """
        Inactive lang file should not redirect in DEV mode.
        """
        # Disabled because of bug 815573
        raise SkipTest
        response = self.client.get('/de/inactive-de-lang-file/')
        eq_(response.status_code, 200)
        doc = pq(response.content)
        eq_(doc('h1').text(), 'Die Lage von Mozilla')


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
        eq_(mail.outbox[0].subject,
            '[Django] locale/en-US/%s.lang is corrupted' % path)
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
