# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from io import StringIO
from unittest.mock import call, patch

from django.core.management import call_command
from django.test import TransactionTestCase


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
