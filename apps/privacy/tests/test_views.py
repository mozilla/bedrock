# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core import mail
from django.test.client import Client

from mozorg.tests import TestCase
from funfactory.urlresolvers import reverse

from nose.tools import eq_


class PrivacyFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact = 'foo@bar.com'
        with self.activate('en-US'):
            self.url = reverse('privacy.index')
        self.data = {
            'name': 'Tester',
            'sender': self.contact,
            'comments': 'It works!',
        }

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
        eq_(outbox.to, ['privacy@mozilla.com'])
