# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
from urllib.parse import parse_qs

from django.test import override_settings
from django.test.client import RequestFactory

import querystringsafe_base64
from mock import patch, ANY
from pyquery import PyQuery as pq

from bedrock.firefox import views
from bedrock.mozorg.tests import TestCase


@override_settings(
    STUB_ATTRIBUTION_HMAC_KEY='achievers',
    STUB_ATTRIBUTION_RATE=1,
    STUB_ATTRIBUTION_MAX_LEN=600,
)
class TestStubAttributionCode(TestCase):
    def _get_request(self, params):
        rf = RequestFactory()
        return rf.get(
            '/',
            params,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_ACCEPT='application/json',
        )

    def test_not_ajax_request(self):
        req = RequestFactory().get('/', {'source': 'malibu'})
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 400)
        assert 'cache-control' not in resp
        data = json.loads(resp.content)
        self.assertEqual(data['error'], 'Resource only available via XHR')

    def test_no_valid_param_names(self):
        final_params = {
            'source': 'www.mozilla.org',
            'medium': '(none)',
            'campaign': '(not set)',
            'content': '(not set)',
            'experiment': '(not set)',
            'variation': '(not set)',
            'ua': '(not set)',
        }
        req = self._get_request({'dude': 'abides'})
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(
            querystringsafe_base64.decode(data['attribution_code'].encode()).decode()
        )
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data['attribution_sig'],
            'e0eff8af228709c6f99d8a57699e36e8152698146e0992c7f491e91905eec5f4',
        )

    def test_no_valid_param_data(self):
        params = {'utm_source': 'br@ndt', 'utm_medium': 'ae<t>her', 'experiment': 'dfb</p>s', 'variation': 'ef&bvcv'}
        final_params = {
            'source': 'www.mozilla.org',
            'medium': '(none)',
            'campaign': '(not set)',
            'content': '(not set)',
            'experiment': '(not set)',
            'variation': '(not set)',
            'ua': '(not set)',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(
            querystringsafe_base64.decode(data['attribution_code'].encode()).decode()
        )
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data['attribution_sig'],
            'e0eff8af228709c6f99d8a57699e36e8152698146e0992c7f491e91905eec5f4',
        )

    def test_some_valid_param_data(self):
        params = {'utm_source': 'brandt', 'utm_content': 'ae<t>her'}
        final_params = {
            'source': 'brandt',
            'medium': '(direct)',
            'campaign': '(not set)',
            'content': '(not set)',
            'experiment': '(not set)',
            'variation': '(not set)',
            'ua': '(not set)',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(
            querystringsafe_base64.decode(data['attribution_code'].encode()).decode()
        )
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data['attribution_sig'],
            '248b763a1848f0a5e4a4ce169b38c5810511b198aed731091e065b8fd6b02e23',
        )

    def test_campaign_data_too_long(self):
        """If the code is too long then the utm_campaign value should be truncated"""
        params = {
            'utm_source': 'brandt',
            'utm_medium': 'aether',
            'utm_content': 'A144_A000_0000000',
            'utm_campaign': 'The%7cDude%7cabides%7cI%7cdont%7cknow%7cabout%7cyou%7c'
            'but%7cI%7ctake%7ccomfort%7cin%7cthat' * 6,
            'experiment': '(not set)',
            'variation': '(not set)',
            'ua': 'chrome',
        }
        final_params = {
            'source': 'brandt',
            'medium': 'aether',
            'campaign': 'The|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in'
            '|thatThe|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in|thatThe'
            '|Dude|abides|I|dont|know|about|you|but|I|take|comfort|in|thatThe|Dude|abides'
            '|I|dont|know|about|you|but|I|take|comfort|in|thatThe|Dude|abides|I|dont|know'
            '|about|you|but|I|take|comfort|in|thatThe|Dude|abides|I|dont|_',
            'content': 'A144_A000_0000000',
            'experiment': '(not set)',
            'variation': '(not set)',
            'ua': 'chrome',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        code = querystringsafe_base64.decode(data['attribution_code'].encode()).decode()
        assert len(code) <= 600
        attrs = parse_qs(code)
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data['attribution_sig'],
            'ed35e1ed1167806f7744bdbb62c4e1d781c8800df6f2dca09fe63877caa9e167',
        )

    def test_other_data_too_long_not_campaign(self):
        """If the code is too long but not utm_campaign return error"""
        params = {
            'utm_source': 'brandt',
            'utm_campaign': 'dude',
            'utm_content': 'A144_A000_0000000',
            'utm_medium': 'The%7cDude%7cabides%7cI%7cdont%7cknow%7cabout%7cyou%7c'
            'but%7cI%7ctake%7ccomfort%7cin%7cthat' * 6,
        }
        final_params = {'error': 'Invalid code'}
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 400)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        self.assertDictEqual(data, final_params)

    def test_returns_valid_data(self):
        params = {'utm_source': 'brandt', 'utm_medium': 'aether', 'experiment': 'firefox-new', 'variation': '1', 'ua': 'chrome'}
        final_params = {
            'source': 'brandt',
            'medium': 'aether',
            'campaign': '(not set)',
            'content': '(not set)',
            'experiment': 'firefox-new',
            'variation': '1',
            'ua': 'chrome',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(
            querystringsafe_base64.decode(data['attribution_code'].encode()).decode()
        )
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data['attribution_sig'],
            '8987babc249a7128b3cd32b11623645cc490ae1709e560249176a2622f288a79',
        )

    def test_handles_referrer(self):
        params = {'utm_source': 'brandt', 'referrer': 'https://duckduckgo.com/privacy'}
        final_params = {
            'source': 'brandt',
            'medium': '(direct)',
            'campaign': '(not set)',
            'content': '(not set)',
            'experiment': '(not set)',
            'variation': '(not set)',
            'ua': '(not set)',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(
            querystringsafe_base64.decode(data['attribution_code'].encode()).decode()
        )
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data['attribution_sig'],
            '248b763a1848f0a5e4a4ce169b38c5810511b198aed731091e065b8fd6b02e23',
        )

    def test_handles_referrer_no_source(self):
        params = {
            'referrer': 'https://example.com:5000/searchin',
            'utm_medium': 'aether',
        }
        final_params = {
            'source': 'example.com:5000',
            'medium': 'referral',
            'campaign': '(not set)',
            'content': '(not set)',
            'experiment': '(not set)',
            'variation': '(not set)',
            'ua': '(not set)',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(
            querystringsafe_base64.decode(data['attribution_code'].encode()).decode()
        )
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data['attribution_sig'],
            '70461f833cc24a4c16a68fda95629c3f5d6bb377d64ae032679a49b4de016679',
        )

    def test_handles_referrer_utf8(self):
        """Should ignore non-ascii domain names.

        We were getting exceptions when the view was trying to base64 encode
        non-ascii domain names in the referrer. The whitelist for bouncer doesn't
        include any such domains anyway, so we should just ignore them.
        """
        params = {'referrer': 'http://youtubê.com/sorry/'}
        final_params = {
            'source': 'www.mozilla.org',
            'medium': '(none)',
            'campaign': '(not set)',
            'content': '(not set)',
            'experiment': '(not set)',
            'variation': '(not set)',
            'ua': '(not set)',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(
            querystringsafe_base64.decode(data['attribution_code'].encode()).decode()
        )
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(
            data['attribution_sig'],
            'e0eff8af228709c6f99d8a57699e36e8152698146e0992c7f491e91905eec5f4',
        )

    @override_settings(STUB_ATTRIBUTION_RATE=0.2)
    def test_rate_limit(self):
        params = {'utm_source': 'brandt', 'utm_medium': 'aether'}
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'

    @override_settings(STUB_ATTRIBUTION_RATE=0)
    def test_rate_limit_disabled(self):
        params = {'utm_source': 'brandt', 'utm_medium': 'aether'}
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 429)
        assert resp['cache-control'] == 'max-age=300'

    @override_settings(STUB_ATTRIBUTION_HMAC_KEY='')
    def test_no_hmac_key_set(self):
        params = {'utm_source': 'brandt', 'utm_medium': 'aether'}
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 403)
        assert resp['cache-control'] == 'max-age=300'


