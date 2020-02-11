# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.test import RequestFactory
from django.test.utils import override_settings

from mock import ANY, patch

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg.util import (
    get_fb_like_locale,
    page,
)


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')


class TestGetFacebookLikeLocale(TestCase):

    def test_supported_locale(self):
        """
        Return the given locale if supported.
        """
        assert get_fb_like_locale('en-PI') == 'en_PI'

    def test_first_supported_locale_for_language(self):
        """
        If the given locale is not supported, iterate through
        the supported locales and return the first one that
        matches the language.
        """
        assert get_fb_like_locale('es-AR') == 'es_ES'

    def test_unsupported_locale(self):
        """
        Return the default en_US when locale isn't supported.
        """
        assert get_fb_like_locale('zz-ZZ') == 'en_US'


@patch('bedrock.mozorg.util.django_render')
@patch('bedrock.mozorg.util.l10n_utils')
class TestPageUtil(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    @override_settings(SUPPORTED_NONLOCALES=['dude'])
    def test_locale_redirect_exclusion(self, l10n_mock, djrender_mock):
        """A url with a prefix in SUPPORTED_NONLOCALES should use normal render."""
        url = page('dude/abides', 'dude/abides.html', donny='alive')
        url.callback(self.rf.get('/dude/abides/'))
        assert not l10n_mock.render.called
        djrender_mock.assert_called_with(ANY, 'dude/abides.html', {'urlname': 'dude.abides',
                                                                   'donny': 'alive'})

    @override_settings(SUPPORTED_NONLOCALES=['dude'])
    def test_locale_redirect_non_exclusion(self, l10n_mock, djrender_mock):
        """A url with a prefix not in SUPPORTED_NONLOCALES should use l10n render."""
        url = page('walter/abides', 'walter/abides.html', donny='ashes')
        url.callback(self.rf.get('/walter/abides/'))
        assert not djrender_mock.called
        l10n_mock.render.assert_called_with(ANY, 'walter/abides.html', {'urlname': 'walter.abides',
                                                                        'donny': 'ashes'}, ftl_files=None)

    @override_settings(SUPPORTED_NONLOCALES=['dude'])
    def test_locale_redirect_exclusion_nested(self, l10n_mock, djrender_mock):
        """The final URL is what should be tested against the setting."""
        url = page('abides', 'abides.html', donny='alive')
        url.callback(self.rf.get('/dude/abides/'))
        assert not l10n_mock.render.called
        djrender_mock.assert_called_with(ANY, 'abides.html', {'urlname': 'abides',
                                                              'donny': 'alive'})

    @override_settings(SUPPORTED_NONLOCALES=['dude'])
    def test_locale_redirect_works_home_page(self, l10n_mock, djrender_mock):
        """Make sure the home page still works. "/" is a special case."""
        url = page('', 'index.html')
        url.callback(self.rf.get('/'))
        assert not djrender_mock.called
        l10n_mock.render.assert_called_with(ANY, 'index.html', {'urlname': 'index'}, ftl_files=None)

    def test_url_name_set_from_template(self, l10n_mock, djrender_mock):
        """If not provided the URL pattern name should be set from the template path."""
        url = page('lebowski/urban_achievers', 'lebowski/achievers.html')
        assert url.name == 'lebowski.achievers'

    def test_url_name_set_from_param(self, l10n_mock, djrender_mock):
        """If provided the URL pattern name should be set from the parameter."""
        url = page('lebowski/urban_achievers', 'lebowski/achievers.html',
                   url_name='proud.we.are.of.all.of.them')
        assert url.name == 'proud.we.are.of.all.of.them'
