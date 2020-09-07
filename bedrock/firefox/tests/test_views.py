# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
from urllib.parse import parse_qs

from django.core import mail
from django.test import override_settings
from django.test.client import RequestFactory

import querystringsafe_base64
from mock import patch, ANY
from pyquery import PyQuery as pq

from bedrock.firefox import views
from bedrock.firefox.forms import UnfckForm
from bedrock.mozorg.tests import TestCase
from bedrock.base.urlresolvers import reverse


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
        non-ascii domain names in the referrer. The allowed list for bouncer
        doesn't include any such domains anyway, so we should just ignore them.
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
    @patch.dict(os.environ, SWITCH_NEW_REDESIGN='True')
    @patch.object(views, 'ftl_file_is_active', lambda *x: True)
    def test_download_template(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'en-US'
        view = views.NewView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ['firefox/new/desktop/download.html']

    @patch.dict(os.environ, SWITCH_NEW_REDESIGN='True')
    @patch.object(views, 'ftl_file_is_active', lambda *x: True)
    def test_thanks_template(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/')
        req.locale = 'en-US'
        view = views.DownloadThanksView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ['firefox/new/desktop/thanks.html']

    @patch.dict(os.environ, SWITCH_NEW_REDESIGN='True')
    @patch.object(views, 'ftl_file_is_active', lambda *x: False)
    def test_download_old_template(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'de'
        view = views.NewView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ['firefox/new/trailhead/download.html']

    @patch.dict(os.environ, SWITCH_NEW_REDESIGN='True')
    @patch.object(views, 'ftl_file_is_active', lambda *x: False)
    def test_thanks_old_template(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/')
        req.locale = 'de'
        view = views.DownloadThanksView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ['firefox/new/trailhead/thanks.html']

    def test_thanks_redirect(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&dude=abides')
        req.locale = 'en-US'
        view = views.NewView.as_view()
        resp = view(req)
        assert resp.status_code == 301
        assert resp['location'].endswith(
            '/firefox/download/thanks/?scene=2&dude=abides'
        )

    # yandex - issue 5635

    @patch.dict(os.environ, SWITCH_FIREFOX_YANDEX='True')
    def test_yandex_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'ru'
        view = views.NewView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ['firefox/new/trailhead/download-yandex.html']

    @patch.dict(os.environ, SWITCH_FIREFOX_YANDEX='False')
    @patch.object(views, 'ftl_file_is_active', lambda *x: True)
    def test_yandex_scene_1_switch_off(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'ru'
        view = views.NewView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ['firefox/new/trailhead/download.html']


class TestFirefoxNewNoIndex(TestCase):
    def test_download_noindex(self):
        # Scene 1 of /firefox/new/ should never contain a noindex tag.
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'en-US'
        view = views.NewView.as_view()
        response = view(req)
        doc = pq(response.content)
        robots = doc('meta[name="robots"]')
        assert robots.length == 0

    def test_thanks_canonical(self):
        # Scene 2 /firefox/download/thanks/ should always contain a noindex tag.
        req = RequestFactory().get('/firefox/download/thanks/')
        req.locale = 'en-US'
        view = views.DownloadThanksView.as_view()
        response = view(req)
        doc = pq(response.content)
        robots = doc('meta[name="robots"]')
        assert robots.length == 1
        assert 'noindex' in robots.attr('content')


class TestFirefoxHome(TestCase):
    @patch('bedrock.firefox.views.l10n_utils.render')
    def test_firefox_home(self, render_mock):
        req = RequestFactory().get('/firefox/')
        req.locale = 'en-US'
        view = views.FirefoxHomeView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ['firefox/home/index-master.html']

    @patch('bedrock.firefox.views.l10n_utils.render')
    @patch.object(views, 'ftl_file_is_active', lambda *x: False)
    def test_firefox_home_legacy(self, render_mock):
        req = RequestFactory().get('/firefox/')
        req.locale = 'fr'
        view = views.FirefoxHomeView.as_view()
        view(req)
        template = render_mock.call_args[0][1]
        assert template == ['firefox/home/index-quantum.html']


class TestFirefoxWelcomePage1(TestCase):
    @patch('bedrock.firefox.views.l10n_utils.render')
    def test_firefox_welcome_page1(self, render_mock):
        req = RequestFactory().get('/firefox/welcome/1/')
        req.locale = 'en-US'
        views.firefox_welcome_page1(req)
        render_mock.assert_called_once_with(req, 'firefox/welcome/page1.html', ANY,
                                            ftl_files='firefox/welcome/page1')


class TestUnfckForm(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = views.FirefoxUnfckView.as_view()
        with self.activate('en-US'):
            self.url = reverse('firefox.campaign.unfck')

        self.data = {
            'unfck_field': 'test message'
        }

    def tearDown(self):
        mail.outbox = []

    def test_view_post_valid_data(self):
        """
        A valid POST should 302 redirect.
        """
        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        response = self.view(request)

        assert response.status_code == 302
        assert response['Location'] == '/en-US/firefox/campaign/unfck/?success=True'

    def test_view_post_missing_data(self):
        """
        POST with missing data should return 200 and contain form
        errors in the template.
        """

        self.data.update(unfck_field='')  # remove required field

        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        response = self.view(request)

        assert response.status_code == 200
        self.assertIn(b'An error has occurred with your submission.', response.content)

    def test_view_post_honeypot(self):
        """
        POST with honeypot text box filled should return 200 and
        contain general form error message.
        """

        self.data['office_fax'] = 'spammer'

        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        response = self.view(request)

        assert response.status_code == 200
        self.assertIn(b'An error has occurred with your submission.', response.content)

    def test_form_valid_data(self):
        """
        Form should be valid.
        """
        form = UnfckForm(self.data)

        # make sure form is valid
        assert form.is_valid()

    def test_form_missing_data(self):
        """
        With incorrect data (missing email), form should not be valid
        """
        self.data.update(unfck_field='')

        form = UnfckForm(self.data)

        # make sure form is invalid
        assert not form.is_valid()

    def test_form_honeypot(self):
        """
        Form with honeypot text box filled should not be valid.
        """
        self.data['office_fax'] = 'spammer'

        form = UnfckForm(self.data)

        assert not form.is_valid()

    @patch('bedrock.firefox.views.render_to_string',
           return_value='rendered')
    @patch('bedrock.firefox.views.EmailMessage')
    def test_email(self, mock_email_message, mock_render_to_string):
        """
        Make sure email is sent with expected values.
        """
        mock_send = mock_email_message.return_value.send

        # create POST request
        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        # submit POST request
        self.view(request)

        # make sure email was sent
        mock_send.assert_called_once_with()

        # make sure email values are correct
        mock_email_message.assert_called_once_with(
            views.UNFCK_EMAIL_SUBJECT,
            'rendered',
            views.UNFCK_EMAIL_FROM,
            views.UNFCK_EMAIL_TO)
