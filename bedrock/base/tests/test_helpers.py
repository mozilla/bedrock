from django.test import TestCase
from django.test import override_settings

from django_jinja.backend import Jinja2
from mock import patch
from nose.tools import eq_

from bedrock.base.templatetags import helpers


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


@override_settings(LANG_GROUPS={'en': ['en-US', 'en-GB']})
def test_switch():
    with patch.object(helpers, 'waffle') as waffle:
        ret = helpers.switch({'LANG': 'de'}, 'dude', ['fr', 'de'])

    assert ret is waffle.switch.return_value
    waffle.switch.assert_called_with('dude')

    with patch.object(helpers, 'waffle') as waffle:
        assert not helpers.switch({'LANG': 'de'}, 'dude', ['fr', 'en'])

    waffle.switch.assert_not_called()

    with patch.object(helpers, 'waffle') as waffle:
        ret = helpers.switch({'LANG': 'de'}, 'dude')

    assert ret is waffle.switch.return_value
    waffle.switch.assert_called_with('dude')

    with patch.object(helpers, 'waffle') as waffle:
        ret = helpers.switch({'LANG': 'en-GB'}, 'dude', ['de', 'en'])

    assert ret is waffle.switch.return_value
    waffle.switch.assert_called_with('dude')
