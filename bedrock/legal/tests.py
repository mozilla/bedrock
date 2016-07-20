# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core import mail
from django.test.client import RequestFactory

from bedrock.base.urlresolvers import reverse
from mock import Mock, patch
from nose.tools import eq_, ok_

from bedrock.legal import forms as legal_forms, views as legal_views
from bedrock.legal.forms import FraudReportForm
from bedrock.legal.views import submit_form
from bedrock.mozorg.tests import TestCase


class TestFraudReport(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        with self.activate('en-US'):
            self.url = reverse('legal.fraud-report')

        self.data = {
            'input_url': 'http://www.test.com/',
            'input_category': 'Charging for software',
            'input_product': 'Firefox',
            'input_specific_product': '',
            'input_details': 'test details',
            'input_attachment_desc': 'test attachment',
            'input_email': 'foo@bar.com',
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

        response = legal_views.fraud_report(request)

        eq_(response.status_code, 302)
        eq_(response['Location'], '/en-US/about/legal/fraud-report/?submitted=True')

    def test_view_post_missing_data(self):
        """
        POST with missing data should return 200 and contain form
        errors in the template.
        """

        self.data.update(input_url='')  # remove required url

        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        response = legal_views.fraud_report(request)

        eq_(response.status_code, 200)
        self.assertIn('Please enter a URL.', response.content)

    def test_view_post_honeypot(self):
        """
        POST with honeypot text box filled should return 200 and
        contain general form error message.
        """

        self.data['office_fax'] = 'spammer'

        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        response = legal_views.fraud_report(request)

        eq_(response.status_code, 200)
        self.assertIn('An error has occurred', response.content)

    def test_form_valid_data(self):
        """
        Form should be valid.
        """
        form = FraudReportForm(self.data)

        # make sure form is valid
        ok_(form.is_valid())

    def test_form_invalid_data(self):
        """
        With incorrect data (missing url), form should not be valid and should
        have url in the errors hash.
        """
        self.data.update(input_url='')  # remove required url

        form = FraudReportForm(self.data)

        # make sure form is invalid
        eq_(False, form.is_valid())

        # make sure url errors are in form
        self.assertIn('input_url', form.errors)

    def test_form_honeypot(self):
        """
        Form with honeypot text box filled should not be valid.
        """
        self.data['office_fax'] = 'spammer!'

        form = FraudReportForm(self.data)

        eq_(False, form.is_valid())

    def test_form_valid_attachement(self):
        """
        Form should be valid when attachment under/at size limit.
        """
        # attachment within size limit
        mock_attachment = Mock(_size=legal_forms.FRAUD_REPORT_FILE_SIZE_LIMIT)

        form = FraudReportForm(self.data, {'input_attachment': mock_attachment})

        # make sure form is valid
        ok_(form.is_valid())

    def test_form_invalid_attachement(self):
        """
        Form should be invalid and contain attachment errors when attachment
        over size limit.
        """
        # attachment within size limit
        mock_attachment = Mock(
            _size=(legal_forms.FRAUD_REPORT_FILE_SIZE_LIMIT + 1))

        form = FraudReportForm(self.data, {'input_attachment': mock_attachment})

        # make sure form is not valid
        eq_(False, form.is_valid())

        # make sure attachment errors are in form
        self.assertIn('input_attachment', form.errors)

    @patch('bedrock.legal.views.render_to_string', return_value='rendered')
    @patch('bedrock.legal.views.EmailMessage')
    def test_email(self, mock_email_message, mock_render_to_string):
        """
        Make sure email is sent with expected values.
        """
        mock_send = Mock()
        mock_email_message.return_value = Mock(send=mock_send)

        form = FraudReportForm(self.data)

        # submit form
        request = self.factory.get('/')
        submit_form(request, form)

        # make sure email was sent
        mock_send.assert_called_once_with()

        # make sure email values are correct
        mock_email_message.assert_called_once_with(
            legal_views.FRAUD_REPORT_EMAIL_SUBJECT % (self.data['input_url'],
                                                      self.data['input_category']),
            'rendered',
            legal_views.FRAUD_REPORT_EMAIL_FROM,
            legal_views.FRAUD_REPORT_EMAIL_TO)

    @patch('bedrock.legal.views.render_to_string', return_value='rendered')
    @patch('bedrock.legal.views.EmailMessage')
    def test_email_with_attachement(self, mock_email_message, mock_render_to_string):
        """
        Make sure email is sent with attachment.
        """
        mock_attachment = Mock(
            content_type='text/plain',
            _size=(legal_forms.FRAUD_REPORT_FILE_SIZE_LIMIT))

        # make sure name attribute is treated as string
        mock_attachment.name = 'img.jpg'

        form = FraudReportForm(self.data, {'input_attachment': mock_attachment})

        # submit form
        request = self.factory.get('/')
        submit_form(request, form)

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
            legal_views.FRAUD_REPORT_EMAIL_SUBJECT % (self.data['input_url'],
                                                      self.data['input_category']),
            'rendered',
            legal_views.FRAUD_REPORT_EMAIL_FROM,
            legal_views.FRAUD_REPORT_EMAIL_TO)

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

        STRING1 = u"<em>J'adore Citröns</em> & <Piñatas> so there"
        EXPECTED1 = u"J'adore Citröns &  so there"

        STRING2 = u"<em>J'adore Piñatas</em> & <fromage> so here"
        EXPECTED2 = u"J'adore Piñatas &  so here"

        STRING3 = u"J'adore <coffee>el café</coffee> también"
        EXPECTED3 = u"J'adore el café también"

        self.data.update(input_specific_product=STRING1, input_details=STRING2,
                         input_attachment_desc=STRING3)
        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        legal_views.fraud_report(request)

        eq_(len(mail.outbox), 1)

        m = mail.outbox[0]

        self.assertIn(EXPECTED1, m.body)
        self.assertIn(EXPECTED2, m.body)
        self.assertIn(EXPECTED3, m.body)