class TestSendToDeviceView(TestCase):
    def setUp(self):
        patcher = patch('bedrock.firefox.views.basket.subscribe')
        self.mock_subscribe = patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch('bedrock.firefox.views.basket.request')
        self.mock_send_sms = patcher.start()
        self.addCleanup(patcher.stop)

    def _request(self, data, expected_status=200, locale='en-US'):
        req = RequestFactory().post('/', data)
        req.locale = locale
        resp = views.send_to_device_ajax(req)
        assert resp.status_code == expected_status
        return json.loads(resp.content)

    def test_phone_or_email_required(self):
        resp_data = self._request({'platform': 'android'})
        assert not resp_data['success']
        assert 'phone-or-email' in resp_data['errors']
        assert not self.mock_send_sms.called
        assert not self.mock_subscribe.called

    def test_send_android_sms(self):
        resp_data = self._request(
            {'platform': 'android', 'phone-or-email': '5558675309'}
        )
        assert resp_data['success']
        self.mock_send_sms.assert_called_with(
            'post',
            'subscribe_sms',
            data={
                'mobile_number': '5558675309',
                'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms'][
                    'android'
                ],
                'lang': 'en-US',
            },
        )

    def test_send_android_sms_non_en_us(self):
        resp_data = self._request(
            {'platform': 'android', 'phone-or-email': '015558675309'}, locale='de'
        )
        assert resp_data['success']
        self.mock_send_sms.assert_called_with(
            'post',
            'subscribe_sms',
            data={
                'mobile_number': '015558675309',
                'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms'][
                    'android'
                ],
                'lang': 'de',
            },
        )

    def test_send_android_sms_with_country(self):
        resp_data = self._request(
            {'platform': 'android', 'phone-or-email': '5558675309', 'country': 'de'}
        )
        assert resp_data['success']
        self.mock_send_sms.assert_called_with(
            'post',
            'subscribe_sms',
            data={
                'mobile_number': '5558675309',
                'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms'][
                    'android'
                ],
                'lang': 'en-US',
                'country': 'de',
            },
        )

    def test_send_android_sms_with_invalid_country(self):
        resp_data = self._request(
            {'platform': 'android', 'phone-or-email': '5558675309', 'country': 'X2'}
        )
        assert resp_data['success']
        self.mock_send_sms.assert_called_with(
            'post',
            'subscribe_sms',
            data={
                'mobile_number': '5558675309',
                'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms'][
                    'android'
                ],
                'lang': 'en-US',
            },
        )

        resp_data = self._request(
            {'platform': 'android', 'phone-or-email': '5558675309', 'country': 'dude'}
        )
        assert resp_data['success']
        self.mock_send_sms.assert_called_with(
            'post',
            'subscribe_sms',
            data={
                'mobile_number': '5558675309',
                'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms'][
                    'android'
                ],
                'lang': 'en-US',
            },
        )

    def test_send_android_sms_basket_error(self):
        self.mock_send_sms.side_effect = views.basket.BasketException
        resp_data = self._request(
            {'platform': 'android', 'phone-or-email': '5558675309'}, 400
        )
        assert not resp_data['success']
        assert 'system' in resp_data['errors']

    def test_send_bad_sms_number(self):
        self.mock_send_sms.side_effect = views.basket.BasketException(
            'mobile_number is invalid'
        )
        resp_data = self._request({'platform': 'android', 'phone-or-email': '555'})
        assert not resp_data['success']
        assert 'number' in resp_data['errors']

    def test_send_android_email(self):
        resp_data = self._request(
            {
                'platform': 'android',
                'phone-or-email': 'dude@example.com',
                'source-url': 'https://nihilism.info',
            }
        )
        assert resp_data['success']
        self.mock_subscribe.assert_called_with(
            'dude@example.com',
            views.SEND_TO_DEVICE_MESSAGE_SETS['default']['email']['android'],
            source_url='https://nihilism.info',
            lang='en-US',
        )

    def test_send_android_email_basket_error(self):
        self.mock_subscribe.side_effect = views.basket.BasketException
        resp_data = self._request(
            {
                'platform': 'android',
                'phone-or-email': 'dude@example.com',
                'source-url': 'https://nihilism.info',
            },
            400,
        )
        assert not resp_data['success']
        assert 'system' in resp_data['errors']

    def test_send_android_bad_email(self):
        resp_data = self._request(
            {
                'platform': 'android',
                'phone-or-email': '@example.com',
                'source-url': 'https://nihilism.info',
            }
        )
        assert not resp_data['success']
        assert 'email' in resp_data['errors']
        assert not self.mock_subscribe.called

    # an invalid value for 'message-set' should revert to 'default' message set
    def test_invalid_message_set(self):
        resp_data = self._request(
            {
                'platform': 'ios',
                'phone-or-email': '5558675309',
                'message-set': 'the-dude-is-not-in',
            }
        )
        assert resp_data['success']
        self.mock_send_sms.assert_called_with(
            'post',
            'subscribe_sms',
            data={
                'mobile_number': '5558675309',
                'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms']['ios'],
                'lang': 'en-US',
            },
        )

    # /firefox/android/ embedded widget (bug 1221328)
    def test_android_embedded_email(self):
        resp_data = self._request(
            {
                'platform': 'android',
                'phone-or-email': 'dude@example.com',
                'message-set': 'fx-android',
            }
        )
        assert resp_data['success']
        self.mock_subscribe.assert_called_with(
            'dude@example.com',
            views.SEND_TO_DEVICE_MESSAGE_SETS['fx-android']['email']['android'],
            source_url=None,
            lang='en-US',
        )

    def test_android_embedded_sms(self):
        resp_data = self._request(
            {
                'platform': 'android',
                'phone-or-email': '5558675309',
                'message-set': 'fx-android',
            }
        )
        assert resp_data['success']
        self.mock_send_sms.assert_called_with(
            'post',
            'subscribe_sms',
            data={
                'mobile_number': '5558675309',
                'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['fx-android']['sms'][
                    'android'
                ],
                'lang': 'en-US',
            },
        )

    # /firefox/mobile-download/desktop
    def test_fx_mobile_download_desktop_email(self):
        resp_data = self._request(
            {
                'phone-or-email': 'dude@example.com',
                'message-set': 'fx-mobile-download-desktop',
            }
        )
        assert resp_data['success']
        self.mock_subscribe.assert_called_with(
            'dude@example.com',
            views.SEND_TO_DEVICE_MESSAGE_SETS['fx-mobile-download-desktop']['email'][
                'all'
            ],
            source_url=None,
            lang='en-US',
        )

    def test_fx_mobile_download_desktop_sms(self):
        resp_data = self._request(
            {
                'phone-or-email': '5558675309',
                'message-set': 'fx-mobile-download-desktop',
            }
        )
        assert resp_data['success']
        self.mock_send_sms.assert_called_with(
            'post',
            'subscribe_sms',
            data={
                'mobile_number': '5558675309',
                'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS[
                    'fx-mobile-download-desktop'
                ]['sms']['all'],
                'lang': 'en-US',
            },
        )

    def test_sms_number_with_punctuation(self):
        resp_data = self._request(
            {
                'phone-or-email': '(555) 867-5309',
                'message-set': 'fx-mobile-download-desktop',
            }
        )
        assert resp_data['success']
        self.mock_send_sms.assert_called_with(
            'post',
            'subscribe_sms',
            data={
                'mobile_number': '5558675309',
                'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS[
                    'fx-mobile-download-desktop'
                ]['sms']['all'],
                'lang': 'en-US',
            },
        )

    def test_sms_number_too_long(self):
        resp_data = self._request(
            {
                'phone-or-email': '5558675309555867530912',
                'message-set': 'fx-mobile-download-desktop',
            }
        )
        assert not resp_data['success']
        self.mock_send_sms.assert_not_called()
        assert 'number' in resp_data['errors']

    def test_sms_number_too_short(self):
        resp_data = self._request(
            {'phone-or-email': '555', 'message-set': 'fx-mobile-download-desktop'}
        )
        assert not resp_data['success']
        self.mock_send_sms.assert_not_called()
        assert 'number' in resp_data['errors']


