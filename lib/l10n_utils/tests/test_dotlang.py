# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core import mail
from django.core.cache import cache
from django.core.urlresolvers import clear_url_caches
from django.http import HttpRequest
from django.test.utils import override_settings

from django_jinja.backend import Jinja2
from mock import patch
from nose.tools import assert_not_equal, eq_, ok_
from pathlib import Path
from product_details import product_details
from pyquery import PyQuery as pq

from bedrock.mozorg.tests import TestCase
from lib.l10n_utils import render
from lib.l10n_utils.dotlang import (_, _lazy, FORMAT_IDENTIFIER_RE, lang_file_has_tag,
                                    lang_file_is_active, parse, translate)
from lib.l10n_utils.extract import extract_python


LANG_FILES = 'test_file'
ROOT_PATH = Path(__file__).with_name('test_files')
ROOT = str(ROOT_PATH)
TEMPLATE_DIRS = [str(ROOT_PATH.joinpath('templates'))]
jinja_env = Jinja2.get_default().env


@override_settings(DEV=False, LANGUAGE_CODE='en-US')
@patch.object(jinja_env.loader, 'searchpath', TEMPLATE_DIRS)
@patch.object(settings, 'ROOT_URLCONF', 'lib.l10n_utils.tests.test_files.urls')
@patch.object(settings, 'ROOT', ROOT)
class TestLangFilesActivation(TestCase):
    def setUp(self):
        clear_url_caches()

    def test_lang_file_is_active(self):
        """
        `lang_file_is_active` should return true if lang file has the
        comment, and false otherwise.
        """
        ok_(lang_file_is_active('active_de_lang_file', 'de'))
        ok_(lang_file_is_active('active_de_lang_file_bom', 'de'))
        ok_(not lang_file_is_active('active_de_lang_file', 'es'))
        ok_(not lang_file_is_active('inactive_de_lang_file', 'de'))
        ok_(not lang_file_is_active('does_not_exist', 'de'))

    def test_lang_file_has_tag(self):
        """
        `lang_file_has_tag` should return true if lang file has the
        comment, and false otherwise.
        """
        ok_(lang_file_has_tag('active_de_lang_file', 'de', 'active'))
        ok_(lang_file_has_tag('active_de_lang_file_bom', 'de', 'active'))
        ok_(not lang_file_has_tag('active_de_lang_file', 'es', 'active'))
        ok_(not lang_file_has_tag('inactive_de_lang_file', 'de', 'active'))
        ok_(not lang_file_has_tag('file_does_not_exist', 'de', 'active'))
        ok_(lang_file_has_tag('main', 'de', 'guten_tag'))
        ok_(not lang_file_has_tag('main', 'de', 'tag_after_non_tag_lines'))
        ok_(not lang_file_has_tag('main', 'de', 'no_such_tag'))

    def test_active_locale_not_redirected(self):
        """ Active lang file should render correctly.

        Also the template has an inactive lang file manually set,
        but that should not cause it to be inactive.
        """
        response = self.client.get('/de/active-de-lang-file/')
        eq_(response.status_code, 200)
        doc = pq(response.content)
        eq_(doc('h1').text(), 'Die Lage von Mozilla')

    def test_inactive_locale_redirected(self):
        """ Inactive locale should redirect to en-US. """
        response = self.client.get('/de/inactive-de-lang-file/')
        eq_(response.status_code, 302)
        eq_(response['location'],
            'http://testserver/en-US/inactive-de-lang-file/')
        response = self.client.get('/de/inactive-de-lang-file/', follow=True)
        doc = pq(response.content)
        eq_(doc('h1').text(), 'The State of Mozilla')

    @override_settings(DEV=True)
    def test_inactive_locale_not_redirected_dev_true(self):
        """
        Inactive lang file should not redirect in DEV mode.
        """
        response = self.client.get('/de/inactive-de-lang-file/')
        eq_(response.status_code, 200)
        doc = pq(response.content)
        eq_(doc('h1').text(), 'Die Lage von Mozilla')

    def test_active_alternate_lang_file(self):
        """Template with active alternate lang file should activate from it."""
        response = self.client.get('/de/state-of-mozilla/')
        eq_(response.status_code, 200)
        doc = pq(response.content)
        eq_(doc('h1').text(), 'Die Lage von Mozilla')


