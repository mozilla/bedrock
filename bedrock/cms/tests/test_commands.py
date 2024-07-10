# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from io import StringIO
from unittest.mock import call, patch

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.management import call_command
from django.test import TransactionTestCase
from django.utils.timezone import now as tz_now

from wagtail.models import Locale, Revision
from wagtail_localize.models import TranslationSource

from bedrock.cms.models import SimpleRichTextPage
from bedrock.cms.tests.factories import LocaleFactory, SimpleRichTextPageFactory


class ScrubExportedCMSDataTestCase(TransactionTestCase):
    def setUp(
        self,
    ):
        en_us_locale, created = Locale.objects.get_or_create(language_code="en-US")
        fr_locale = LocaleFactory(language_code="fr")

        self.user = User.objects.create(username="testuser")
        self.session = Session.objects.create(
            session_key="testsession",
            expire_date=tz_now(),
        )
        self.root_page = SimpleRichTextPageFactory(slug="root_page_that_never_gets_seen")

        self.page_en = SimpleRichTextPageFactory(
            parent=self.root_page,
            slug="test-page",
            title="Test Page",
            locale=en_us_locale,
        )
        self.en_revision1 = self.page_en.save_revision()
        self.en_revision2 = self.page_en.save_revision()
        self.page_en.publish(revision=self.en_revision1)
        self.page_en.refresh_from_db()

        self.page_fr = self.page_en.copy_for_translation(fr_locale)
        self.fr_revision = self.page_fr.save_revision()
        self.page_fr.publish(revision=self.fr_revision)
        self.page_fr.refresh_from_db()
        self.translation_source, created = TranslationSource.get_or_create_from_instance(self.page_fr)

    @patch("bedrock.cms.management.commands.scrub_exported_cms_data.Command.output")
    def test_handle_command(self, mock_output):
        out = StringIO()
        call_command("scrub_exported_cms_data", stdout=out)
        output = str(mock_output.call_args_list)
        self.assertIn("Deleted Users:", output)
        self.assertIn("Deleted Sessions:", output)
        self.assertIn("Deleted non-live Revisions:", output)
        self.assertIn("Deleted TranslationSources:", output)

    def test_handle_command_with_non_sqlite_database(self):
        with self.assertRaises(Exception) as cm:
            with patch.object(settings, "DATABASES", {"default": {"ENGINE": "django.db.backends.postgresql"}}):
                call_command("scrub_exported_cms_data")
        self.assertEqual(str(cm.exception), "This command may only be run against a sqlite database")

    @patch("bedrock.cms.management.commands.scrub_exported_cms_data.sys.stdout.write")
    def test_handle_command_quiet_option(self, mock_write):
        out = StringIO()
        call_command("scrub_exported_cms_data", "-q", stdout=out)
        output = mock_write.call_args_list
        self.assertEqual(output, [])

    def test_scrub(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Session.objects.count(), 1)
        self.assertEqual(Revision.objects.count(), 4)
        self.assertEqual(TranslationSource.objects.count(), 1)
        self.assertEqual(SimpleRichTextPage.objects.count(), 3)

        call_command("scrub_exported_cms_data")

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Session.objects.count(), 0)
        self.assertEqual(Revision.objects.count(), 0)
        self.assertEqual(TranslationSource.objects.count(), 0)
        self.assertEqual(SimpleRichTextPage.objects.count(), 3)  # pages are unaffected


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
                call("Not bootstrapping an Admin user: WAGTAIL_ADMIN_EMAIL not defined in environment."),
            ],
        )

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "test@mozilla.com", "WAGTAIL_ADMIN_PASSWORD": ""})
    def test_email_available(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Created Admin user test@mozilla.com for local SSO use"),
            ],
        )

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "test@example.com", "WAGTAIL_ADMIN_PASSWORD": ""})
    def test_email_available_but_not_moco(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Not bootstrapping an Admin user: WAGTAIL_ADMIN_EMAIL is not a @mozilla.com email address."),
            ],
        )

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "test@mozilla.com", "WAGTAIL_ADMIN_PASSWORD": "secret"})
    def test_email_and_password_available(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Created Admin user test@mozilla.com with password 'secret'"),
            ],
        )

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "", "WAGTAIL_ADMIN_PASSWORD": ""})
    def test_only_password_available(self, mock_write):
        self._run_test(
            mock_write=mock_write,
            expected_output=[
                call("Not bootstrapping an Admin user: WAGTAIL_ADMIN_EMAIL not defined in environment."),
            ],
        )

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "test@mozilla.com", "WAGTAIL_ADMIN_PASSWORD": ""})
    def test_existing_user_exists_email_only(self, mock_write):
        out = StringIO()
        call_command("bootstrap_local_admin", stdout=out)
        call_command("bootstrap_local_admin", stdout=out)
        output = mock_write.call_args_list
        expected_output = [
            call("Created Admin user test@mozilla.com for local SSO use"),
            call("Admin user test@mozilla.com already exists"),
        ]
        self.assertEqual(output, expected_output)

    @patch.dict("os.environ", {"WAGTAIL_ADMIN_EMAIL": "test@mozilla.com", "WAGTAIL_ADMIN_PASSWORD": "secret"})
    def test_existing_user_exists_email_and_password(self, mock_write):
        out = StringIO()
        call_command("bootstrap_local_admin", stdout=out)
        call_command("bootstrap_local_admin", stdout=out)
        output = mock_write.call_args_list
        expected_output = [
            call("Created Admin user test@mozilla.com with password 'secret'"),
            call("Admin user test@mozilla.com already exists"),
        ]
        self.assertEqual(output, expected_output)
