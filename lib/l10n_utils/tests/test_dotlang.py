import os
import unittest

from nose.tools import eq_

from l10n_utils.dotlang import parse


class TestDotlang(unittest.TestCase):
    def test_parse(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.lang')
        parsed = parse(path)
        expected = {
            u'Hooray! Your Firefox is up to date.':
                u'F\xe9licitations&nbsp;! '
                u'Votre Firefox a \xe9t\xe9 mis \xe0 jour.',
            u'Your Firefox is out of date.':
                u'Votre Firefox ne semble pas \xe0 jour.'
        }

        eq_(parsed,expected)