class TestDotlang(TestCase):
    def setUp(self):
        cache.clear()
        clear_url_caches()

    def test_parse(self):
        path = str(ROOT_PATH.joinpath('test.lang'))
        parsed = parse(path)
        expected = {
            u'Hooray! Your Firefox is up to date.':
                u'F\xe9licitations&nbsp;! '
                u'Votre Firefox a \xe9t\xe9 mis \xe0 jour.',
            u'Your Firefox is out of date.':
                u'Votre Firefox ne semble pas \xe0 jour.'
        }
        eq_(parsed, expected)

    def test_parse_not_skip_untranslated(self):
        path = str(ROOT_PATH.joinpath('test.lang'))
        parsed = parse(path, skip_untranslated=False)
        expected = {
            u'Hooray! Your Firefox is up to date.':
                u'F\xe9licitations&nbsp;! '
                u'Votre Firefox a \xe9t\xe9 mis \xe0 jour.',
            u'Your Firefox is out of date.':
                u'Votre Firefox ne semble pas \xe0 jour.',
            u'Firefox Beta':
                u'Firefox Beta',
            u'Firefox Aurora':
                u'Firefox Aurora'
        }
        eq_(parsed, expected)

    def test_parse_with_comments(self):
        path = str(ROOT_PATH.joinpath('test.lang'))
        parsed = parse(path, extract_comments=True)

        expected = {
            u'Hooray! Your Firefox is up to date.': [
                u'This is for the Whatsnew page: '
                u'http://www-dev.allizom.org/b/firefox/whatsnew/',
                u'F\xe9licitations&nbsp;! '
                u'Votre Firefox a \xe9t\xe9 mis \xe0 jour.',
            ],
            u'Your Firefox is out of date.': [
                None,
                u'Votre Firefox ne semble pas \xe0 jour.',
            ]
        }
        eq_(parsed, expected)

    @override_settings(EMAIL_SUBJECT_PREFIX='[bedrock] ', MANAGERS=('dude@example.com',))
    def test_parse_utf8_error(self):
        path = str(ROOT_PATH.joinpath('test_utf8_error.lang'))
        parsed = parse(path)
        eq_(len(mail.outbox), 1)
        eq_(mail.outbox[0].subject, '[bedrock] %s is corrupted' % path)
        expected = {
            u'Update now': u'Niha rojane bike',
            u'Supported Devices': u'C�haz�n pi�tgiriy'
        }
        eq_(parsed, expected)
        mail.outbox = []

    def test_parse_ingnores_untranslated(self):
        """parse should skip strings that aren't translated."""
        path = str(ROOT_PATH.joinpath('locale/de/main.lang'))
        parsed = parse(path)
        expected = {
            u'The State of Mozilla': u'Awesome Baby! YEEEAAHHHH!!'
        }
        self.assertDictEqual(parsed, expected)

    def test_format_identifier_re(self):
        eq_(FORMAT_IDENTIFIER_RE.findall('%s %s'),
            [('%s', ''), ('%s', '')])

        eq_(FORMAT_IDENTIFIER_RE.findall('%(foo_bar)s %s'),
            [('%(foo_bar)s', 'foo_bar'), ('%s', '')])

    @override_settings(ROOT=ROOT, EMAIL_SUBJECT_PREFIX='[bedrock] ',
                       MANAGERS=('dude@example.com',))
    def test_format_identifier_mismatch(self):
        path = 'format_identifier_mismatch'
        expected = '%(foo)s is the new %s'
        with self.activate('fr'):
            result = translate(expected, [path])
        eq_(expected, result)
        eq_(len(mail.outbox), 1)
        eq_(mail.outbox[0].subject,
            '[bedrock] locale/fr/%s.lang is corrupted' % path)
        mail.outbox = []

    @patch.object(settings, 'ROOT', ROOT)
    def test_format_identifier_order(self):
        """
        Test that the order in which the format identifier appears doesn't
        matter
        """
        path = 'format_identifier_mismatch'
        expected = '%(foo)s is the new %(bar)s'
        with self.activate('fr'):
            result = translate(expected, [path])
        assert_not_equal(expected, result)
        eq_(len(mail.outbox), 0)

    @patch.object(jinja_env.loader, 'searchpath', TEMPLATE_DIRS)
    @patch.object(settings, 'ROOT_URLCONF', 'lib.l10n_utils.tests.test_files.urls')
    @patch.object(settings, 'ROOT', ROOT)
    def test_lang_files_queried_in_order(self):
        """The more specific lang files should be searched first."""
        response = self.client.get('/de/trans-block-reload-test/')
        doc = pq(response.content)
        gettext_call = doc('h1')
        eq_(gettext_call.text(), 'Die Lage von Mozilla')

    @patch.object(settings, 'ROOT', ROOT)
    def test_extract_message_tweaks_do_not_break(self):
        """
        Extraction and translation matching should tweak msgids the same.
        """
        clean_string = u'Stuff about many things.'
        dirty_string = u'Stuff\xa0about\r\nmany\t   things.'
        trans_string = u'This is the translation.'

        # extraction
        pypath = ROOT_PATH.joinpath('extract_me.py')
        with open(str(pypath)) as pyfile:
            vals = extract_python(pyfile, ['_'], [], {}).next()
        eq_(vals[2], clean_string)

        # translation
        # path won't exist for en-US as there isn't a dir for that
        # in locale.
        with self.activate('fr'):
            result = translate(dirty_string, ['does_not_exist'])
            eq_(result, dirty_string)

            result = translate(dirty_string, ['tweaked_message_translation'])
            eq_(result, trans_string)

    @patch('lib.l10n_utils.dotlang.translate')
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

    @patch('lib.l10n_utils.dotlang.translate')
    def test_gettext_ignores_default_lang_files(self, trans_patch):
        """
        The `l10n_utils.dotlang._` function should search .lang files
        specified in the module from which it's called before the
        default files, but it should not include the defaults twice.
        """
        # use LANG_FILES global in this module
        global LANG_FILES
        old_lang_files = LANG_FILES

        trans_str = 'Translate me'
        LANG_FILES = [settings.DOTLANG_FILES[0], 'dude', 'donnie', 'walter']
        _(trans_str)
        call_lang_files = LANG_FILES[1:] + settings.DOTLANG_FILES
        trans_patch.assert_called_with(trans_str, call_lang_files)

        # restore original value to avoid test leakage
        LANG_FILES = old_lang_files

    @patch('lib.l10n_utils.dotlang.translate')
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

    @patch('lib.l10n_utils.dotlang.translate')
    def test_gettext_searches_kwarg_specified_lang_files(self, trans_patch):
        """
        The `l10n_utils.dotlang._` function should search .lang files
        specified in the `lang_files` keyword arg, and not the ones from the
        module.
        """
        # test the case when LANG_FILES is a string
        trans_str = 'Translate me'
        _(trans_str, lang_files='maude')
        call_lang_files = ['maude'] + settings.DOTLANG_FILES
        trans_patch.assert_called_with(trans_str, call_lang_files)

        # test the case when LANG_FILES is a list
        lang_files_list = ['maude', 'bunny', 'uli']
        _(trans_str, lang_files=lang_files_list)
        call_lang_files = lang_files_list + settings.DOTLANG_FILES
        trans_patch.assert_called_with(trans_str, call_lang_files)

    @patch('lib.l10n_utils.dotlang.translate')
    def test_gettext_lazy_searches_kwarg_specified_lang_files(self, trans_patch):
        """
        The `l10n_utils.dotlang._lazy` function should search .lang files
        specified in the `lang_files` keyword arg, and not the ones from the
        module.
        """
        # test the case when LANG_FILES is a string
        trans_str = 'Translate me'
        # have to call __unicode__ directly because the value is a Mock
        # object, and the `unicode()` function throws an exception.
        _lazy(trans_str, lang_files='maude').__unicode__()
        call_lang_files = ['maude'] + settings.DOTLANG_FILES
        trans_patch.assert_called_with(trans_str, call_lang_files)

        # test the case when LANG_FILES is a list
        lang_files_list = ['maude', 'bunny', 'uli']
        _lazy(trans_str, lang_files=lang_files_list).__unicode__()
        call_lang_files = lang_files_list + settings.DOTLANG_FILES
        trans_patch.assert_called_with(trans_str, call_lang_files)

    @patch('lib.l10n_utils.dotlang.translate')
    def test_lazy_gettext_searches_specified_lang_files(self, trans_patch):
        """
        The `l10n_utils.dotlang._lazy` function should search .lang files
        specified in the module from which it's called before the
        default files.
        """
        from lib.l10n_utils.tests.test_files import extract_me_with_langfiles_lazy

        dude_says = extract_me_with_langfiles_lazy.do_translate()
        dirty_string = u"I'm The Dude, so that's what you call me, man."
        self.assertFalse(trans_patch.called)
        # have to call __unicode__ directly because the value is a Mock
        # object, and the `unicode()` function throws an exception.
        dude_says.__unicode__()
        trans_patch.assert_called_with(dirty_string, ['donnie', 'walter'] +
                                       settings.DOTLANG_FILES)

    @patch('lib.l10n_utils.dotlang.translate')
    def test_gettext_works_without_extra_lang_files(self, trans_patch):
        """
        The `l10n_utils.dotlang._` function should search the default .lang
        files if no others are specified.
        """
        from lib.l10n_utils.tests.test_files import extract_me

        extract_me.do_translate()
        dirty_string = u'Stuff\xa0about\r\nmany\t   things.'
        trans_patch.assert_called_with(dirty_string, settings.DOTLANG_FILES)

    def test_gettext_str_interpolation(self):
        result = _('The %s %s.', 'dude', 'abides')
        eq_(result, 'The dude abides.')

    @patch('lib.l10n_utils.dotlang.cache')
    def test_translate_skips_for_default_locale(self, cache_mock):
        """
        Translation calls should not hit the cache for the default language.
        There will never be any lang files, and the strings in the calls are
        the correct ones already.
        """
        with self.activate('fr'):
            translate('The Dude abides.', ['main'])
        self.assertEqual(cache_mock.get.call_count, 1)
        cache_mock.reset_mock()
        with self.activate(settings.LANGUAGE_CODE):
            translate('The Dude abides.', ['main'])
        self.assertEqual(cache_mock.get.call_count, 0)


