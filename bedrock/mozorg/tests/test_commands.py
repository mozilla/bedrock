# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from pathlib import Path
from unittest.mock import DEFAULT, patch

from django.core.management import call_command
from django.test import override_settings

import pytest
import requests

from bedrock.mozorg.management.commands import update_product_details_files, update_root_store_policy_page, update_webvision_docs
from bedrock.mozorg.models import WebvisionDoc
from bedrock.mozorg.tests import TestCase

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


class TestUpdateWebvisionDocs:
    @pytest.fixture
    def git_repo(self):
        with patch.object(update_webvision_docs, "GitRepo") as git_mock:
            repo = git_mock.return_value
            repo.has_changes.return_value = True
            yield repo

    @pytest.fixture
    def refresh(self):
        with patch.object(WebvisionDoc.objects, "refresh", return_value=(3, 0)) as refresh_mock:
            yield refresh_mock

    def test_repo_is_built_from_settings(self, git_repo, refresh, settings):
        settings.WEBVISION_DOCS_PATH = "/app/data/webvisions"
        settings.WEBVISION_DOCS_REPO = "https://example.com/webvision.git"
        settings.WEBVISION_DOCS_BRANCH = "prod"

        call_command("update_webvision_docs")

        update_webvision_docs.GitRepo.assert_called_once_with(
            "/app/data/webvisions",
            "https://example.com/webvision.git",
            branch_name="prod",
            name="Webvision Docs",
        )
        git_repo.update.assert_called_once_with()

    def test_no_changes_loads_nothing(self, git_repo, refresh, capsys):
        git_repo.has_changes.return_value = False

        call_command("update_webvision_docs")

        refresh.assert_not_called()
        git_repo.set_db_latest.assert_not_called()
        assert "No webvision docs updates" in capsys.readouterr().out

    def test_force_loads_without_changes(self, git_repo, refresh):
        git_repo.has_changes.return_value = False

        call_command("update_webvision_docs", force=True)

        refresh.assert_called_once_with()
        git_repo.set_db_latest.assert_called_once_with()

    def test_docs_are_loaded(self, git_repo, refresh, capsys):
        call_command("update_webvision_docs")

        refresh.assert_called_once_with()
        git_repo.set_db_latest.assert_called_once_with()
        out = capsys.readouterr().out
        assert "3 webvision docs successfully loaded" in out
        assert "Saved latest git repo state to database" in out

    def test_errors_leave_repo_state_unsaved(self, git_repo, refresh, capsys):
        refresh.return_value = (2, 1)

        call_command("update_webvision_docs")

        git_repo.set_db_latest.assert_not_called()
        out = capsys.readouterr().out
        assert "2 webvision docs successfully loaded" in out
        assert "Encountered 1 errors while loading docs" in out

    def test_quiet(self, git_repo, refresh, capsys):
        call_command("update_webvision_docs", quiet=True)

        refresh.assert_called_once_with()
        assert capsys.readouterr().out == ""

    @patch("bedrock.utils.management.decorators.capture_exception")
    def test_error_goes_to_sentry(self, capture_exception, git_repo, refresh):
        error = RuntimeError("git fetch failed")
        git_repo.update.side_effect = error

        with pytest.raises(RuntimeError):
            call_command("update_webvision_docs")

        capture_exception.assert_called_once_with(error)
        refresh.assert_not_called()


POLICY_MD = """\
# Mozilla Root Store Policy

*Version 3.1*

## 1. Introduction

This policy covers [CAs](https://example.com/cas).

* first
* second

## 2. Certificate Authorities

### 2.1 CA Operations

1. Step one
   - nested
"""

POLICY_HTML = """\
<h1 class="mzp-c-article-title" id="mozilla-root-store-policy">Mozilla Root Store Policy</h1>
<p><em>Version 3.1</em></p>

<ol class="mzp-u-list-styled">
  <li><a href="#1-introduction">Introduction</a></li>
  <li><a href="#2-certificate-authorities">Certificate Authorities</a></li>
</ol>

<h2 id="1-introduction">1. Introduction</h2>
<p>This policy covers <a href="https://example.com/cas">CAs</a>.</p>
<ul class="mzp-u-list-styled">
<li>first</li>
<li>second</li>
</ul>
<h2 id="2-certificate-authorities">2. Certificate Authorities</h2>
<h3 id="21-ca-operations">2.1 CA Operations</h3>
<ol class="mzp-u-list-styled">
<li>Step one
<ul>
<li>nested</li>
</ul>
</li>
</ol>
"""


class TestUpdateRootStorePolicyPage:
    @pytest.fixture(autouse=True)
    def policy_response(self):
        with patch.object(update_root_store_policy_page.requests, "get") as get_mock:
            get_mock.return_value.text = POLICY_MD
            yield get_mock

    @pytest.fixture
    def dest(self, tmp_path):
        # The default dest is the real policy template, so every test passes this one
        return tmp_path / "policy.html"

    def expected_page(self, html):
        with open(update_root_store_policy_page.WRAPPING_TEMPLATE_PATH) as fp:
            return fp.read().replace("__HTML_POLICY_CONTENT_PLACEHOLDER__", html)

    def test_writes_the_policy_page(self, policy_response, dest, capsys):
        call_command("update_root_store_policy_page", dest_path=str(dest))

        policy_response.assert_called_once_with(update_root_store_policy_page.SOURCE_CERT_POLICY_DOCUMENT_URL)
        assert dest.read_text(encoding="utf-8") == self.expected_page(POLICY_HTML)
        out = capsys.readouterr().out
        assert f"Writing HTML to {dest}" in out
        assert out.endswith("Done!\n")

    def test_source_can_be_overridden(self, policy_response, dest):
        call_command("update_root_store_policy_page", source_url="https://example.com/policy.md", dest_path=str(dest))

        policy_response.assert_called_once_with("https://example.com/policy.md")

    def test_dry_run_prints_without_writing(self, dest, capsys):
        call_command("update_root_store_policy_page", dry_run=True, dest_path=str(dest))

        assert not dest.exists()
        out = capsys.readouterr().out
        assert "DRY RUN ONLY" in out
        assert self.expected_page(POLICY_HTML) in out

    def test_quiet(self, dest, capsys):
        call_command("update_root_store_policy_page", quiet=True, dest_path=str(dest))

        assert dest.exists()
        assert capsys.readouterr().out == ""

    def test_fetch_error_writes_nothing(self, policy_response, dest):
        policy_response.return_value.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

        with pytest.raises(requests.HTTPError):
            call_command("update_root_store_policy_page", dest_path=str(dest))

        assert not dest.exists()

    @pytest.mark.parametrize(
        "markdown, message",
        [
            ("## 1. Introduction\n\n* first\n", "No h1 found!"),
            ("# Mozilla Root Store Policy\n\n## 1. Introduction\n\nNo lists here.\n", "No list items found!"),
        ],
    )
    def test_unexpected_document_shape_writes_nothing(self, policy_response, dest, markdown, message):
        policy_response.return_value.text = markdown

        with pytest.raises(AssertionError, match=message):
            call_command("update_root_store_policy_page", dest_path=str(dest))

        assert not dest.exists()
