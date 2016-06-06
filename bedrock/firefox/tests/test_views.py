# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from django.test.client import RequestFactory

from bedrock.base.urlresolvers import reverse
from mock import patch
from nose.tools import eq_, ok_

from bedrock.firefox import views
from bedrock.mozorg.tests import TestCase


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
        self.mock_send_sms.assert_called_with('15558675309', views.SMS_MESSAGES['android'])

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
                                               views.EMAIL_MESSAGES['android'],
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

    # /firefox/android/ embedded widget (bug 1221328)
    def test_variant_android_embedded_email(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': 'dude@example.com',
            'send-to-device-basket-id': 'android-embed',
        })
        ok_(resp_data['success'])
        self.mock_subscribe.assert_called_with('dude@example.com',
                                                views.EMAIL_MESSAGES['android-embed'],
                                                source_url=None,
                                                lang='en-US')

    def test_variant_android_embedded_sms(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': '5558675309',
            'send-to-device-basket-id': 'android-embed',
        })
        ok_(resp_data['success'])
        self.mock_send_sms.assert_called_with('15558675309',
                                                views.SMS_MESSAGES['android-embed'])

    # an invalid value for 'android-send-to-device-test' should cause email message
    # to revert back to specified platform
    def test_variant_android_invalid_test_value(self):
        resp_data = self._request({
            'platform': 'android',
            'phone-or-email': 'dude@example.com',
            'send-to-device-basket-id': 'a-real-reactionary',  # bad value!
        })
        ok_(resp_data['success'])
        self.mock_subscribe.assert_called_with('dude@example.com',
                                               views.EMAIL_MESSAGES['android'],
                                               source_url=None,
                                               lang='en-US')


@patch('bedrock.firefox.views.l10n_utils.render')
class TestFirefoxNew(TestCase):
    def test_frames_allow(self, render_mock):
        """
        Bedrock pages get the 'x-frame-options: DENY' header by default.
        The firefox/new page needs to be framable for things like stumbleupon.
        Bug 1004598.
        """
        with self.activate('en-US'):
            resp = self.client.get(reverse('firefox.new'))

        ok_('x-frame-options' not in resp)

    def test_scene_1_horizon_template_en_us(self, render_mock):
        req = RequestFactory().get('/firefox/new/?v=1')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/horizon/scene1.html')

    def test_scene_2_horizon_template_en_us(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2&v=1')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/horizon/scene2.html')

    def test_scene_1_template_en_us(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/redesign/scene1.html')

    def test_scene_2_template_en_us(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2')
        req.locale = 'en-US'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/redesign/scene2.html')

    def test_scene_1_template_other_locales(self, render_mock):
        req = RequestFactory().get('/firefox/new/')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene1.html')

    def test_scene_2_template_other_locales(self, render_mock):
        req = RequestFactory().get('/firefox/new/?scene=2')
        req.locale = 'de'
        views.new(req)
        render_mock.assert_called_once_with(req, 'firefox/new/scene2.html')


class TestWin10WelcomeView(TestCase):
    def test_get_template_names_default(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10-welcome.html'])

    def test_get_template_names_v1(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=1')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10_variants/variant-3-1.html'])

    def test_get_template_names_v2(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=2')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10_variants/variant-3-2.html'])

    def test_get_template_names_v3(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=3')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10_variants/variant-3-3.html'])

    def test_get_template_names_v4(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=4')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10_variants/variant-3-4.html'])

    def test_get_template_names_v5(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=5')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10_variants/variant-3-5.html'])

    def test_get_template_names_v6(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=6')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10_variants/variant-3-6.html'])

    def test_get_template_names_v7(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=7')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10_variants/variant-3-7.html'])

    def test_get_template_names_v8(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=8')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10_variants/variant-3-8.html'])

    def test_get_template_names_v9(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=9')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10_variants/variant-3-9.html'])

    def test_get_template_names_v10(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=10')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10_variants/variant-3-10.html'])

    def test_get_template_names_non_en(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=1')
        view.request.locale = 'de'
        eq_(view.get_template_names(), ['firefox/win10-welcome.html'])

    def test_get_template_names_invalid_number(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=11')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10-welcome.html'])

    def test_get_template_names_invalid_string(self):
        view = views.Win10Welcome()
        view.request = RequestFactory().get('/?v=dude')
        view.request.locale = 'en-US'
        eq_(view.get_template_names(), ['firefox/win10-welcome.html'])


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
