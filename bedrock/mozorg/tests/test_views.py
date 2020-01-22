# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

from django.test import override_settings
from django.test.client import RequestFactory

from bedrock.base.urlresolvers import reverse
from mock import ANY, patch

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg import views


class TestViews(TestCase):
    @patch.dict(os.environ, FUNNELCAKE_5_LOCALES='en-US', FUNNELCAKE_5_PLATFORMS='win')
    def test_download_button_funnelcake(self):
        """The download button should have the funnelcake ID."""
        with self.activate('en-US'):
            resp = self.client.get(reverse('mozorg.home'), {'f': '5'})
            assert b'product=firefox-stub-f5&' in resp.content

    def test_download_button_bad_funnelcake(self):
        """The download button should not have a bad funnelcake ID."""
        with self.activate('en-US'):
            resp = self.client.get(reverse('mozorg.home'), {'f': '5dude'})
            assert b'product=firefox-stub&' in resp.content
            assert b'product=firefox-stub-f5dude&' not in resp.content

            resp = self.client.get(reverse('mozorg.home'), {'f': '999999999'})
            assert b'product=firefox-stub&' in resp.content
            assert b'product=firefox-stub-f999999999&' not in resp.content


class TestRobots(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.view = views.Robots()

    def test_production_disallow_all_is_false(self):
        self.view.request = self.rf.get('/', HTTP_HOST='www.mozilla.org')
        self.assertFalse(self.view.get_context_data()['disallow_all'])

    def test_non_production_disallow_all_is_true(self):
        self.view.request = self.rf.get('/', HTTP_HOST='www.allizom.org')
        self.assertTrue(self.view.get_context_data()['disallow_all'])

    def test_robots_no_redirect(self):
        response = self.client.get('/robots.txt', HTTP_HOST='www.mozilla.org')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context_data['disallow_all'])
        self.assertEqual(response.get('Content-Type'), 'text/plain')


