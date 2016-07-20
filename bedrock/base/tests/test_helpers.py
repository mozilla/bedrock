from django.test import TestCase

from django_jinja.backend import Jinja2
from nose.tools import eq_


jinja_env = Jinja2.get_default()


def render(s, context={}):
    t = jinja_env.from_string(s)
    return t.render(context)


class HelpersTests(TestCase):

    def test_urlencode_with_unicode(self):
        template = '<a href="?var={{ key|urlencode }}">'
        context = {'key': '?& /()'}
        eq_(render(template, context), '<a href="?var=%3F%26+%2F%28%29">')
        # non-ascii
        context = {'key': u'\xe4'}
        eq_(render(template, context), '<a href="?var=%C3%A4">')
