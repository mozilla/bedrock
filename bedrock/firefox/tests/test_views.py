# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
from urlparse import parse_qs

from django.test import override_settings
from django.test.client import RequestFactory

import querystringsafe_base64
from mock import patch, Mock, ANY
from nose.tools import eq_, ok_
from pyquery import PyQuery as pq

from bedrock.firefox import views
from bedrock.mozorg.tests import TestCase


@override_settings(STUB_ATTRIBUTION_HMAC_KEY='achievers',
                   STUB_ATTRIBUTION_RATE=1)
@patch.object(views, 'time', Mock(return_value=12345.678))
class TestStubAttributionCode(TestCase):
    def _get_request(self, params):
        rf = RequestFactory()
        return rf.get('/', params,
                      HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                      HTTP_ACCEPT='application/json')

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
            'timestamp': '12345',
        }
        req = self._get_request({'dude': 'abides'})
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data['attribution_code']))
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(data['attribution_sig'],
                         '153c1e8b7d4a582fa245d57d9c28ca9d6bcb65957e41924f826f1e7a5a2f8de9')

    def test_no_valid_param_data(self):
        params = {'utm_source': 'br@ndt', 'utm_medium': 'ae<t>her'}
        final_params = {
            'source': 'www.mozilla.org',
            'medium': '(none)',
            'campaign': '(not set)',
            'content': '(not set)',
            'timestamp': '12345',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data['attribution_code']))
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(data['attribution_sig'],
                         '153c1e8b7d4a582fa245d57d9c28ca9d6bcb65957e41924f826f1e7a5a2f8de9')

    def test_some_valid_param_data(self):
        params = {'utm_source': 'brandt', 'utm_content': 'ae<t>her'}
        final_params = {
            'source': 'brandt',
            'medium': '(direct)',
            'campaign': '(not set)',
            'content': '(not set)',
            'timestamp': '12345',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data['attribution_code']))
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(data['attribution_sig'],
                         'bd6c54115eb1f331b64bec83225a667fa0e16090d7d6abb33dab6305cd858a9d')

    def test_returns_valid_data(self):
        params = {'utm_source': 'brandt', 'utm_medium': 'aether'}
        final_params = {
            'source': 'brandt',
            'medium': 'aether',
            'campaign': '(not set)',
            'content': '(not set)',
            'timestamp': '12345',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data['attribution_code']))
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(data['attribution_sig'],
                         'ab55c9b24e230f08d3ad50bf9a3a836ef4405cfb6919cb1df8efe208be38e16d')

    def test_handles_referrer(self):
        params = {'utm_source': 'brandt', 'referrer': 'https://duckduckgo.com/privacy'}
        final_params = {
            'source': 'brandt',
            'medium': '(direct)',
            'campaign': '(not set)',
            'content': '(not set)',
            'timestamp': '12345',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data['attribution_code']))
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(data['attribution_sig'],
                         'bd6c54115eb1f331b64bec83225a667fa0e16090d7d6abb33dab6305cd858a9d')

    def test_handles_referrer_no_source(self):
        params = {'referrer': 'https://example.com:5000/searchin', 'utm_medium': 'aether'}
        final_params = {
            'source': 'example.com:5000',
            'medium': 'referral',
            'campaign': '(not set)',
            'content': '(not set)',
            'timestamp': '12345',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data['attribution_code']))
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(data['attribution_sig'],
                         '6b3dbb178e9abc22db66530df426b17db8590e8251fc153ba443e81ca60e355e')

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
            'timestamp': '12345',
        }
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 200)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        # will it blend?
        attrs = parse_qs(querystringsafe_base64.decode(data['attribution_code']))
        # parse_qs returns a dict with lists for values
        attrs = {k: v[0] for k, v in attrs.items()}
        self.assertDictEqual(attrs, final_params)
        self.assertEqual(data['attribution_sig'],
                         '153c1e8b7d4a582fa245d57d9c28ca9d6bcb65957e41924f826f1e7a5a2f8de9')

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
        eq_(resp.status_code, expected_status)
        return json.loads(resp.content)

    def test_phone_or_email_required(self):
        resp_data = self._request({
            'platform': 'android',
        })
        ok_(not resp_data['success'])
        ok_('phone-or-email' in resp_data['errors'])
        ok_(not self.mock_send_sms.called)
        ok_(not self.mock_subscribe.called)

    def test_send_android_sms(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '5558675309',
        })
        ok_(resp_data['success'])
        self.mock_send_sms.assert_called_with('post', 'subscribe_sms', data={
            'mobile_number': '5558675309',
            'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms']['android'],
            'lang': 'en-US',
        })

    def test_send_android_sms_non_en_us(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '015558675309',
        }, locale='de')
        ok_(resp_data['success'])
        self.mock_send_sms.assert_called_with('post', 'subscribe_sms', data={
            'mobile_number': '015558675309',
            'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms']['android'],
            'lang': 'de',
        })

    def test_send_android_sms_with_country(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '5558675309',
            'country': 'de',
        })
        ok_(resp_data['success'])
        self.mock_send_sms.assert_called_with('post', 'subscribe_sms', data={
            'mobile_number': '5558675309',
            'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms']['android'],
            'lang': 'en-US',
            'country': 'de',
        })

    def test_send_android_sms_with_invalid_country(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '5558675309',
            'country': 'X2',
        })
        ok_(resp_data['success'])
        self.mock_send_sms.assert_called_with('post', 'subscribe_sms', data={
            'mobile_number': '5558675309',
            'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms']['android'],
            'lang': 'en-US',
        })

        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '5558675309',
            'country': 'dude',
        })
        ok_(resp_data['success'])
        self.mock_send_sms.assert_called_with('post', 'subscribe_sms', data={
            'mobile_number': '5558675309',
            'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms']['android'],
            'lang': 'en-US',
        })

    def test_send_android_sms_basket_error(self):
        self.mock_send_sms.side_effect = views.basket.BasketException
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '5558675309',
        }, 400)
        ok_(not resp_data['success'])
        ok_('system' in resp_data['errors'])

    def test_send_bad_sms_number(self):
        self.mock_send_sms.side_effect = views.basket.BasketException('mobile_number is invalid')
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '555',
        })
        ok_(not resp_data['success'])
        ok_('number' in resp_data['errors'])

    def test_send_android_email(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': 'dude@example.com',
            'source-url': 'https://nihilism.info',
        })
        ok_(resp_data['success'])
        self.mock_subscribe.assert_called_with('dude@example.com',
                                               views.SEND_TO_DEVICE_MESSAGE_SETS['default']['email']['android'],
                                               source_url='https://nihilism.info',
                                               lang='en-US')

    def test_send_android_email_basket_error(self):
        self.mock_subscribe.side_effect = views.basket.BasketException
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': 'dude@example.com',
            'source-url': 'https://nihilism.info',
        }, 400)
        ok_(not resp_data['success'])
        ok_('system' in resp_data['errors'])

    def test_send_android_bad_email(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '@example.com',
            'source-url': 'https://nihilism.info',
        })
        ok_(not resp_data['success'])
        ok_('email' in resp_data['errors'])
        ok_(not self.mock_subscribe.called)

    # an invalid value for 'message-set' should revert to 'default' message set
    def test_invalid_message_set(self):
        resp_data = self._request({
            'platform': 'ios',
            'phone-or-email': '5558675309',
            'message-set': 'the-dude-is-not-in',
        })
        ok_(resp_data['success'])
        self.mock_send_sms.assert_called_with('post', 'subscribe_sms', data={
            'mobile_number': '5558675309',
            'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms']['ios'],
            'lang': 'en-US',
        })

    # /firefox/android/ embedded widget (bug 1221328)
    def test_android_embedded_email(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': 'dude@example.com',
            'message-set': 'fx-android',
        })
        ok_(resp_data['success'])
        self.mock_subscribe.assert_called_with('dude@example.com',
                                                views.SEND_TO_DEVICE_MESSAGE_SETS['fx-android']['email']['android'],
                                                source_url=None,
                                                lang='en-US')

    def test_android_embedded_sms(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '5558675309',
            'message-set': 'fx-android',
        })
        ok_(resp_data['success'])
        self.mock_send_sms.assert_called_with('post', 'subscribe_sms', data={
            'mobile_number': '5558675309',
            'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['fx-android']['sms']['android'],
            'lang': 'en-US',
        })

    # /firefox/mobile-download/desktop
    def test_fx_mobile_download_desktop_email(self):
        resp_data = self._request({
            'phone-or-email': 'dude@example.com',
            'message-set': 'fx-mobile-download-desktop',
        })
        ok_(resp_data['success'])
        self.mock_subscribe.assert_called_with('dude@example.com',
                                                views.SEND_TO_DEVICE_MESSAGE_SETS['fx-mobile-download-desktop']['email']['all'],
                                                source_url=None,
                                                lang='en-US')

    def test_fx_mobile_download_desktop_sms(self):
        resp_data = self._request({
            'phone-or-email': '5558675309',
            'message-set': 'fx-mobile-download-desktop',
        })
        ok_(resp_data['success'])
        self.mock_send_sms.assert_called_with('post', 'subscribe_sms', data={
            'mobile_number': '5558675309',
            'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['fx-mobile-download-desktop']['sms']['all'],
            'lang': 'en-US',
        })

    def test_sms_number_with_punctuation(self):
        resp_data = self._request({
            'phone-or-email': '(555) 867-5309',
            'message-set': 'fx-mobile-download-desktop',
        })
        ok_(resp_data['success'])
        self.mock_send_sms.assert_called_with('post', 'subscribe_sms', data={
            'mobile_number': '5558675309',
            'msg_name': views.SEND_TO_DEVICE_MESSAGE_SETS['fx-mobile-download-desktop']['sms']['all'],
            'lang': 'en-US',
        })

    def test_sms_number_too_long(self):
        resp_data = self._request({
            'phone-or-email': '5558675309555867530912',
            'message-set': 'fx-mobile-download-desktop',
        })
        ok_(not resp_data['success'])
        self.mock_send_sms.assert_not_called()
        ok_('number' in resp_data['errors'])

    def test_sms_number_too_short(self):
        resp_data = self._request({
            'phone-or-email': '555',
            'message-set': 'fx-mobile-download-desktop',
        })
        ok_(not resp_data['success'])
        self.mock_send_sms.assert_not_called()
        ok_('number' in resp_data['errors'])


