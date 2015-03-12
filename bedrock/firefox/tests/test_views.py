# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import json
from django.test.client import RequestFactory
from funfactory.urlresolvers import reverse
from mock import patch
from nose.tools import ok_

from bedrock.firefox import views
from bedrock.mozorg.tests import TestCase


class TestFirefoxNew(TestCase):
    def test_frames_allow(self):
        """
        Bedrock pages get the 'x-frame-options: DENY' header by default.
        The firefox/new page needs to be framable for things like stumbleupon.
        Bug 1004598.
        """
        with self.activate('en-US'):
            resp = self.client.get(reverse('firefox.new'))

        ok_('x-frame-options' not in resp)


@patch('bedrock.firefox.views.basket.send_sms')
class TestSMSView(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_normal_post_success(self, sms_mock):
        """Should send sms and return a redirect."""
        req = self.rf.post('/', {'number': '5558675309'})
        resp = views.sms_send(req)
        sms_mock.assert_called_with('15558675309', 'SMS_Android', False)
        self.assertEqual(resp.status_code, 302)

    def test_ajax_post_success(self, sms_mock):
        """Should send sms and return a JSON response."""
        req = self.rf.post('/', {'number': '5558675309'},
                           HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        resp = views.sms_send(req)
        sms_mock.assert_called_with('15558675309', 'SMS_Android', False)
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content)
        self.assertEqual(resp_data, {'success': True})

    def test_normal_post_error(self, sms_mock):
        """Should not send sms and should return the form with error message."""
        req = self.rf.post('/', {'number': '8675309'})
        resp = views.sms_send(req)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, u'Sorry. This number isn\'t valid.')
        self.assertFalse(sms_mock.called)

    def test_ajax_post_error(self, sms_mock):
        """Should not send sms and should return a JSON response."""
        req = self.rf.post('/', {'number': '8675309'},
                           HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        resp = views.sms_send(req)
        self.assertFalse(sms_mock.called)
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content)
        self.assertFalse(resp_data['success'])
        self.assertIn(u'Sorry. This number isn\'t valid.', resp_data['error'])

    def test_normal_basket_error(self, sms_mock):
        """Should not send sms and should return the form with error message."""
        sms_mock.side_effect = views.basket.BasketException
        req = self.rf.post('/', {'number': '5558675309'})
        resp = views.sms_send(req)
        sms_mock.assert_called_with('15558675309', 'SMS_Android', False)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, u'An error occurred in our system. Please try again later.')

    def test_ajax_basket_error(self, sms_mock):
        """Should not send sms and should return a JSON response."""
        sms_mock.side_effect = views.basket.BasketException
        req = self.rf.post('/', {'number': '5558675309'},
                           HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        resp = views.sms_send(req)
        sms_mock.assert_called_with('15558675309', 'SMS_Android', False)
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content)
        self.assertEqual(resp_data, {
            'success': False,
            'error': u'An error occurred in our system. Please try again later.',
        })
