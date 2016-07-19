from nose.tools import eq_
from django.test import TestCase
import jingo


def render(s, context={}):
    t = jingo.get_env().from_string(s)
    return t.render(context)


class HelpersTests(TestCase):

    def test_urlencode_with_unicode(self):
        template = '<a href="?var={{ key|urlencode }}">'
        context = {'key': '?& /()'}
        eq_(render(template, context), '<a href="?var=%3F%26+%2F%28%29">')
        # non-ascii
        context = {'key': u'\xe4'}
        eq_(render(template, context), '<a href="?var=%C3%A4">')
