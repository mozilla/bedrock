from django.test import TestCase
from django.test import override_settings

from django_jinja.backend import Jinja2
from mock import patch
from nose.tools import eq_

from bedrock.base.templatetags import helpers


jinja_env = Jinja2.get_default()
SEND_TO_DEVICE_MESSAGE_SETS = {
    'default': {
        'sms_countries': ['US', 'DE'],
        'sms': {
            'ios': 'ff-ios-download',
            'android': 'SMS_Android',
        },
        'email': {
            'android': 'download-firefox-android',
            'ios': 'download-firefox-ios',
            'all': 'download-firefox-mobile',
        }
    },
    'other': {
        'sms_countries': ['US', 'FR'],
    }
}


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

    def test_mailtoencode_with_unicode(self):
        template = '<a href="?var={{ key|mailtoencode }}">'
        context = {'key': '?& /()'}
        eq_(render(template, context), '<a href="?var=%3F%26%20/%28%29">')
        # non-ascii
        context = {'key': u'\xe4'}
        eq_(render(template, context), '<a href="?var=%C3%A4">')


@override_settings(SEND_TO_DEVICE_MESSAGE_SETS=SEND_TO_DEVICE_MESSAGE_SETS)
def test_send_to_device_sms_countries():
    assert helpers.send_to_device_sms_countries('default') == '|us|de|'
    assert helpers.send_to_device_sms_countries('other') == '|us|fr|'
    assert helpers.send_to_device_sms_countries('none') == '|us|'


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


@override_settings(DONATE_PARAMS={'en-US': {'presets': '50,30,20,10'},
                   'id': {'presets': '270000,140000,70000,40000'}})
class TestGetDonateParams(TestCase):
    def test_en_us(self):
        ctx = {'LANG': 'en-US'}
        params = helpers.get_donate_params(ctx)
        eq_(params['preset_list'], '50,30,20,10'.split(','))

    def test_id(self):
        ctx = {'LANG': 'id'}
        params = helpers.get_donate_params(ctx)
        eq_(params['preset_list'], '270000,140000,70000,40000'.split(','))

    def test_undefined_locale(self):
        ctx = {'LANG': 'de'}
        params = helpers.get_donate_params(ctx)
        eq_(params['preset_list'], '50,30,20,10'.split(','))
