# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
from urlparse import parse_qs

from django.test import override_settings
from django.test.client import RequestFactory

import querystringsafe_base64
from mock import patch, Mock
from nose.tools import eq_, ok_

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
        req = self._get_request({'dude': 'abides'})
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 400)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        self.assertEqual(data['error'], 'no params')

    def test_no_valid_param_data(self):
        params = {'utm_source': 'br@ndt', 'utm_medium': 'ae<t>her'}
        req = self._get_request(params)
        resp = views.stub_attribution_code(req)
        self.assertEqual(resp.status_code, 400)
        assert resp['cache-control'] == 'max-age=300'
        data = json.loads(resp.content)
        self.assertEqual(data['error'], 'no params')

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

        patcher = patch('bedrock.firefox.views.basket.send_sms')
        self.mock_send_sms = patcher.start()
        self.addCleanup(patcher.stop)

    def _request(self, data, expected_status=200):
        rf = RequestFactory()
        resp = views.send_to_device_ajax(rf.post('/', data))
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
        self.mock_send_sms.assert_called_with('15558675309', views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms']['android'])

    def test_send_android_sms_basket_error(self):
        self.mock_send_sms.side_effect = views.basket.BasketException
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '5558675309',
        }, 400)
        ok_(not resp_data['success'])
        ok_('system' in resp_data['errors'])

    def test_send_bad_sms_number(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '555',
        })
        ok_(not resp_data['success'])
        ok_('number' in resp_data['errors'])
        ok_(not self.mock_send_sms.called)

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
        self.mock_send_sms.assert_called_with('15558675309',
                                               views.SEND_TO_DEVICE_MESSAGE_SETS['default']['sms']['ios'])

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
        self.mock_send_sms.assert_called_with('15558675309',
                                               views.SEND_TO_DEVICE_MESSAGE_SETS['fx-android']['sms']['android'])

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
        self.mock_send_sms.assert_called_with('15558675309',
                                               views.SEND_TO_DEVICE_MESSAGE_SETS['fx-mobile-download-desktop']['sms']['all'])


@override_settings(DEV=False)
@patch('bedrock.firefox.views.l10n_utils.render')
class TestFirefoxNew(TestCase):
    def test_scene_1_template(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/onboarding/scene1.html')

    def test_scene_2_template(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/onboarding/scene2.html')

    @patch.object(views, 'lang_file_is_active', lambda *x: False)
    def test_scene_1_old_template(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html')

    @patch.object(views, 'lang_file_is_active', lambda *x: False)
    def test_scene_2_old_template(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html')

    # ad-campaign experience tests (bug 1329661)
    def test_break_free_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=breakfree')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/break-free/scene1.html')

    def test_break_free_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=breakfree')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/break-free/scene2.html')

    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_break_free_locale_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=breakfree')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/onboarding/scene1.html')

    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_break_free_locale_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=breakfree')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/onboarding/scene2.html')

    def test_way_of_the_fox_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=wayofthefox')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/way-of-the-fox/scene1.html')

    def test_way_of_the_fox_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=wayofthefox')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/way-of-the-fox/scene2.html')

    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_way_of_the_fox_locale_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=wayofthefox')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/onboarding/scene1.html')

    @patch.object(views, 'lang_file_is_active', lambda *x: True)
    def test_way_of_the_fox_locale_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=wayofthefox')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/onboarding/scene2.html')

    # moar ad campaign pages bug 1363543

    def test_private_not_option_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=privatenotoption')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/private-not-option/scene1.html')

    def test_private_not_option_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=privatenotoption')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/private-not-option/scene2.html')

    def test_conformity_not_default_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=conformitynotdefault')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/conformity-not-default/scene1.html')

    def test_conformity_not_default_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=conformitynotdefault')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/conformity-not-default/scene2.html')

    def test_browse_up_to_you_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=browseuptoyou')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/browse-up-to-you/scene1.html')

    def test_browse_up_to_you_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=browseuptoyou')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/browse-up-to-you/scene2.html')

    def test_more_protection_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=moreprotection')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/more-protection/scene1.html')

    def test_more_protection_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=moreprotection')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/more-protection/scene2.html')

    def test_working_out_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=workingout')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/working-out/scene1.html')

    def test_working_out_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=workingout')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/working-out/scene2.html')

    def test_you_do_you_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=youdoyou')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/you-do-you/scene1.html')

    def test_you_do_you_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=youdoyou')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/you-do-you/scene2.html')

    def test_its_your_web_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=itsyourweb')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/its-your-web/scene1.html')

    def test_its_your_web_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=itsyourweb')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/fx-lifestyle/its-your-web/scene2.html')

    # browse against the machine bug 1363802, 1364988.

    def test_batmfree_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=batmfree')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/free.html')

    def test_batmfree_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=batmfree')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/scene2.html')

    def test_batmprivate_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=batmprivate')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/private.html')

    def test_batmprivate_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=batmprivate')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/scene2.html')

    def test_batmnimble_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=batmnimble')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/nimble.html')

    def test_batmnimble_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=batmnimble')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/scene2.html')

    def test_batmresist_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=batmresist')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/resist.html')

    def test_batmresist_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=batmresist')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/scene2.html')

    # browse against the machine animation bug 1366397

    def test_batma_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=batmprivate&v=a')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/machine-a.html')

    def test_batma_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=batmprivate&v=a')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/scene2.html')

    def test_batmb_scene_1(self, render_mock):
        req = RequestFactory().get('/firefox/new/?xv=batmprivate&v=b')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/machine-b.html')

    def test_batmb_scene_2(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&xv=batmprivate&v=b')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/batm/scene2.html')


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