@patch('bedrock.mozorg.views.l10n_utils.render')
class TestTechnology(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_technology_template(self, render_mock):
        view = views.TechnologyView()
        view.request = RequestFactory().get('/technology/')
        view.request.locale = 'en-US'
        assert view.get_template_names() == ['mozorg/technology-en.html']

    def test_technology_locale_template(self, render_mock):
        view = views.TechnologyView()
        view.request = RequestFactory().get('/technology/')
        view.request.locale = 'es-ES'
        assert view.get_template_names() == ['mozorg/technology.html']


@patch('bedrock.mozorg.views.l10n_utils.render')
class TestHomePage(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_home_en_template(self, render_mock):
        req = RequestFactory().get('/')
        req.locale = 'en-US'
        views.home_view(req)
        render_mock.assert_called_once_with(req, 'mozorg/home/home-en.html', ANY)

    def test_home_de_template(self, render_mock):
        req = RequestFactory().get('/')
        req.locale = 'de'
        views.home_view(req)
        render_mock.assert_called_once_with(req, 'mozorg/home/home-de.html', ANY)

    def test_home_fr_template(self, render_mock):
        req = RequestFactory().get('/')
        req.locale = 'fr'
        views.home_view(req)
        render_mock.assert_called_once_with(req, 'mozorg/home/home-fr.html', ANY)

    def test_home_locale_template(self, render_mock):
        req = RequestFactory().get('/')
        req.locale = 'es'
        views.home_view(req)
        render_mock.assert_called_once_with(req, 'mozorg/home/home.html', ANY)


@override_settings(DEV=True)
class TestOAuthFxa(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    @override_settings(DEV=False)
    @override_settings(SWITCH_FIREFOX_CONCERT_SERIES=False)
    def test_switch_off(self):
        """Should redirect to the home page if the whole system is turned off"""
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides')
        response = views.oauth_fxa(req)
        assert response.status_code == 302
        assert response['Location'] == '/'

    def test_missing_expected_state(self):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides')
        response = views.oauth_fxa(req)
        assert response.status_code == 302
        assert response['Location'] == '/oauth/fxa/error/'

    def test_missing_provided_state(self):
        req = self.rf.get('/mozorg/oauth/fxa?code=abides')
        req.COOKIES['fxaOauthState'] = 'thedude'
        response = views.oauth_fxa(req)
        assert response.status_code == 302
        assert response['Location'] == '/oauth/fxa/error/'

    def test_state_mismatch(self):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides')
        req.COOKIES['fxaOauthState'] = 'walter'
        response = views.oauth_fxa(req)
        assert response.status_code == 302
        assert response['Location'] == '/oauth/fxa/error/'

    def test_missing_code(self):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude')
        req.COOKIES['fxaOauthState'] = 'thedude'
        response = views.oauth_fxa(req)
        assert response.status_code == 302
        assert response['Location'] == '/oauth/fxa/error/'

    @patch('bedrock.mozorg.views.get_fxa_oauth_token')
    def test_token_failure(self, gfot_mock):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides')
        req.COOKIES['fxaOauthState'] = 'thedude'
        gfot_mock.return_value = None
        response = views.oauth_fxa(req)
        assert response.status_code == 302
        assert response['Location'] == '/oauth/fxa/error/'

    @patch('bedrock.mozorg.views.get_fxa_oauth_token')
    @patch('bedrock.mozorg.views.get_fxa_profile_email')
    def test_email_failure(self, gfpe_mock, gfot_mock):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides')
        req.COOKIES['fxaOauthState'] = 'thedude'
        gfot_mock.return_value = 'atoken'
        gfpe_mock.return_value = None
        response = views.oauth_fxa(req)
        assert response.status_code == 302
        assert response['Location'] == '/oauth/fxa/error/'

    @patch('bedrock.mozorg.views.get_fxa_oauth_token')
    @patch('bedrock.mozorg.views.get_fxa_profile_email')
    @patch('bedrock.mozorg.views.fxa_concert_rsvp')
    def test_rsvp_failure(self, rsvp_mock, gfpe_mock, gfot_mock):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides')
        req.COOKIES['fxaOauthState'] = 'thedude'
        gfot_mock.return_value = 'atoken'
        gfpe_mock.return_value = 'maude@example.com'
        rsvp_mock.return_value = None
        response = views.oauth_fxa(req)
        assert response.status_code == 302
        assert response['Location'] == '/oauth/fxa/error/'

    @patch('bedrock.mozorg.views.get_fxa_oauth_token')
    @patch('bedrock.mozorg.views.get_fxa_profile_email')
    @patch('bedrock.mozorg.views.fxa_concert_rsvp')
    def test_success(self, rsvp_mock, gfpe_mock, gfot_mock):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides')
        req.COOKIES['fxaOauthState'] = 'thedude'
        gfot_mock.return_value = 'atoken'
        gfpe_mock.return_value = 'maude@example.com'
        response = views.oauth_fxa(req)
        assert response.cookies['fxaOauthVerified'].value == 'True'
        assert response.status_code == 302
        assert response['Location'] == '/firefox/concerts/'

    @patch('bedrock.mozorg.views.get_fxa_oauth_token')
    @patch('bedrock.mozorg.views.get_fxa_profile_email')
    @patch('bedrock.mozorg.views.fxa_concert_rsvp')
    def test_rsvp_is_firefox(self, rsvp_mock, gfpe_mock, gfot_mock):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides', HTTP_USER_AGENT='Firefox')
        req.COOKIES['fxaOauthState'] = 'thedude'
        gfot_mock.return_value = 'atoken'
        gfpe_mock.return_value = 'maude@example.com'
        views.oauth_fxa(req)
        rsvp_mock.assert_called_with('maude@example.com', True)

    @patch('bedrock.mozorg.views.get_fxa_oauth_token')
    @patch('bedrock.mozorg.views.get_fxa_profile_email')
    @patch('bedrock.mozorg.views.fxa_concert_rsvp')
    def test_rsvp_not_firefox(self, rsvp_mock, gfpe_mock, gfot_mock):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides', HTTP_USER_AGENT='Safari')
        req.COOKIES['fxaOauthState'] = 'thedude'
        gfot_mock.return_value = 'atoken'
        gfpe_mock.return_value = 'maude@example.com'
        views.oauth_fxa(req)
        rsvp_mock.assert_called_with('maude@example.com', False)
