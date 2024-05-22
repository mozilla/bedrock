# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings


class CheckEmailDeliverabilityTestCase(TestCase):
    @override_settings(EMAIL_HOST_USER="", EMAIL_HOST_PASSWORD="")
    @patch("sys.stdout")
    def test_no_email_config_at_all(self, mock_stdout):
        with self.assertRaises(SystemExit) as cm:
            call_command("check_email_deliverability")
        self.assertEqual(cm.exception.code, 0)

        mock_stdout.write.assert_called_once_with("Email not configured for sending. Exiting\n")

    @override_settings(EMAIL_HOST_USER="user", EMAIL_HOST_PASSWORD="pass")
    @patch("sys.stdout")
    def test_no_email_address_at_all(self, mock_stdout):
        with self.assertRaises(SystemExit) as cm:
            call_command("check_email_deliverability")
        self.assertEqual(cm.exception.code, 1)

        mock_stdout.write.assert_called_once_with("Unable to send test email: no destination address available\n")

    @override_settings(EMAIL_HOST_USER="user", EMAIL_HOST_PASSWORD="pass")
    @patch.dict(
        "os.environ",
        {"EMAIL_DELIVERABILITY_TEST_ADDRESS": "envtest@example.com"},
    )
    @patch("sys.stdout")
    def test_send_test_email_with_env_var_email(self, mock_stdout):
        email_address = "envtest@example.com"
        call_command("check_email_deliverability", email=email_address)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test email to confirm email deliverability")
        self.assertEqual(mail.outbox[0].to, [email_address])
        mock_stdout.write.assert_called_once_with(f"Test email sent successfully to {email_address}\n")

    @override_settings(EMAIL_HOST_USER="user", EMAIL_HOST_PASSWORD="pass")
    @patch("sys.stdout")
    def test_send_test_email_with_cli_email_argument(self, mock_stdout):
        email_address = "test@example.com"
        call_command("check_email_deliverability", email=email_address)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test email to confirm email deliverability")
        self.assertEqual(mail.outbox[0].to, [email_address])
        mock_stdout.write.assert_called_once_with(f"Test email sent successfully to {email_address}\n")
