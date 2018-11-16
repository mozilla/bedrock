# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
from datetime import date
import json

from django.core.cache import cache
from django.db.utils import DatabaseError
from django.http.response import Http404
from django.test import override_settings
from django.test.client import RequestFactory

from bedrock.base.urlresolvers import reverse
from mock import ANY, patch
from nose.tools import eq_, ok_

from bedrock.mozorg.tests import TestCase
from bedrock.mozorg import views
from scripts import update_tableau_data


class TestViews(TestCase):
    @patch.dict(os.environ, FUNNELCAKE_5_LOCALES='en-US', FUNNELCAKE_5_PLATFORMS='win')
    def test_download_button_funnelcake(self):
        """The download button should have the funnelcake ID."""
        with self.activate('en-US'):
            resp = self.client.get(reverse('mozorg.home'), {'f': '5'})
            ok_('product=firefox-stub-f5&' in resp.content)

    def test_download_button_bad_funnelcake(self):
        """The download button should not have a bad funnelcake ID."""
        with self.activate('en-US'):
            resp = self.client.get(reverse('mozorg.home'), {'f': '5dude'})
            ok_('product=firefox-stub&' in resp.content)
            ok_('product=firefox-stub-f5dude&' not in resp.content)

            resp = self.client.get(reverse('mozorg.home'), {'f': '999999999'})
            ok_('product=firefox-stub&' in resp.content)
            ok_('product=firefox-stub-f999999999&' not in resp.content)


