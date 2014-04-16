# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core import mail

from bedrock.mozorg.tests import TestCase
from funfactory.urlresolvers import reverse

from nose.tools import eq_


class PrivacyFormTest(TestCase):
    def setUp(self):
        self.contact = 'foo@bar.com'
        with self.activate('en-US'):
            self.url = reverse('privacy')
        self.data = {
            'sender': self.contact,
            'comments': 'It works!',
        }
        self.bad_data = {
            'sender': '',
            'comments': 'Forgot your email!'
        }
        mail.outbox = []

    def tearDown(self):
        mail.outbox = []

    def test_send_privacy_contact(self):
        self.client.post(self.url, self.data)

        # Test that message has been sent.
        eq_(len(mail.outbox), 1)

        outbox = mail.outbox[0]
        # Verify that it has the correct subject
        eq_(outbox.subject, 'Message sent from Privacy Hub')

        # Verify sender
        eq_(outbox.from_email, self.contact)

        # Verify recipient
        eq_(outbox.to, ['yourprivacyis#1@mozilla.com'])

    def test_send_privacy_contact_invalid_data(self):
        response = self.client.post(reverse('privacy'), self.bad_data)

        eq_(response.status_code, 200)
        self.assertIn('This field is required, please enter your email address.', response.content)

        # Test that message was not sent.
        eq_(len(mail.outbox), 0)

    def test_honeypot_existence(self):
        res = self.client.get(self.url)

        self.assertIn('office_fax', res.content)

    def test_send_privacy_contact_with_honeypot(self):
        hp_data = self.data.copy()
        hp_data['office_fax'] = 'spammer'

        res = self.client.post(self.url, hp_data)

        self.assertIn("Your request could not be completed. Please try again.", res.content)