@patch.object(jinja_env.loader, 'searchpath', TEMPLATE_DIRS)
@patch.object(settings, 'ROOT_URLCONF', 'lib.l10n_utils.tests.test_files.urls')
@patch.object(settings, 'ROOT', ROOT)
class TestTranslationList(TestCase):
    def _test(self, lang, view_name):
        """
        The context of each view should have the 'links' dictionary which
        contains the canonical and alternate URLs of the page.
        """
        request = HttpRequest()
        request.path = '/' + lang + '/' + view_name + '/'
        request.locale = lang
        template = view_name.replace('-', '_') + '.html'
        with patch('lib.l10n_utils.django_render') as django_render:
            render(request, template, {})
        translations = django_render.call_args[0][2]['translations']

        # The en-US locale is always active
        eq_(translations['en-US'], product_details.languages['en-US']['native'])
        # The de locale is active depending on the template
        if view_name == 'active-de-lang-file':
            eq_(translations['de'], product_details.languages['de']['native'])
        else:
            eq_('de' in translations, False)
        # The fr locale is inactive
        eq_('fr' in translations, False)

    def test_localized_en(self):
        self._test('en-US', 'active-de-lang-file')

    def test_localized_de(self):
        self._test('de', 'active-de-lang-file')

    def test_unlocalized(self):
        self._test('en-US', 'inactive-de-lang-file')
