# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime

from django.core import mail
from django.test.client import RequestFactory

from bedrock.base.urlresolvers import reverse
from mock import Mock, patch
from nose.tools import eq_, ok_

from bedrock.press import forms as press_forms, views as press_views
from bedrock.press.forms import (PressInquiryForm, SpeakerRequestForm)
from bedrock.mozorg.tests import TestCase


class TestPressInquiry(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = press_views.PressInquiryView.as_view()
        with self.activate('en-US'):
            self.url = reverse('press.press-inquiry')

        self.data = {
            'jobtitle': 'Senior Inquiry Person',
            'name': 'IceCat FireBadger',
            'user_email': 'courage@nowhere.com',
            'media_org': 'Big Money',
            'inquiry': 'Want to know private stuff',
            'deadline': datetime.date.today() + datetime.timedelta(days=1)
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

        eq_(response.status_code, 302)
        eq_(response['Location'], '/en-US/press/press-inquiry/?success=True')

    def test_view_post_missing_data(self):
        """
        POST with missing data should return 200 and contain form
        errors in the template.
        """

        self.data.update(name='')  # remove required name

        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        response = self.view(request)

        eq_(response.status_code, 200)
        self.assertIn('Please enter your name.', response.content)

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

        eq_(response.status_code, 200)
        self.assertIn('An error has occurred', response.content)

    def test_form_valid_data(self):
        """
        Form should be valid.
        """
        form = PressInquiryForm(self.data)

        # make sure form is valid
        ok_(form.is_valid())

    def test_form_missing_data(self):
        """
        With incorrect data (missing email), form should not be valid and should
        have user_email in the errors hash.
        """
        self.data.update(user_email='')  # remove required user_email

        form = PressInquiryForm(self.data)

        # make sure form is invalid
        ok_(not form.is_valid())

        # make sure user_email errors are in form
        self.assertIn('user_email', form.errors)

    def test_form_honeypot(self):
        """
        Form with honeypot text box filled should not be valid.
        """
        self.data['office_fax'] = 'spammer'

        form = PressInquiryForm(self.data)

        eq_(False, form.is_valid())

    @patch('bedrock.press.views.render_to_string',
           return_value='rendered')
    @patch('bedrock.press.views.EmailMessage')
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
            press_views.PRESS_INQUIRY_EMAIL_SUBJECT,
            'rendered',
            press_views.PRESS_INQUIRY_EMAIL_FROM,
            press_views.PRESS_INQUIRY_EMAIL_TO)


class TestSpeakerRequest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = press_views.SpeakerRequestView.as_view()
        with self.activate('en-US'):
            self.url = reverse('press.speaker-request')

        self.data = {
            'sr_event_name': 'Test Event',
            'sr_event_url': 'www.mozilla.org',
            'sr_event_date': datetime.date.today() + datetime.timedelta(days=1),
            'sr_event_time': '12:00 PM',
            'sr_contact_name': 'The Dude',
            'sr_contact_email': 'foo@bar.com',
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

        eq_(response.status_code, 302)
        eq_(response['Location'], '/en-US/press/speakerrequest/?success=True')

    def test_view_post_missing_data(self):
        """
        POST with missing data should return 200 and contain form
        errors in the template.
        """

        self.data.update(sr_event_url='')  # remove required url

        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        response = self.view(request)

        eq_(response.status_code, 200)
        self.assertIn('Please enter a URL', response.content)

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

        eq_(response.status_code, 200)
        self.assertIn('An error has occurred', response.content)

    def test_form_valid_data(self):
        """
        Form should be valid.
        """
        form = SpeakerRequestForm(self.data)

        # make sure form is valid
        ok_(form.is_valid())

    def test_form_missing_data(self):
        """
        With incorrect data (missing url), form should not be valid and should
        have url in the errors hash.
        """
        self.data.update(sr_event_url='')  # remove required url

        form = SpeakerRequestForm(self.data)

        # make sure form is invalid
        ok_(not form.is_valid())

        # make sure url errors are in form
        self.assertIn('sr_event_url', form.errors)

    def test_form_honeypot(self):
        """
        Form with honeypot text box filled should not be valid.
        """
        self.data['office_fax'] = 'spammer'

        form = SpeakerRequestForm(self.data)

        eq_(False, form.is_valid())

    def test_form_valid_attachement(self):
        """
        Form should be valid when attachment under/at size limit.
        """
        # attachment within size limit
        mock_attachment = Mock(
            _size=press_forms.SPEAKER_REQUEST_FILE_SIZE_LIMIT)

        form = SpeakerRequestForm(
            self.data, {
                'sr_attachment': mock_attachment})

        # make sure form is valid
        ok_(form.is_valid())

    def test_form_invalid_attachement(self):
        """
        Form should be invalid and contain attachment errors when attachment
        over size limit.
        """
        # attachment within size limit
        mock_attachment = Mock(
            _size=(press_forms.SPEAKER_REQUEST_FILE_SIZE_LIMIT + 1))

        form = SpeakerRequestForm(
            self.data, {
                'sr_attachment': mock_attachment})

        # make sure form is not valid
        ok_(not form.is_valid())

        # make sure attachment errors are in form
        self.assertIn('sr_attachment', form.errors)

    @patch('bedrock.press.views.render_to_string',
           return_value='rendered')
    @patch('bedrock.press.views.EmailMessage')
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
            press_views.SPEAKER_REQUEST_EMAIL_SUBJECT,
            'rendered',
            press_views.SPEAKER_REQUEST_EMAIL_FROM,
            press_views.SPEAKER_REQUEST_EMAIL_TO)

    @patch('bedrock.press.views.render_to_string',
           return_value='rendered')
    @patch('bedrock.press.views.EmailMessage')
    def test_email_with_attachement(
            self, mock_email_message, mock_render_to_string):
        """
        Make sure email is sent with attachment.
        """
        mock_attachment = Mock(
            content_type='text/plain',
            _size=(press_forms.SPEAKER_REQUEST_FILE_SIZE_LIMIT))

        # make sure name attribute is treated as string
        mock_attachment.name = 'img.jpg'

        # create POST request
        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        # add mock attachment to files dict
        request.FILES['sr_attachment'] = mock_attachment

        # submit POST request
        self.view(request)

        # make sure attachment was attached
        mock_email_message.return_value.attach.assert_called_once_with(
            'img.jpg',
            mock_attachment.read.return_value,
            'text/plain')

        mock_attachment.read.assert_called_once_with()

        # make sure email was sent
        mock_email_message.return_value.send.assert_called_once_with()

        # make sure email values are correct
        mock_email_message.assert_called_once_with(
            press_views.SPEAKER_REQUEST_EMAIL_SUBJECT,
            'rendered',
            press_views.SPEAKER_REQUEST_EMAIL_FROM,
            press_views.SPEAKER_REQUEST_EMAIL_TO)

    def test_emails_not_escaped(self):
        """
        Strings in the fraud report form should not be HTML escaped
        when inserted into the email, which is just text.

        E.g. if they entered

            J'adore le ''Renard de feu''

        the email should not contain

            J&#39;adore le &#39;&#39;Renard de feu&#39;&#39;

        Tags are still stripped, though.
        """

        STRING1 = u"<blink>J'adore Citröns</blink> & <Piñatas> so there"
        EXPECTED1 = u"J'adore Citröns &  so there"

        STRING2 = u"J'adore Piñatas & <fromage> so here"
        EXPECTED2 = u"J'adore Piñatas &  so here"

        STRING3 = u"J'adore <coffee>el café</coffee> también"
        EXPECTED3 = u"J'adore el café también"

        self.data.update(sr_contact_title=STRING1, sr_event_theme=STRING2,
                         sr_event_format=STRING3)
        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        self.view(request)

        eq_(len(mail.outbox), 1)

        m = mail.outbox[0]

        self.assertIn(EXPECTED1, m.body)
        self.assertIn(EXPECTED2, m.body)
        self.assertIn(EXPECTED3, m.body)
