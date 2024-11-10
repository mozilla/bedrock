# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from unittest.mock import patch

from django.test import TestCase, override_settings

import pytest
from django_jinja.backend import Jinja2

from bedrock.base.templatetags import helpers
from lib.l10n_utils import get_translations_native_names

jinja_env = Jinja2.get_default()
SEND_TO_DEVICE_MESSAGE_SETS = {
    "default": {
        "email": {
            "android": "download-firefox-android",
            "ios": "download-firefox-ios",
            "all": "download-firefox-mobile",
        }
    }
}


def render(s, context={}):
    t = jinja_env.from_string(s)
    return t.render(context)


class HelpersTests(TestCase):
    def test_urlencode_with_unicode(self):
        template = '<a href="?var={{ key|urlencode }}">'
        context = {"key": "?& /()"}
        assert render(template, context) == '<a href="?var=%3F%26+%2F%28%29">'
        # non-ascii
        context = {"key": "\xe4"}
        assert render(template, context) == '<a href="?var=%C3%A4">'

    def test_mailtoencode_with_unicode(self):
        template = '<a href="?var={{ key|mailtoencode }}">'
        context = {"key": "?& /()"}
        assert render(template, context) == '<a href="?var=%3F%26%20/%28%29">'
        # non-ascii
        context = {"key": "\xe4"}
        assert render(template, context) == '<a href="?var=%C3%A4">'


@override_settings(LANG_GROUPS={"en": ["en-US", "en-GB"]})
def test_switch():
    with patch.object(helpers, "waffle") as waffle:
        ret = helpers.switch({"LANG": "de"}, "dude", ["fr", "de"])

    assert ret is waffle.switch.return_value
    waffle.switch.assert_called_with("dude")

    with patch.object(helpers, "waffle") as waffle:
        assert not helpers.switch({"LANG": "de"}, "dude", ["fr", "en"])

    waffle.switch.assert_not_called()

    with patch.object(helpers, "waffle") as waffle:
        ret = helpers.switch({"LANG": "de"}, "dude")

    assert ret is waffle.switch.return_value
    waffle.switch.assert_called_with("dude")

    with patch.object(helpers, "waffle") as waffle:
        ret = helpers.switch({"LANG": "en-GB"}, "dude", ["de", "en"])

    assert ret is waffle.switch.return_value
    waffle.switch.assert_called_with("dude")


@pytest.mark.parametrize(
    "translations_locales, cms_locales, django_locales, expected",
    (
        (
            ["en-US", "fr", "sco"],
            ["de", "pt-BR"],
            ["ja-JP", "zh-CN"],
            ["de", "pt-BR", "ja-JP", "zh-CN"],
        ),
        (
            ["en-US", "fr", "sco"],
            [],
            [],
            ["en-US", "fr", "sco"],
        ),
    ),
)
def test_get_lang_switcher_options(rf, translations_locales, cms_locales, django_locales, expected):
    native_translations = get_translations_native_names(translations_locales)
    native_expected = get_translations_native_names(expected)

    request = rf.get("/dummy/path/")

    if cms_locales and django_locales:
        request._locales_available_via_cms = cms_locales
        request._locales_for_django_fallback_view = django_locales

    assert native_expected == helpers.get_lang_switcher_options(
        request=request,
        translations=native_translations,
    )
