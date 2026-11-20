# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import call, patch

from django.core.management import call_command
from django.core.management.base import CommandError

import pytest

from bedrock.externalfiles.management.commands import update_externalfiles


@pytest.fixture
def git_repo():
    with patch.object(update_externalfiles, "GitRepo") as git_mock:
        repo = git_mock.return_value
        repo.has_changes.return_value = True
        yield repo


@pytest.fixture
def file_class():
    with patch.object(update_externalfiles, "import_string") as import_mock:
        yield import_mock.return_value


@pytest.fixture(autouse=True)
def external_files(settings):
    settings.EXTERNAL_FILES = {
        "credits": {"type": "bedrock.mozorg.credits.CreditsFile", "name": "credits/names.csv"},
        "example": {"type": "example.files.ExampleFile", "name": "example/data.csv"},
    }


def test_repo_is_built_from_settings(git_repo, file_class, settings):
    settings.EXTERNAL_FILES_PATH = "/app/data/community_data"
    settings.EXTERNAL_FILES_REPO = "https://example.com/community-data.git"
    settings.EXTERNAL_FILES_BRANCH = "main"

    call_command("update_externalfiles")

    update_externalfiles.GitRepo.assert_called_once_with(
        "/app/data/community_data",
        "https://example.com/community-data.git",
        branch_name="main",
        name="Community Data",
    )
    git_repo.update.assert_called_once_with()


def test_no_changes_loads_nothing(git_repo, file_class, capsys):
    git_repo.has_changes.return_value = False

    call_command("update_externalfiles")

    file_class.assert_not_called()
    git_repo.set_db_latest.assert_not_called()
    assert "No community data updates" in capsys.readouterr().out


def test_force_loads_without_changes(git_repo, file_class):
    git_repo.has_changes.return_value = False

    call_command("update_externalfiles", force=True)

    assert file_class.return_value.update.call_count == 2
    git_repo.set_db_latest.assert_called_once_with()


def test_every_external_file_is_updated(git_repo, file_class, capsys):
    call_command("update_externalfiles")

    assert update_externalfiles.import_string.call_args_list == [
        call("bedrock.mozorg.credits.CreditsFile"),
        call("example.files.ExampleFile"),
    ]
    assert file_class.call_args_list == [call("credits"), call("example")]
    assert file_class.return_value.update.call_count == 2
    git_repo.set_db_latest.assert_called_once_with()
    out = capsys.readouterr().out
    assert "Community data successfully loaded" in out
    assert out.endswith("Done!\n")


def test_invalid_file_fails_without_saving_repo_state(git_repo, file_class):
    file_class.return_value.update.side_effect = ValueError("Much smaller file than expected. 12 rows.")

    with pytest.raises(CommandError, match="Much smaller file than expected"):
        call_command("update_externalfiles")

    git_repo.set_db_latest.assert_not_called()


def test_quiet(git_repo, file_class, capsys):
    call_command("update_externalfiles", quiet=True)

    assert file_class.return_value.update.call_count == 2
    assert capsys.readouterr().out == ""


@patch("bedrock.utils.management.decorators.capture_exception")
def test_error_goes_to_sentry(capture_exception, git_repo, file_class):
    file_class.return_value.update.side_effect = ValueError("credits/names.csv is empty")

    with pytest.raises(CommandError):
        call_command("update_externalfiles")

    error = capture_exception.call_args.args[0]
    assert isinstance(error, CommandError)
    assert str(error) == "credits/names.csv is empty"
