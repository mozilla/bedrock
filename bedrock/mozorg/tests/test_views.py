# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os

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
