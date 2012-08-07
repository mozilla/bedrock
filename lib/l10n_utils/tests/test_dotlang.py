# coding=utf-8

import os
import unittest

from nose.tools import eq_

from django.core import mail
from l10n_utils.dotlang import parse


class TestDotlang(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__))

    def test_parse(self):
        path = os.path.join(self.path, 'test.lang')
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
        path = os.path.join(self.path, 'test_utf8_error.lang')
        parsed = parse(path)
        eq_(len(mail.outbox), 1)
        eq_(mail.outbox[0].subject, '[Django] %s is corrupted' % path)
        expected = {
            u'Update now': u'Niha rojane bike',
            u'Supported Devices': u'C�haz�n pi�tgiriy'
        }
        eq_(parsed, expected)
        mail.outbox = []
