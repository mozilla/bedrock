# coding=utf-8

import os
import unittest

from django.conf import settings
from django.core import mail

from mock import patch
from nose.tools import eq_
from tower.management.commands.extract import extract_tower_python

from l10n_utils.dotlang import FORMAT_IDENTIFIER_RE, parse, translate

ROOT = os.path.dirname(os.path.abspath(__file__))


class TestDotlang(unittest.TestCase):
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
        result = translate(expected, [path])
        eq_(expected, result)
        eq_(len(mail.outbox), 1)
        eq_(mail.outbox[0].subject, '[Django] %s is corrupted' % path)
        mail.outbox = []

    @patch.object(settings, 'ROOT', ROOT)
    def test_extract_message_tweaks_do_not_break(self):
        """
        Extraction and translation matching should tweak msgids the same.
        """
        clean_string = u'Stuff about many things.'
        dirty_string = u'Stuff\xa0about\r\nmany\t   things.'
        trans_string = u'This is the translation.'

        # extraction
        with open(os.path.join(ROOT, 'test_py_extract.py.txt')) as pyfile:
            vals = extract_tower_python(pyfile, {'_', None}, [], {}).next()
        eq_(vals[2], clean_string)

        # translation
        # path won't exist for en-US as there isn't a dir for that
        # in locale.
        result = translate(dirty_string, ['does_not_exist'])
        eq_(result, dirty_string)

        result = translate(dirty_string, ['tweaked_message_translation'])
        eq_(result, trans_string)
