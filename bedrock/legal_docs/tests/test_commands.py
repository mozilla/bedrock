# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.core.management import call_command

import pytest

from bedrock.legal_docs.management.commands import update_legal_docs
from bedrock.legal_docs.models import LegalDoc

from .test_models import write_doc


@pytest.fixture
def git_repo():
    """Stand in for the legal-docs git checkout, with changes waiting by default."""
    with patch.object(update_legal_docs, "GitRepo") as git_mock:
        repo = git_mock.return_value
        repo.has_changes.return_value = True
        yield repo


@pytest.fixture
def refresh():
    with patch.object(LegalDoc.objects, "refresh", return_value=(3, 0)) as refresh_mock:
        yield refresh_mock


@pytest.fixture(autouse=True)
def requests_mock():
    """Autouse so a locally configured LEGAL_DOCS_DMS_URL can never ping the real snitch."""
    with patch.object(update_legal_docs, "requests") as mock:
        yield mock


class TestRepoUpdate:
    def test_repo_is_built_from_settings(self, git_repo, refresh, settings):
        settings.LEGAL_DOCS_PATH = "/app/data/legal_docs"
        settings.LEGAL_DOCS_REPO = "https://example.com/legal-docs.git"
        settings.LEGAL_DOCS_BRANCH = "prod"

        call_command("update_legal_docs")

        update_legal_docs.GitRepo.assert_called_once_with(
            "/app/data/legal_docs",
            "https://example.com/legal-docs.git",
            branch_name="prod",
            name="Legal Docs",
        )

    def test_repo_is_always_updated(self, git_repo, refresh):
        call_command("update_legal_docs")
        git_repo.update.assert_called_once_with()


class TestNoChanges:
    def test_docs_are_not_reloaded(self, git_repo, refresh, capsys):
        git_repo.has_changes.return_value = False

        call_command("update_legal_docs")

        refresh.assert_not_called()
        git_repo.set_db_latest.assert_not_called()
        assert "No legal docs updates" in capsys.readouterr().out

    def test_snitch_is_still_pinged(self, git_repo, refresh, requests_mock, settings):
        # nothing to do is a healthy outcome, so the dead man's switch must still hear from us
        settings.LEGAL_DOCS_DMS_URL = "https://snitch.example.com/abc123"
        git_repo.has_changes.return_value = False

        call_command("update_legal_docs")

        requests_mock.get.assert_called_once_with("https://snitch.example.com/abc123")

    def test_force_reloads_anyway(self, git_repo, refresh):
        git_repo.has_changes.return_value = False

        call_command("update_legal_docs", "--force")

        refresh.assert_called_once_with()

    def test_force_short_circuits_the_changes_check(self, git_repo, refresh):
        call_command("update_legal_docs", "-f")
        git_repo.has_changes.assert_not_called()


class TestSuccessfulLoad:
    def test_docs_are_reloaded(self, git_repo, refresh):
        call_command("update_legal_docs")
        refresh.assert_called_once_with()

    def test_latest_ref_is_saved(self, git_repo, refresh):
        call_command("update_legal_docs")
        git_repo.set_db_latest.assert_called_once_with()

    def test_snitch_is_pinged(self, git_repo, refresh, requests_mock, settings):
        settings.LEGAL_DOCS_DMS_URL = "https://snitch.example.com/abc123"

        call_command("update_legal_docs")

        requests_mock.get.assert_called_once_with("https://snitch.example.com/abc123")

    def test_progress_is_reported(self, git_repo, refresh, capsys):
        call_command("update_legal_docs")

        out = capsys.readouterr().out
        assert "Updating git repo" in out
        assert "Loading legal docs into database" in out
        assert "3 legal docs successfully loaded" in out
        assert "Saved latest git repo state to database" in out
        assert "Done!" in out

    def test_quiet_suppresses_output(self, git_repo, refresh, capsys):
        call_command("update_legal_docs", "--quiet")
        assert capsys.readouterr().out == ""


class TestPartialLoad:
    def test_latest_ref_is_not_saved(self, git_repo, refresh):
        # leaving the ref behind means the next run retries the failed docs
        refresh.return_value = (2, 1)

        call_command("update_legal_docs")

        git_repo.set_db_latest.assert_not_called()

    def test_snitch_is_not_pinged(self, git_repo, refresh, requests_mock, settings):
        # staying quiet is what alerts us that the load is broken
        settings.LEGAL_DOCS_DMS_URL = "https://snitch.example.com/abc123"
        refresh.return_value = (2, 1)

        call_command("update_legal_docs")

        requests_mock.get.assert_not_called()

    def test_errors_are_reported(self, git_repo, refresh, capsys):
        refresh.return_value = (2, 1)

        call_command("update_legal_docs")

        out = capsys.readouterr().out
        assert "2 legal docs successfully loaded" in out
        assert "Encountered 1 errors while loading docs" in out
        assert "Done!" in out


class TestSnitch:
    def test_unset_dms_url_pings_nothing(self, git_repo, refresh, requests_mock, settings):
        settings.LEGAL_DOCS_DMS_URL = ""

        call_command("update_legal_docs")

        requests_mock.get.assert_not_called()


class TestFailuresReachSentry:
    def test_exception_is_captured_and_re_raised(self, git_repo, refresh):
        refresh.side_effect = ValueError("boom")

        with patch("bedrock.utils.management.decorators.capture_exception") as capture_mock:
            with pytest.raises(ValueError):
                call_command("update_legal_docs")

        assert isinstance(capture_mock.call_args[0][0], ValueError)


@pytest.mark.django_db
class TestEndToEnd:
    def test_docs_on_disk_end_up_in_the_database(self, git_repo, requests_mock, tmp_path, settings, capsys):
        settings.LEGAL_DOCS_PATH = tmp_path
        settings.LEGAL_DOCS_DMS_URL = "https://snitch.example.com/abc123"
        write_doc(tmp_path, "en", "websites_privacy_notice", "Legalese")
        write_doc(tmp_path, "de", "websites_privacy_notice", "")

        call_command("update_legal_docs")

        assert LegalDoc.objects.values_list("name", "locale").get() == ("websites_privacy_notice", "en")
        out = capsys.readouterr().out
        assert "1 legal docs successfully loaded" in out
        assert "Encountered 1 errors while loading docs" in out
        # the empty German doc failed, so neither the ref nor the snitch is updated
        git_repo.set_db_latest.assert_not_called()
        requests_mock.get.assert_not_called()