@override_settings(DEV=False)
@patch('bedrock.firefox.views.l10n_utils.render')
class TestFirefoxNew(TestCase):
    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_download_template(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(
            req, 'firefox/new/trailhead/download.html', ANY
        )

    @patch.object(views, 'lang_file_is_active', lambda *x: False)
    def test_download_old_template(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html', ANY)

    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_thanks_template(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/new/trailhead/thanks.html', ANY
        )

    @patch.object(views, 'lang_file_is_active', lambda *x: False)
    def test_thanks_old_template(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html', ANY)

    def test_thanks_redirect(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&dude=abides')
        req.locale = 'en-US'
        resp = views.new(req)
        assert resp.status_code == 301
        assert resp['location'].endswith(
            '/firefox/download/thanks/?scene=2&dude=abides'
        )

    # yandex - issue 5635

    @patch.dict(os.environ, SWITCH_FIREFOX_YANDEX='True')
    def test_yandex_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'ru'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/download-yandex.html', ANY)

    @patch.dict(os.environ, SWITCH_FIREFOX_YANDEX='False')
    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_yandex_scene_1_switch_off(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'ru'
        views.new(req)
        render_mock.assert_called_once_with(
            req, 'firefox/new/trailhead/download.html', ANY
        )


class TestFirefoxNewNoIndex(TestCase):
    def test_download_noindex(self):
        # Scene 1 of /firefox/new/ should never contain a noindex tag.
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'en-US'
        response = views.new(req)
        doc = pq(response.content)
        robots = doc('meta[name="robots"]')
        assert robots.length == 0

    def test_thanks_canonical(self):
        # Scene 2 /firefox/download/thanks/ should always contain a noindex tag.
        req = RequestFactory().get('/firefox/download/thanks/')
        req.locale = 'en-US'
        response = views.download_thanks(req)
        doc = pq(response.content)
        robots = doc('meta[name="robots"]')
        assert robots.length == 1
        assert 'noindex' in robots.attr('content')


@override_settings(DEV=False)
@patch('bedrock.firefox.views.l10n_utils.render')
class TestFirefoxCampaign(TestCase):
    def test_scene_1_template(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/')
        req.locale = 'en-US'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/index-trailhead.html', ANY
        )

    # berlin campaign bug 1447445 + 3 berlin variations bug 1473357

    # berlin
    def test_berlin_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=berlin')
        req.locale = 'de'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene1.html', ANY
        )

    def test_berlin_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=berlin')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene2.html', ANY
        )

    def test_berlin_nonde_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=berlin')
        req.locale = 'en-US'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/index-trailhead.html', ANY
        )

    def test_berlin_nonde_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=berlin')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/new/trailhead/thanks.html', ANY
        )

    # herz
    def test_variation_herz_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=herz')
        req.locale = 'de'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene1-herz.html', ANY
        )

    def test_variation_herz_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=herz')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene2-herz.html', ANY
        )

    def test_variation_herz_nonde_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=herz')
        req.locale = 'en-US'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/index-trailhead.html', ANY
        )

    def test_variation_herz_nonde_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=herz')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/new/trailhead/thanks.html', ANY
        )

    # geschwindigkeit
    def test_variation_speed_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=geschwindigkeit')
        req.locale = 'de'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene1-gesch.html', ANY
        )

    def test_variation_speed_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=geschwindigkeit')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene2-gesch.html', ANY
        )

    def test_variation_speed_nonde_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=geschwindigkeit')
        req.locale = 'en-US'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/index-trailhead.html', ANY
        )

    def test_variation_speed_nonde_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=geschwindigkeit')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/new/trailhead/thanks.html', ANY
        )

    # privatsphare
    def test_variation_privacy_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=privatsphare')
        req.locale = 'de'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene1-privat.html', ANY
        )

    def test_variation_privacy_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=privatsphare')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene2-privat.html', ANY
        )

    def test_variation_privacy_nonde_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=privatsphare')
        req.locale = 'en-US'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/index-trailhead.html', ANY
        )

    def test_variation_privacy_nonde_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=privatsphare')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/new/trailhead/thanks.html', ANY
        )

    # auf-deiner-seite
    def test_variation_oys_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=auf-deiner-seite')
        req.locale = 'de'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene1-auf-deiner-seite.html', ANY
        )

    def test_variation_oys_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=auf-deiner-seite')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene2-auf-deiner-seite.html', ANY
        )

    def test_variation_oys_nonde_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=auf-deiner-seite')
        req.locale = 'en-US'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/index-trailhead.html', ANY
        )

    def test_variation_oys_nonde_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=auf-deiner-seite')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/new/trailhead/thanks.html', ANY
        )

    # berlin video test issue 5637

    def test_berlin_video_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=aus-gruenden')
        req.locale = 'de'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene1-aus-gruenden.html', ANY
        )

    def test_berlin_video_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=aus-gruenden')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/berlin/scene2-aus-gruenden.html', ANY
        )

    # better browser test issue 5841

    def test_better_browser_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=betterbrowser')
        req.locale = 'en-US'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/better-browser/scene1.html', ANY
        )

    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_better_browser_scene_1_non_us(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=betterbrowser')
        req.locale = 'de'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/index-trailhead.html', ANY
        )

    def test_better_browser_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=betterbrowser')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/better-browser/scene2.html', ANY
        )

    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_better_browser_scene_2_non_us(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=betterbrowser')
        req.locale = 'fr'
        views.download_thanks(req)
        render_mock.assert_called_once_with(
            req, 'firefox/new/trailhead/thanks.html', ANY
        )

    # Safari SEM campaign bug #1479085

    def test_compare_safari_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=safari')
        req.locale = 'en-US'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/compare/scene1-safari.html', ANY
        )

    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_compare_safari_scene_1_non_us(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=safari')
        req.locale = 'fr'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/index-trailhead.html', ANY
        )

    # Edge SEM campaign Bug #1479086

    def test_compare_edge_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=edge')
        req.locale = 'en-US'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/compare/scene1-edge.html', ANY
        )

    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_compare_edge_scene_1_non_us(self, render_mock):
        req = RequestFactory().get('/firefox/campaign/?xv=edge')
        req.locale = 'fr'
        views.campaign(req)
        render_mock.assert_called_once_with(
            req, 'firefox/campaign/index-trailhead.html', ANY
        )


class TestFirefoxHome(TestCase):
    @patch('bedrock.firefox.views.l10n_utils.render')
    def test_firefox_home(self, render_mock):
        req = RequestFactory().get('/firefox/')
        req.locale = 'en-US'
        views.firefox_home(req)
        render_mock.assert_called_once_with(req, 'firefox/home/index-master.html')

    @patch('bedrock.firefox.views.l10n_utils.render')
    @patch.object(views, 'lang_file_is_active', lambda *x: False)
    def test_firefox_home_legacy(self, render_mock):
        req = RequestFactory().get('/firefox/')
        req.locale = 'fr'
        views.firefox_home(req)
        render_mock.assert_called_once_with(req, 'firefox/home/index-quantum.html')


class TestFirefoxWelcomePage1(TestCase):
    @patch('bedrock.firefox.views.l10n_utils.render')
    def test_firefox_welcome_page1(self, render_mock):
        req = RequestFactory().get('/firefox/welcome/1/')
        req.locale = 'en-US'
        views.firefox_welcome_page1(req)
        render_mock.assert_called_once_with(req, 'firefox/welcome/page1.html', ANY)
