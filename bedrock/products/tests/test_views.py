# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from django.test.client import RequestFactory
from django.http import HttpResponse

from mock import patch

from bedrock.products import views
from bedrock.mozorg.tests import TestCase


@patch('bedrock.newsletter.forms.get_lang_choices', lambda *x: [['en', 'English']])
class TestVPNInviteWaitlist(TestCase):
    def setUp(self):
        patcher = patch('bedrock.products.views.basket.subscribe')
        self.mock_subscribe = patcher.start()
        self.addCleanup(patcher.stop)

    def _request(self, data, expected_status=200, locale='en-US'):
        req = RequestFactory().post('/', data)
        req.locale = locale
        resp = views.vpn_invite_waitlist(req)
        assert resp.status_code == expected_status
        return json.loads(resp.content)

    def test_form_success(self):
        resp_data = self._request({
            'newsletters': 'guardian-vpn-waitlist',
            'email': 'test@example.com',
            'country': 'us',
            'privacy': True,
            'fmt': 'H',
            'lang': 'en'
        })
        assert resp_data['success']
        self.mock_subscribe.assert_called_with(
            email='test@example.com',
            fpn_country='us',
            fpn_platform='',
            lang='en',
            newsletters='guardian-vpn-waitlist'
        )

    def test_invalid_email(self):
        resp_data = self._request({
            'newsletters': 'guardian-vpn-waitlist',
            'email': 'invalid.email',
            'country': 'us',
            'privacy': True,
            'fmt': 'H',
            'lang': 'en'
        })
        assert not resp_data['success']
        assert 'Please enter a valid email address' in resp_data['errors']
        assert not self.mock_subscribe.called

    def test_invalid_country(self):
        resp_data = self._request({
            'newsletters': 'guardian-vpn-waitlist',
            'email': 'test@example.com',
            'country': 'zzzz',
            'privacy': True,
            'fmt': 'H',
            'lang': 'en'
        })
        assert not resp_data['success']
        assert 'Select a valid choice. zzzz is not one of the available choices.' in resp_data['errors']
        assert not self.mock_subscribe.called

    def test_platforms(self):
        resp_data = self._request({
            'newsletters': 'guardian-vpn-waitlist',
            'email': 'test@example.com',
            'country': 'us',
            'platforms': ['windows', 'android'],
            'privacy': True,
            'fmt': 'H',
            'lang': 'en'
        })
        assert resp_data['success']
        self.mock_subscribe.assert_called_with(
            email='test@example.com',
            fpn_country='us',
            fpn_platform='windows,android',
            lang='en',
            newsletters='guardian-vpn-waitlist'
        )

@patch('bedrock.products.views.l10n_utils.render', return_value=HttpResponse())
class TestVPNLandingPage(TestCase):
    def test_vpn_landing_page_template(self, render_mock):
        req = RequestFactory().get('/products/vpn/')
        req.locale = 'en-US'
        view = views.vpn_landing_page
        view(req)
        template = render_mock.call_args[0][1]
        assert template == 'products/vpn/landing.html'

    def test_vpn_landing_page_variant_a_template(self, render_mock):
        req = RequestFactory().get('/products/vpn/?entrypoint_experiment=vpn-landing-page-cta-change&entrypoint_variation=a')
        req.locale = 'en-US'
        view = views.vpn_landing_page
        view(req)
        template = render_mock.call_args[0][1]
        assert template == 'products/vpn/variations/cta-a.html'

    def test_vpn_landing_page_variant_b_template(self, render_mock):
        req = RequestFactory().get('/products/vpn/?entrypoint_experiment=vpn-landing-page-cta-change&entrypoint_variation=b')
        req.locale = 'en-US'
        view = views.vpn_landing_page
        view(req)
        template = render_mock.call_args[0][1]
        assert template == 'products/vpn/variations/cta-b.html'