@override_settings(DEV=False)
@patch('bedrock.firefox.views.l10n_utils.render')
class TestFirefoxFeatures(TestCase):
    def test_new_template(self, render_mock):
        req = RequestFactory().get('/firefox/features/')
        req.locale = 'en-US'
        views.features_landing(req)
        render_mock.assert_called_once_with(req, 'firefox/features/index.html')

    @patch.object(views, 'lang_file_is_active', lambda *x: False)
    def test_old_template(self, render_mock):
        req = RequestFactory().get('/firefox/features/')
        req.locale = 'de'
        views.features_landing(req)
        render_mock.assert_called_once_with(req, 'firefox/features.html')


@override_settings(DEV=False)
@patch('bedrock.mozorg.views.l10n_utils.render')
class TestFirefoxProductDesktopView(TestCase):
    def test_new_template(self, render_mock):
        view = views.FirefoxProductDesktopView()
        view.request = RequestFactory().get('/firefox/desktop/')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/products/desktop.html'])

    @patch.object(views, 'lang_file_is_active', lambda *x: False)
    def test_old_template(self, render_mock):
        view = views.FirefoxProductDesktopView()
        view.request = RequestFactory().get('/firefox/desktop/')
        view.request.locale = 'fr'
        eq_(view.get_template_names(), ['firefox/desktop/index.html'])


@override_settings(DEV=False)
@patch('bedrock.mozorg.views.l10n_utils.render')
class TestFirefoxProductAndroidView(TestCase):
    def test_new_template(self, render_mock):
        view = views.FirefoxProductAndroidView()
        view.request = RequestFactory().get('/firefox/android/')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/products/android.html'])

    @patch.object(views, 'lang_file_is_active', lambda *x: False)
    def test_old_template(self, render_mock):
        view = views.FirefoxProductAndroidView()
        view.request = RequestFactory().get('/firefox/android/')
        view.request.locale = 'fr'
        eq_(view.get_template_names(), ['firefox/android/index.html'])


@override_settings(DEV=False)
@patch('bedrock.mozorg.views.l10n_utils.render')
class TestFirefoxProductIOSView(TestCase):
    def test_new_template(self, render_mock):
        view = views.FirefoxProductIOSView()
        view.request = RequestFactory().get('/firefox/ios/')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/products/ios.html'])

    @patch.object(views, 'lang_file_is_active', lambda *x: False)
    def test_old_template(self, render_mock):
        view = views.FirefoxProductIOSView()
        view.request = RequestFactory().get('/firefox/ios/')
        view.request.locale = 'fr'
        eq_(view.get_template_names(), ['firefox/ios.html'])


@override_settings(DEV=False)
@patch('bedrock.firefox.views.l10n_utils.render')
class TestSync(TestCase):
    def test_en_us_template(self, render_mock):
        req = RequestFactory().get('/firefox/features/sync/')
        req.locale = 'en-US'
        views.FeaturesSyncView(req)
        render_mock.assert_called_once_with(req, 'firefox/features/sync-en.html')

    def test_en_gb_template(self, render_mock):
        req = RequestFactory().get('/firefox/features/sync/')
        req.locale = 'en-GB'
        views.FeaturesSyncView(req)
        render_mock.assert_called_once_with(req, 'firefox/features/sync-en.html')

    def test_locales_template(self, render_mock):
        req = RequestFactory().get('/firefox/features/sync/')
        req.locale = 'de'
        views.FeaturesSyncView(req)
        render_mock.assert_called_once_with(req, 'firefox/features/sync.html')
