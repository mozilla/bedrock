# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from io import StringIO
from unittest.mock import call, patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, TransactionTestCase

import everett


@patch("bedrock.cms.management.commands.bootstrap_local_admin.sys.stdout.write")
class BootstrapLocalAdminTests(TransactionTestCase):
    def _run_test(self, mock_write, expected_output):
        out = StringIO()
        call_command("bootstrap_local_admin", stdout=out)
        output = mock_write.call_args_list
        self.assertEqual(output, expected_output)

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "", "WAGTAIL_ADMIN_PASSWORD": ""})
    def test_no_env_vars_available(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Not bootstrapping an Admin user: WAGTAIL_ADMIN_EMAIL not defined in environment\n"),
            ],
        )

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "test@mozilla.com", "WAGTAIL_ADMIN_PASSWORD": ""})
    def test_email_available(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Created Admin user test@mozilla.com for local SSO use\n"),
            ],
        )

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "test@example.com", "WAGTAIL_ADMIN_PASSWORD": ""})
    def test_email_available_but_not_moco(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Not bootstrapping an Admin user: WAGTAIL_ADMIN_EMAIL is not a @mozilla.com email address\n"),
            ],
        )

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "test@mozilla.com", "WAGTAIL_ADMIN_PASSWORD": "secret"})
    def test_email_and_password_available(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Created Admin user test@mozilla.com with password 'secret'\n"),
            ],
        )

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "", "WAGTAIL_ADMIN_PASSWORD": ""})
    def test_only_password_available(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Not bootstrapping an Admin user: WAGTAIL_ADMIN_EMAIL not defined in environment\n"),
            ],
        )

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "test@mozilla.com", "WAGTAIL_ADMIN_PASSWORD": ""})
    def test_existing_user_exists_email_only(self, mock_write):
        out = StringIO()
        call_command("bootstrap_local_admin", stdout=out)
        call_command("bootstrap_local_admin", stdout=out)
        output = mock_write.call_args_list
        expected_output = [
            call("Created Admin user test@mozilla.com for local SSO use\n"),
            call("Admin user test@mozilla.com already exists\n"),
        ]
        self.assertEqual(output, expected_output)

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "test@mozilla.com", "WAGTAIL_ADMIN_PASSWORD": "secret"})
    def test_existing_user_exists_email_and_password(self, mock_write):
        out = StringIO()
        call_command("bootstrap_local_admin", stdout=out)
        call_command("bootstrap_local_admin", stdout=out)
        output = mock_write.call_args_list
        expected_output = [
            call("Created Admin user test@mozilla.com with password 'secret'\n"),
            call("Admin user test@mozilla.com already exists\n"),
        ]
        self.assertEqual(output, expected_output)


@patch("bedrock.cms.management.commands.bootstrap_demo_server_admins.sys.stdout.write")
class BootstrapDemoAdminsTests(TransactionTestCase):
    maxDiff = None

    def _run_test(self, mock_write, expected_output):
        out = StringIO()
        call_command("bootstrap_demo_server_admins", stdout=out)
        output = mock_write.call_args_list
        self.assertEqual(output, expected_output)

    @patch.dict("os.environ", {"DEMO_SERVER_ADMIN_USERS": ""})
    def test_no_env_vars_available(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Not bootstrapping users: DEMO_SERVER_ADMIN_USERS not set\n"),
            ],
        )

    @patch.dict("os.environ", {"DEMO_SERVER_ADMIN_USERS": ","})
    def test_only_empty_list_available(self, mock_write):
        with self.assertRaises(everett.InvalidValueError):
            self._run_test(
                mock_write=None,
                expected_output=None,
            )

    @patch.dict("os.environ", {"DEMO_SERVER_ADMIN_USERS": "test@mozilla.com, test2@mozilla.com,  test3@mozilla.com "})
    def test_multiple_emails_available(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Bootstrapping 3 SSO users\n"),
                call("Created Admin user test@mozilla.com for local SSO use\n"),
                call("Created Admin user test2@mozilla.com for local SSO use\n"),
                call("Created Admin user test3@mozilla.com for local SSO use\n"),
            ],
        )

    @patch.dict("os.environ", {"DEMO_SERVER_ADMIN_USERS": "testadmin@mozilla.com"})
    def test_single_email_available(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Bootstrapping 1 SSO users\n"),
                call("Created Admin user testadmin@mozilla.com for local SSO use\n"),
            ],
        )

    @patch.dict("os.environ", {"DEMO_SERVER_ADMIN_USERS": "testadmin@mozilla.com"})
    def test_user_created_has_appropriate_perms(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Bootstrapping 1 SSO users\n"),
                call("Created Admin user testadmin@mozilla.com for local SSO use\n"),
            ],
        )
        user = User.objects.get(email="testadmin@mozilla.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertFalse(user.has_usable_password())

    @patch.dict("os.environ", {"DEMO_SERVER_ADMIN_USERS": "test@mozilla.com, test2@mozilla.com, test3@mozilla.com"})
    def test_multiple_emails_available_but_exist_already_somehow(self, mock_write):
        # This is not likely to happen in reality, but worth testing
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Bootstrapping 3 SSO users\n"),
                call("Created Admin user test@mozilla.com for local SSO use\n"),
                call("Created Admin user test2@mozilla.com for local SSO use\n"),
                call("Created Admin user test3@mozilla.com for local SSO use\n"),
            ],
        )
        mock_write.reset_mock()
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Bootstrapping 3 SSO users\n"),
                call("User test@mozilla.com already exists - not creating\n"),
                call("User test2@mozilla.com already exists - not creating\n"),
                call("User test3@mozilla.com already exists - not creating\n"),
            ],
        )


class SmartlingSyncTests(TestCase):
    @patch("bedrock.cms.management.commands.run_smartling_sync.call_command")
    def test_sentry_logging_for_run_smartling_sync_command(self, mock_call_command):
        test_exception = Exception("Boom!")
        mock_call_command.side_effect = test_exception
        with patch("bedrock.cms.management.commands.run_smartling_sync.capture_exception") as mock_capture_exception:
            call_command("run_smartling_sync")
        mock_capture_exception.assert_called_once_with(test_exception)

    @patch("bedrock.cms.management.commands.bootstrap_local_admin.sys.stderr.write")
    @patch("bedrock.cms.management.commands.run_smartling_sync.call_command")
    def test_error_messaging_for_run_smartling_sync_command(self, mock_call_command, mock_stderr_write):
        test_exception = Exception("Boom!")
        mock_call_command.side_effect = test_exception
        call_command("run_smartling_sync")

        expected_output = "\nsync_smartling did not execute successfully: Boom!\n"
        output = mock_stderr_write.call_args_list[0][0][0]
        self.assertEqual(output, expected_output)
