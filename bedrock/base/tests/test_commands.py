# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from io import StringIO
from unittest.mock import MagicMock, call, patch

from django.core import mail
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

import pytest
from waffle.models import Switch

from bedrock.base.management.commands import reset_demo_db_schema
from bedrock.base.models import ConfigValue


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


@pytest.mark.django_db
class TestImportWaffleSwitches:
    def test_switch_values_become_waffle_switches(self, capsys):
        ConfigValue.objects.create(name="SWITCH_DARK_MODE", value="on")
        ConfigValue.objects.create(name="SWITCH_NEW_NAV", value="off")

        call_command("import_waffle_switches")

        assert Switch.objects.get(name="DARK_MODE").active is True
        assert Switch.objects.get(name="NEW_NAV").active is False
        out = capsys.readouterr().out
        assert "Created new switch: DARK_MODE = on" in out
        assert "Created new switch: NEW_NAV = off" in out

    def test_only_on_turns_a_switch_on(self):
        ConfigValue.objects.create(name="SWITCH_YES", value="yes")
        ConfigValue.objects.create(name="SWITCH_TRUE", value="true")

        call_command("import_waffle_switches")

        assert not Switch.objects.filter(active=True).exists()

    def test_other_config_values_are_ignored(self):
        ConfigValue.objects.create(name="FUNNELCAKE_99_LOCALES", value="on")
        ConfigValue.objects.create(name="switch_lowercase", value="on")

        call_command("import_waffle_switches")

        assert not Switch.objects.exists()

    def test_existing_switch_is_updated(self, capsys):
        Switch.objects.create(name="DARK_MODE", active=True)
        ConfigValue.objects.create(name="SWITCH_DARK_MODE", value="off")

        call_command("import_waffle_switches")

        assert Switch.objects.get(name="DARK_MODE").active is False
        assert Switch.objects.count() == 1
        assert "Updated switch: DARK_MODE = off" in capsys.readouterr().out

    @patch("bedrock.utils.management.decorators.capture_exception")
    def test_error_goes_to_sentry(self, capture_exception):
        error = RuntimeError("DB went away")
        with patch.object(ConfigValue.objects, "all", side_effect=error):
            with pytest.raises(RuntimeError):
                call_command("import_waffle_switches")
        capture_exception.assert_called_once_with(error)


class TestResetDemoDbSchema:
    @pytest.fixture
    def connection(self):
        with patch.object(reset_demo_db_schema, "connection", MagicMock(vendor="postgresql")) as connection_mock:
            yield connection_mock

    def executed_sql(self, connection):
        return connection.cursor.return_value.__enter__.return_value.execute.call_args_list

    @pytest.mark.parametrize("is_demo", ["false", "0", ""])
    def test_refuses_to_run_off_demos(self, connection, is_demo):
        with patch.dict("os.environ", {"IS_DEMO": is_demo}):
            with pytest.raises(CommandError, match="This may only be run on demos"):
                call_command("reset_demo_db_schema")
        connection.cursor.assert_not_called()

    def test_refuses_to_run_off_postgres(self, connection):
        connection.vendor = "sqlite"
        with patch.dict("os.environ", {"IS_DEMO": "true"}):
            with pytest.raises(CommandError, match="reset_schema only supports PostgreSQL"):
                call_command("reset_demo_db_schema")
        connection.cursor.assert_not_called()

    def test_drops_and_recreates_public_schema(self, connection):
        out = StringIO()
        with patch.dict("os.environ", {"IS_DEMO": "true"}):
            call_command("reset_demo_db_schema", stdout=out)

        assert self.executed_sql(connection) == [
            call("DROP SCHEMA IF EXISTS public CASCADE;"),
            call("CREATE SCHEMA public AUTHORIZATION CURRENT_USER;"),
        ]
        assert out.getvalue() == "Reset public schema\n"