@override_settings(DEV=False)
@patch('bedrock.firefox.views.l10n_utils.render')
class TestFirefoxNew(TestCase):
    def test_scene_1_template(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html', ANY)

    def test_scene_2_redirect(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&dude=abides')
        req.locale = 'en-US'
        resp = views.new(req)
        assert resp.status_code == 301
        assert resp['location'].endswith('/firefox/download/thanks/?scene=2&dude=abides')

    def test_scene_2_template(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html')

    # wait face campaign bug 1380044

    def test_wait_face_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=waitface')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/wait-face/scene1.html', ANY)

    def test_wait_face_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=waitface')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/wait-face/scene2.html')

    # reggie watts campaign bug 1413995

    def test_reggie_watts_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=reggiewatts')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/reggie-watts/scene1.html', ANY)

    def test_reggie_watts_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=reggiewatts')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/reggie-watts/scene2.html')

    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_reggie_watts_translated_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=reggiewatts')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/reggie-watts/scene1.html', ANY)

    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_reggie_watts_translated_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=reggiewatts')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/reggie-watts/scene2.html')

    @patch.object(views, 'lang_file_is_active', lambda *x: False)
    def test_reggie_watts_untranslated_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=reggiewatts')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html', ANY)

    @patch.object(views, 'lang_file_is_active', lambda *x: False)
    def test_reggie_watts_untranslated_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=reggiewatts')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html')

    # portland campaign bug 1444000

    def test_portland_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=portland')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene1.html', ANY)

    def test_portland_scene_1_fast(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=portland-fast')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene1-fast.html', ANY)

    def test_portland_scene_1_safe(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=portland-safe')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene1-safe.html', ANY)

    def test_portland_scene_1_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=forgood')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene1.html', ANY)

    def test_portland_scene_1_fast_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=fast')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene1-fast.html', ANY)

    def test_portland_scene_1_safe_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=safe')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene1-safe.html', ANY)

    def test_portland_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=portland')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene2.html')

    def test_portland_scene_2_fast(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=portland-fast')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene2-fast.html')

    def test_portland_scene_2_safe(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=portland-safe')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene2-safe.html')

    def test_portland_scene_2_1(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=forgood')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene2.html')

    def test_portland_scene_2_fast_1(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=fast')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene2-fast.html')

    def test_portland_scene_2_safe_1(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=safe')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/portland/scene2-safe.html')

    def test_portland_nonenus_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=portland')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html', ANY)

    def test_portland_nonenus_scene_1_fast(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=portland-fast')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html', ANY)

    def test_portland_nonenus_scene_1_safe(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=portland-safe')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html', ANY)

    def test_portland_nonenus_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=portland')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html')

    def test_portland_nonenus_scene_2_fast(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=portland-fast')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html')

    def test_portland_nonenus_scene_2_safe(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=portland-safe')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html')

    # berlin campaign bug 1447445

    def test_berlin_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=berlin')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/berlin/scene1.html', ANY)

    def test_berlin_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=berlin')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/berlin/scene2.html')

    def test_berlin_nonde_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=berlin')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html', ANY)

    def test_berlin_nonde_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=berlin')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html')

    def test_herz_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=herz')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/berlin/scene1-herz.html', ANY)

    def test_herz_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=herz')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/berlin/scene2-herz.html')

    def test_herz_nonde_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=herz')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html', ANY)

    def test_herz_nonde_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=herz')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html')

    # berlin video test issue 5637

    def test_berlin_video_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=aus-gruenden')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/berlin/scene1-aus-gruenden.html', ANY)

    def test_berlin_video_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=aus-gruenden')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/berlin/scene2-aus-gruenden.html')

    # alternate de/new test issue 5879

    def test_de_a_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?v=a')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html', ANY)

    def test_de_a_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?v=a')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html')

    def test_de_b_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?v=b')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/de/scene1-b.html', ANY)

    def test_de_b_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?v=b')
        req.locale = 'de'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/de/scene2-b.html')

    # better browser test issue 5841

    def test_better_browser_scene_1_va(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=betterbrowser&v=a')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html', ANY)

    def test_better_browser_scene_1_vb(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=betterbrowser&v=b')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/better-browser/scene1-b.html', ANY)

    def test_better_browser_scene_1_vc(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=betterbrowser&v=c')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/better-browser/scene1-c.html', ANY)

    def test_better_browser_scene_1_vd(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=betterbrowser&v=d')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/better-browser/scene1-d.html', ANY)

    def test_better_browser_scene_1_ve(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=betterbrowser&v=e')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/better-browser/scene1-e.html', ANY)

    def test_better_browser_scene_1_vf(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=betterbrowser&v=f')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/better-browser/scene1-f.html', ANY)

    def test_better_browser_scene_1_non_us(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=betterbrowser&v=c')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html', ANY)

    def test_better_browser_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=betterbrowser')
        req.locale = 'en-US'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/better-browser/scene2.html')

    def test_better_browser_scene_2_non_us(self, render_mock):
        req = RequestFactory().get('/firefox/download/thanks/?xv=betterbrowser')
        req.locale = 'fr'
        views.download_thanks(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html')


class TestFirefoxNewNoIndex(TestCase):
    def test_scene_1_noindex(self):
        # Scene 1 of /firefox/new/ should never contain a noindex tag.
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'en-US'
        response = views.new(req)
        doc = pq(response.content)
        robots = doc('meta[name="robots"]')
        eq_(robots.length, 0)

    def test_scene_2_canonical(self):
        # Scene 2 of /firefox/new/ should contain a canonical tag to /firefox/new/.
        req = RequestFactory().get('/firefox/download/thanks/')
        req.locale = 'en-US'
        response = views.download_thanks(req)
        doc = pq(response.content)
        canonical = doc('link[rel="canonical"]')
        eq_(canonical.length, 1)
        ok_('/firefox/new/' in canonical.attr('href'))


class TestFeedbackView(TestCase):
    def test_get_template_names_default_unhappy(self):
        view = views.FeedbackView()
        view.request = RequestFactory().get('/')
        eq_(view.get_template_names(), ['firefox/feedback/unhappy.html'])

    def test_get_template_names_happy(self):
        view = views.FeedbackView()
        view.request = RequestFactory().get('/?score=5')
        eq_(view.get_template_names(), ['firefox/feedback/happy.html'])

    def test_get_template_names_unhappy(self):
        view = views.FeedbackView()
        view.request = RequestFactory().get('/?score=1')
        eq_(view.get_template_names(), ['firefox/feedback/unhappy.html'])

    def test_get_context_data_three_stars(self):
        view = views.FeedbackView()
        view.request = RequestFactory().get('/?score=3')

        ctx = view.get_context_data()
        self.assertTrue(ctx['donate_stars_url'].endswith('Heartbeat_3stars'))

    def test_get_context_data_five_stars(self):
        view = views.FeedbackView()
        view.request = RequestFactory().get('/?score=5')

        ctx = view.get_context_data()
        self.assertTrue(ctx['donate_stars_url'].endswith('Heartbeat_5stars'))

    def test_get_context_data_one_star(self):
        """donate_stars_url should be undefined"""
        view = views.FeedbackView()
        view.request = RequestFactory().get('/?score=1')

        ctx = view.get_context_data()
        self.assertFalse('donate_stars_url' in ctx)
