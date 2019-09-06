# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.test import RequestFactory
from django.test.utils import override_settings

import basket
import fxa.constants
import fxa.errors

from mock import ANY, Mock, patch

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg.util import (
    get_fb_like_locale,
    get_tweets,
    page,
    get_fxa_clients,
    get_fxa_oauth_token,
    get_fxa_profile_email,
    fxa_concert_rsvp,
)


ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files')


@patch('bedrock.mozorg.util.TwitterAPI')
@override_settings(TWITTER_ACCOUNTS=('dude', 'walter'),
                   TWITTER_ACCOUNT_OPTS={'dude': {'abide': True, 'include_rts': False}})
class TestTwitterAPI(TestCase):
    def test_default_call_options(self, twitter_api):
        get_tweets('walter')
        twitter_api.assert_called()
        twitter_api.return_value.user_timeline.assert_called_with(screen_name='walter',
                                                                  include_rts=True,
                                                                  exclude_replies=True,
                                                                  count=100)

    def test_override_default_call_options(self, twitter_api):
        get_tweets('dude')
        twitter_api.assert_called()
        twitter_api.return_value.user_timeline.assert_called_with(screen_name='dude',
                                                                  abide=True,
                                                                  include_rts=False,
                                                                  exclude_replies=True,
                                                                  count=100)

    def test_returns_none_if_api_not_configured(self, twitter_api):
        twitter_api.return_value = None
        self.assertIsNone(get_tweets('dude'))


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


@override_settings(FXA_OAUTH_SERVER_ENV='stable')
@patch('bedrock.mozorg.util.fxa.oauth')
@patch('bedrock.mozorg.util.fxa.profile')
class GetFxAClientsTests(TestCase):
    def test_get_fxa_clients(self, profile_mock, oauth_mock):
        oauth, profile = get_fxa_clients()
        oauth_mock.Client.assert_called_with(server_url=fxa.constants.STABLE_URLS['oauth'])
        profile_mock.Client.assert_called_with(server_url=fxa.constants.STABLE_URLS['profile'])
        assert oauth == oauth_mock.Client.return_value
        assert profile == profile_mock.Client.return_value

        get_fxa_clients()
        assert oauth_mock.Client.call_count == 1


@patch('bedrock.mozorg.util.get_fxa_clients')
class FxAOauthTests(TestCase):
    @override_settings(FXA_OAUTH_CLIENT_ID='12345', FXA_OAUTH_CLIENT_SECRET='67890')
    def test_get_fxa_oauth_token_error(self, gfc_mock):
        oauth_mock = Mock()
        gfc_mock.return_value = oauth_mock, None
        trade_code = oauth_mock.trade_code
        trade_code.side_effect = fxa.errors.ClientError()
        assert not get_fxa_oauth_token('abc123')
        trade_code.assert_called_with('abc123', client_id='12345', client_secret='67890')

    @override_settings(FXA_OAUTH_CLIENT_ID='12345', FXA_OAUTH_CLIENT_SECRET='67890')
    def test_get_fxa_oauth_token_success(self, gfc_mock):
        oauth_mock = Mock()
        gfc_mock.return_value = oauth_mock, None
        trade_code = oauth_mock.trade_code
        trade_code.return_value = {'access_token': 'goodtoken'}
        assert get_fxa_oauth_token('abc123') == 'goodtoken'
        trade_code.assert_called_with('abc123', client_id='12345', client_secret='67890')

    def test_get_fxa_profile_email_error(self, gfc_mock):
        profile_mock = Mock()
        gfc_mock.return_value = None, profile_mock
        get_email = profile_mock.get_email
        get_email.side_effect = fxa.errors.ClientError()
        assert not get_fxa_profile_email('ralphs-card')
        get_email.assert_called_with('ralphs-card')

    def test_get_fxa_profile_email_success(self, gfc_mock):
        profile_mock = Mock()
        gfc_mock.return_value = None, profile_mock
        get_email = profile_mock.get_email
        get_email.return_value = 'maude@example.com'
        assert get_email('ralphs-card') == 'maude@example.com'
        get_email.assert_called_with('ralphs-card')


@override_settings(BASKET_API_KEY='123456')
class FxARSVPTests(TestCase):
    def setUp(self):
        patcher = patch('bedrock.mozorg.util.basket.request')
        self.mock_rsvp = patcher.start()
        self.addCleanup(patcher.stop)

    def test_is_fx(self):
        fxa_concert_rsvp('thedude@example.com', True)

        self.mock_rsvp.assert_called_with('post', 'fxa-concerts-rsvp', data={
            'email': 'thedude@example.com',
            'is_firefox': 'Y',
            'campaign_id': 'firefox-concert-series-Q4-2018',
            'api_key': '123456'
        })

    def test_not_fx(self):
        fxa_concert_rsvp('thedude@example.com', False)

        self.mock_rsvp.assert_called_with('post', 'fxa-concerts-rsvp', data={
            'email': 'thedude@example.com',
            'is_firefox': 'N',
            'campaign_id': 'firefox-concert-series-Q4-2018',
            'api_key': '123456'
        })

    def test_basket_success(self):
        assert fxa_concert_rsvp('thedude@example.com', True)

    def test_basket_failure(self):
        self.mock_rsvp.side_effect = basket.BasketException
        assert not fxa_concert_rsvp('thedude@example.com', True)
