# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from io import BytesIO

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import RequestFactory

from mock import Mock, patch
from PIL import Image

from bedrock.base.urlresolvers import reverse
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

    def _create_image_file(self):
        io = BytesIO()
        image = Image.new('RGB', (200, 200), 'white')
        image.save(io, 'PNG')
        io.seek(0)
        return SimpleUploadedFile('image.png', io.read(), 'image/png')

    def _create_text_file(self):
        return SimpleUploadedFile('stuff.txt', 'This is not an image', 'text/plain')

    def test_view_post_valid_data(self):
        """
        A valid POST should 302 redirect.
        """

        request = self.factory.post(self.url, self.data)

        # make sure CSRF doesn't hold us up
        request._dont_enforce_csrf_checks = True

        response = legal_views.fraud_report(request)

        assert response.status_code == 302
        assert response['Location'] == '/en-US/about/legal/fraud-report/?submitted=True'

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

        assert response.status_code == 200
        self.assertIn(b'Please enter a URL.', response.content)

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

        assert response.status_code == 200
        self.assertIn(b'An error has occurred', response.content)

    def test_form_valid_data(self):
        """
        Form should be valid.
        """
        form = FraudReportForm(self.data)

        # make sure form is valid
        assert form.is_valid()

    def test_form_invalid_data(self):
        """
        With incorrect data (missing url), form should not be valid and should
        have url in the errors hash.
        """
        self.data.update(input_url='')  # remove required url

        form = FraudReportForm(self.data)

        # make sure form is invalid
        assert not form.is_valid()

        # make sure url errors are in form
        self.assertIn('input_url', form.errors)

    def test_form_honeypot(self):
        """
        Form with honeypot text box filled should not be valid.
        """
        self.data['office_fax'] = 'spammer!'

        form = FraudReportForm(self.data)

        assert not form.is_valid()

    def test_form_valid_attachement(self):
        """
        Form should be valid when attachment under/at size limit.
        """
        # attachment within size limit
        mock_attachment = self._create_image_file()
        form = FraudReportForm(self.data, {'input_attachment': mock_attachment})
        # make sure form is valid
        assert form.is_valid()

    def test_form_invalid_attachement_type(self):
        """
        Form should be invalid and contain attachment errors when attachment
        is not an image.
        """
        # attachment within size limit
        mock_attachment = self._create_text_file()
        form = FraudReportForm(self.data, {'input_attachment': mock_attachment})
        # make sure form is not valid
        assert not form.is_valid()
        # make sure attachment errors are in form
        self.assertIn('input_attachment', form.errors)

    def test_form_invalid_attachement_size(self):
        """
        Form should be invalid and contain attachment errors when attachment
        over size limit.
        """
        # attachment within size limit
        mock_attachment = self._create_image_file()
        form = FraudReportForm(self.data, {'input_attachment': mock_attachment})
        with patch.object(legal_forms, 'FRAUD_REPORT_FILE_SIZE_LIMIT', 100):
            # make sure form is not valid
            assert not form.is_valid()

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
        mock_attachment = self._create_image_file()

        form = FraudReportForm(self.data, {'input_attachment': mock_attachment})

        # submit form
        request = self.factory.get('/')
        ret = submit_form(request, form)
        self.assertFalse(ret['form_error'])

        # make sure attachment was attached
        mock_attachment.seek(0)
        mock_email_message.return_value.attach.assert_called_once_with(
            mock_attachment.name,
            mock_attachment.read(),
            mock_attachment.content_type)

        # make sure email was sent
        mock_email_message.return_value.send.assert_called_once()

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

        assert len(mail.outbox) == 1

        m = mail.outbox[0]

        self.assertIn(EXPECTED1, m.body)
        self.assertIn(EXPECTED2, m.body)
        self.assertIn(EXPECTED3, m.body)