class TestContributeStudentAmbassadorsLanding(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.get_req = self.rf.get('/')
        self.no_exist = views.TwitterCache.DoesNotExist()
        cache.clear()

    @patch.object(views.l10n_utils, 'render')
    @patch.object(views.TwitterCache.objects, 'get')
    def test_db_exception_works(self, mock_manager, mock_render):
        """View should function properly without the DB."""
        mock_manager.side_effect = DatabaseError
        views.contribute_studentambassadors_landing(self.get_req)
        mock_render.assert_called_with(ANY, ANY, {'tweets': []})

    @patch.object(views.l10n_utils, 'render')
    @patch.object(views.TwitterCache.objects, 'get')
    def test_no_db_row_works(self, mock_manager, mock_render):
        """View should function properly without data in the DB."""
        mock_manager.side_effect = views.TwitterCache.DoesNotExist
        views.contribute_studentambassadors_landing(self.get_req)
        mock_render.assert_called_with(ANY, ANY, {'tweets': []})

    @patch.object(views.l10n_utils, 'render')
    @patch.object(views.TwitterCache.objects, 'get')
    def test_db_cache_works(self, mock_manager, mock_render):
        """View should use info returned by DB."""
        good_val = 'The Dude tweets, man.'
        mock_manager.return_value.tweets = good_val
        views.contribute_studentambassadors_landing(self.get_req)
        mock_render.assert_called_with(ANY, ANY, {'tweets': good_val})


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


class TestMozIDDataView(TestCase):
    def setUp(self):
        with patch.object(update_tableau_data, 'get_external_data') as ged:
            ged.return_value = (
                (date(2015, 2, 2), 'Firefox', 'bugzilla', 100, 10),
                (date(2015, 2, 2), 'Firefox OS', 'bugzilla', 100, 10),
                (date(2015, 2, 9), 'Sumo', 'sumo', 100, 10),
                (date(2015, 2, 9), 'Firefox OS', 'sumo', 100, 10),
                (date(2015, 2, 9), 'QA', 'reps', 100, 10),
            )
            update_tableau_data.run()

    def _get_json(self, source):
        cache.clear()
        req = RequestFactory().get('/')
        resp = views.mozid_data_view(req, source)
        eq_(resp['content-type'], 'application/json')
        eq_(resp['access-control-allow-origin'], '*')
        return json.loads(resp.content)

    def test_all(self):
        eq_(self._get_json('all'), [
            {'wkcommencing': '2015-02-09', 'totalactive': 300, 'new': 30},
            {'wkcommencing': '2015-02-02', 'totalactive': 200, 'new': 20},
        ])

    def test_team(self):
        """When acting on a team, should just return sums for that team."""
        eq_(self._get_json('firefoxos'), [
            {'wkcommencing': '2015-02-09', 'totalactive': 100, 'new': 10},
            {'wkcommencing': '2015-02-02', 'totalactive': 100, 'new': 10},
        ])

    def test_source(self):
        """When acting on a source, should just return sums for that source."""
        eq_(self._get_json('sumo'), [
            {'wkcommencing': '2015-02-09', 'totalactive': 100, 'new': 10},
        ])

    @patch('bedrock.mozorg.models.CONTRIBUTOR_SOURCE_NAMES', {})
    def test_unknown(self):
        """An unknown source should raise a 404."""
        with self.assertRaises(Http404):
            self._get_json('does-not-exist')


@patch('bedrock.mozorg.views.l10n_utils.render')
class TestTechnology(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_technology_template(self, render_mock):
        view = views.TechnologyView()
        view.request = RequestFactory().get('/technology/')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['mozorg/technology-en.html'])

    def test_technology_locale_template(self, render_mock):
        view = views.TechnologyView()
        view.request = RequestFactory().get('/technology/')
        view.request.locale = 'es-ES'
        eq_(view.get_template_names(), ['mozorg/technology.html'])


@patch('bedrock.mozorg.views.l10n_utils.render')
class TestHomePage(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_home_en_template(self, render_mock):
        req = RequestFactory().get('/')
        req.locale = 'en-US'
        views.home_view(req)
        render_mock.assert_called_once_with(req, 'mozorg/home/home-en.html', ANY)

    def test_home_locale_template(self, render_mock):
        req = RequestFactory().get('/')
        req.locale = 'de'
        views.home_view(req)
        render_mock.assert_called_once_with(req, 'mozorg/home/home.html', ANY)


@patch('bedrock.mozorg.views.l10n_utils.render')
class TestAboutPage(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_about_en_template(self, render_mock):
        req = RequestFactory().get('/')
        req.locale = 'en-US'
        views.about_view(req)
        render_mock.assert_called_once_with(req, 'mozorg/about-en.html')

    def test_about_locale_template(self, render_mock):
        req = RequestFactory().get('/')
        req.locale = 'de'
        views.about_view(req)
        render_mock.assert_called_once_with(req, 'mozorg/about.html')


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
        eq_(response.status_code, 302)
        eq_(response['Location'], '/')

    def test_missing_expected_state(self):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides')
        response = views.oauth_fxa(req)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/oauth/fxa/error/')

    def test_missing_provided_state(self):
        req = self.rf.get('/mozorg/oauth/fxa?code=abides')
        req.COOKIES['fxaOauthState'] = 'thedude'
        response = views.oauth_fxa(req)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/oauth/fxa/error/')

    def test_state_mismatch(self):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides')
        req.COOKIES['fxaOauthState'] = 'walter'
        response = views.oauth_fxa(req)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/oauth/fxa/error/')

    def test_missing_code(self):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude')
        req.COOKIES['fxaOauthState'] = 'thedude'
        response = views.oauth_fxa(req)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/oauth/fxa/error/')

    @patch('bedrock.mozorg.views.get_fxa_oauth_token')
    def test_token_failure(self, gfot_mock):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides')
        req.COOKIES['fxaOauthState'] = 'thedude'
        gfot_mock.return_value = None
        response = views.oauth_fxa(req)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/oauth/fxa/error/')

    @patch('bedrock.mozorg.views.get_fxa_oauth_token')
    @patch('bedrock.mozorg.views.get_fxa_profile_email')
    def test_email_failure(self, gfpe_mock, gfot_mock):
        req = self.rf.get('/mozorg/oauth/fxa?state=thedude&code=abides')
        req.COOKIES['fxaOauthState'] = 'thedude'
        gfot_mock.return_value = 'atoken'
        gfpe_mock.return_value = None
        response = views.oauth_fxa(req)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/oauth/fxa/error/')

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
        eq_(response.status_code, 302)
        eq_(response['Location'], '/oauth/fxa/error/')

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
        eq_(response.status_code, 302)
        eq_(response['Location'], '/firefox/concerts/')

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
