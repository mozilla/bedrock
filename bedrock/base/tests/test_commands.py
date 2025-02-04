# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pathlib import Path
from unittest.mock import DEFAULT, patch

from django.core import mail
from django.core.management import call_command
from django.test import TestCase as DjangoTestCase, override_settings

from bedrock.base.management.commands import update_product_details_files
from bedrock.mozorg.tests import TestCase


class CheckEmailDeliverabilityTestCase(DjangoTestCase):
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


PD_REPO_TEST_PATH = Path(__file__).parent.joinpath("test_pd_repo")


@override_settings(PROD_DETAILS_STORAGE="PDDatabaseStorage", PROD_DETAILS_TEST_DIR=str(PD_REPO_TEST_PATH.joinpath("product-details")))
class TestUpdateProductDetailsFiles(TestCase):
    def setUp(self):
        self.command = update_product_details_files.Command()
        self.command.repo.path = PD_REPO_TEST_PATH
        self.command.repo.path_str = str(PD_REPO_TEST_PATH)

    def test_handle_diff_loads_all(self):
        with patch.multiple(self.command, update_file_data=DEFAULT, validate_data=DEFAULT, file_storage=DEFAULT, load_changes=DEFAULT, repo=DEFAULT):
            options = dict(quiet=False, database="default", force=False)
            self.command.update_file_data.return_value = True
            self.command.handle(**options)
            assert self.command.file_storage.all_json_files.called
            self.command.load_changes.assert_called_with(options, self.command.file_storage.all_json_files())
            assert self.command.repo.set_db_latest.called

    def test_handle_error_no_set_latest(self):
        with patch.multiple(self.command, update_file_data=DEFAULT, validate_data=DEFAULT, file_storage=DEFAULT, load_changes=DEFAULT, repo=DEFAULT):
            options = dict(quiet=False, database="default", force=False)
            self.command.update_file_data.return_value = True
            self.command.load_changes.side_effect = Exception("broke yo")
            with self.assertRaises(Exception):
                self.command.handle(**options)
            assert self.command.file_storage.all_json_files.called
            self.command.load_changes.assert_called_with(options, self.command.file_storage.all_json_files())
            assert not self.command.repo.set_db_latest.called

    def test_handle_no_diff_does_nothing(self):
        with patch.multiple(self.command, update_file_data=DEFAULT, validate_data=DEFAULT, file_storage=DEFAULT, load_changes=DEFAULT, repo=DEFAULT):
            options = dict(quiet=False, database="default", force=False)
            self.command.update_file_data.return_value = False
            self.command.handle(**options)
            assert not self.command.file_storage.all_json_files.called
            assert not self.command.repo.set_db_latest.called
