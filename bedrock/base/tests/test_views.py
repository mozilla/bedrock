# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import os
from datetime import datetime
from unittest.mock import patch

from django.conf import settings
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

import pytest
from waffle.models import Switch

from bedrock.base.views import (
    GeoTemplateView,
    cron_health_check,
    csrf_failure,
    get_db_file_url,
    get_extra_server_info,
    get_l10n_repo_info,
    page_gone_view,
    page_not_found_view,
    server_error_view,
)
from bedrock.utils.models import GitRepoState

geo_template_view = GeoTemplateView.as_view(
    geo_template_names={
        "DE": "firefox-klar.html",
        "GB": "firefox-focus.html",
    },
    template_name="firefox-mobile.html",
)


class TestGeoTemplateView(TestCase):
    def get_template(self, country):
        with patch("bedrock.firefox.views.l10n_utils.render") as render_mock:
            with patch("bedrock.base.views.get_country_from_request") as geo_mock:
                geo_mock.return_value = country
                rf = RequestFactory()
                req = rf.get("/")
                geo_template_view(req)
                return render_mock.call_args[0][1][0]

    def test_country_template(self):
        template = self.get_template("DE")
        assert template == "firefox-klar.html"

    def test_default_template(self):
        template = self.get_template("US")
        assert template == "firefox-mobile.html"

    def test_no_country(self):
        template = self.get_template(None)
        assert template == "firefox-mobile.html"


class TestErrorPages(TestCase):
    """Test error page handlers by calling them directly with mocked dependencies."""

    def check_error_handler(self, handler_func, expected_template, expected_status=200):
        with patch("lib.l10n_utils.render") as render_mock:
            rf = RequestFactory()
            req = rf.get("/")

            try:
                handler_func(req, exception=None)
            except TypeError:
                handler_func(req)

            args, kwargs = render_mock.call_args
            self.assertEqual(args[1], expected_template)
            self.assertEqual(kwargs.get("status"), expected_status)

    def test_404_handler(self):
        """Test 404 handler uses correct template and status."""
        self.check_error_handler(page_not_found_view, "404.html", 404)

    def test_410_handler(self):
        """Test 410 handler uses correct template and status."""
        self.check_error_handler(page_gone_view, "410.html", 410)

    def test_500_handler(self):
        """Test 500 handler uses correct template and status."""
        self.check_error_handler(server_error_view, "500.html", 500)


@pytest.mark.django_db
def test_csrf_view_is_custom_one():
    assert settings.CSRF_FAILURE_VIEW == "bedrock.base.views.csrf_failure"


def test_csrf_failure_renders_403():
    req = RequestFactory().post("/")
    with patch("bedrock.base.views.render", return_value=HttpResponse(status=403)) as render_mock:
        csrf_failure(req)

    render_mock.assert_called_once_with(req, "403_csrf.html", status=403)


class TestGetL10nRepoInfo:
    @patch("bedrock.base.views.git.GitRepo")
    def test_repo_info(self, repo_mock):
        repo = repo_mock.return_value
        repo.current_hash = "abc123"
        repo.last_updated = "2 days ago"
        repo.clean_remote_url = "https://github.com/mozmeao/www-l10n"
        repo.current_commit_timestamp = 1700000000

        assert get_l10n_repo_info() == {
            "latest_ref": "abc123",
            "last_updated": "2 days ago",
            "repo_url": "https://github.com/mozmeao/www-l10n",
            "last_updated_timestamp": datetime.fromtimestamp(1700000000),
        }
        repo_mock.assert_called_once_with(settings.FLUENT_REPO_PATH, settings.FLUENT_REPO_URL, settings.FLUENT_REPO_BRANCH)

    def test_missing_checkout(self, settings, tmp_path):
        settings.FLUENT_REPO_PATH = tmp_path / "missing"
        settings.FLUENT_REPO_URL = "https://github.com/mozmeao/www-l10n.git"

        assert get_l10n_repo_info() == {
            "latest_ref": None,
            "last_updated": "unknown",
            "repo_url": "https://github.com/mozmeao/www-l10n",
            "last_updated_timestamp": datetime.fromtimestamp(0),
        }


@patch("bedrock.base.views.GCS_BASE_URL", "https://storage.googleapis.com/bedrock-db-dev")
def test_get_db_file_url():
    assert get_db_file_url("public-abc.db") == "https://storage.googleapis.com/bedrock-db-dev/public-abc.db"


@patch("bedrock.base.views.GCS_BASE_URL", "https://storage.googleapis.com/bedrock-db-dev")
@patch("bedrock.base.views.GIT_SHA", "deadbeef")
class TestGetExtraServerInfo:
    @pytest.fixture(autouse=True)
    def db_info_file(self, settings, tmp_path):
        settings.HOSTNAME = "web-1"
        settings.CLUSTER_NAME = "prod"
        path = tmp_path / "bedrock_db_info.json"
        with patch("bedrock.base.views.DB_INFO_FILE", str(path)):
            yield path

    @pytest.mark.parametrize(
        "hostname, cluster_name, expected",
        (
            ("web-1", "prod", "web-1.prod"),
            ("web-1", "", "web-1"),
            ("", "prod", "prod"),
            ("", "", ""),
        ),
    )
    def test_server_name(self, settings, hostname, cluster_name, expected):
        settings.HOSTNAME = hostname
        settings.CLUSTER_NAME = cluster_name
        assert get_extra_server_info()["name"] == expected

    def test_no_db_info_file(self):
        assert get_extra_server_info() == {"name": "web-1.prod", "git_sha": "deadbeef"}

    def test_invalid_db_info_file(self, db_info_file):
        db_info_file.write_text("{not json")
        assert get_extra_server_info() == {"name": "web-1.prod", "git_sha": "deadbeef"}

    # timeago subtracts naive local times, so a real "1 hour ago" breaks across DST changes
    @patch("bedrock.base.views.timeago.format", return_value="1 hour ago")
    def test_db_info(self, format_mock, db_info_file):
        updated = 1700000000.5
        db_info_file.write_text(
            json.dumps(
                {
                    "updated": updated,
                    "checksum": "c0ffee",
                    "git_sha": "abc123",
                    "file_name": "public-abc123-c0ffee.db",
                }
            )
        )

        assert get_extra_server_info() == {
            "name": "web-1.prod",
            "git_sha": "deadbeef",
            "db_updated": updated,
            "db_checksum": "c0ffee",
            "db_git_sha": "abc123",
            "db_file_name": "public-abc123-c0ffee.db",
            "db_last_updated_timestamp": datetime.fromtimestamp(updated),
            "db_last_update": "1 hour ago",
            "db_file_url": "https://storage.googleapis.com/bedrock-db-dev/public-abc123-c0ffee.db",
        }
        format_mock.assert_called_once_with(datetime.fromtimestamp(updated))


@pytest.mark.django_db
class TestCronHealthCheck:
    NOW = 1700000000

    @pytest.fixture(autouse=True)
    def render_mock(self, settings, tmp_path):
        settings.DATA_PATH = tmp_path
        with (
            patch("bedrock.base.views.HEALTH_FILES", [("update_locales", 600), ("download_database", 60)]),
            patch("bedrock.base.views.time", return_value=self.NOW),
            patch("bedrock.base.views.get_l10n_repo_info", return_value={}),
            patch("bedrock.base.views.get_extra_server_info", return_value={}),
            patch("bedrock.base.views.render", return_value=HttpResponse()) as render_mock,
        ):
            yield render_mock

    def touch(self, tmp_path, name, age):
        path = tmp_path / f"last-run-{name}"
        path.touch()
        os.utime(path, (self.NOW - age, self.NOW - age))

    def get_context(self, render_mock):
        cron_health_check(RequestFactory().get("/healthz-cron/"))
        args, kwargs = render_mock.call_args
        assert args[1] == "cron-health-check.html"
        return args[2], kwargs["status"]

    def test_missing_files_fail(self, render_mock):
        context, status = self.get_context(render_mock)

        assert status == 500
        assert context["success"] is False
        assert context["results"] == [
            ("update_locales", 600, "None", False),
            ("download_database", 60, "None", False),
        ]

    def test_recent_runs_pass(self, render_mock, tmp_path):
        self.touch(tmp_path, "update_locales", 30)
        self.touch(tmp_path, "download_database", 60)

        context, status = self.get_context(render_mock)

        assert status == 200
        assert context["success"] is True
        assert context["results"] == [
            ("update_locales", 600, 30, True),
            ("download_database", 60, 60, True),
        ]

    def test_stale_run_fails(self, render_mock, tmp_path):
        self.touch(tmp_path, "update_locales", 30)
        self.touch(tmp_path, "download_database", 61)

        context, status = self.get_context(render_mock)

        assert status == 500
        assert context["success"] is False
        assert context["results"] == [
            ("update_locales", 600, 30, True),
            ("download_database", 60, 61, False),
        ]

    def test_git_repos(self, render_mock):
        GitRepoState.objects.create(repo_name="www-l10n", repo_id="1", latest_ref="old", latest_ref_timestamp=1600000000)
        GitRepoState.objects.create(repo_name="www-l10n", repo_id="2", latest_ref="new", latest_ref_timestamp=1650000000)
        GitRepoState.objects.create(repo_name="legal-docs", repo_id="3", latest_ref="legal", latest_ref_timestamp=1640000000)
        GitRepoState.objects.create(repo_name="", repo_id="4", latest_ref="unnamed", latest_ref_timestamp=1690000000)

        context, _ = self.get_context(render_mock)

        repos = list(context["git_repos"])
        assert [repo.latest_ref for repo in repos] == ["legal", "new"]
        assert [repo.last_updated_timestamp for repo in repos] == [
            datetime.fromtimestamp(1640000000),
            datetime.fromtimestamp(1650000000),
        ]
        assert context["most_recent_data_change_ts"] == datetime.fromtimestamp(1650000000)

    def test_no_git_repos(self, render_mock):
        context, _ = self.get_context(render_mock)

        assert list(context["git_repos"]) == []
        assert context["most_recent_data_change_ts"] is None

    def test_switches_sorted_by_name(self, render_mock):
        Switch.objects.create(name="SWITCH_B", active=False)
        Switch.objects.create(name="SWITCH_A", active=True)

        context, _ = self.get_context(render_mock)

        assert [switch.name for switch in context["switches"]] == ["SWITCH_A", "SWITCH_B"]

    def test_never_cached(self):
        response = cron_health_check(RequestFactory().get("/healthz-cron/"))
        assert "no-cache" in response["Cache-Control"]

    def test_post_not_allowed(self, render_mock):
        response = cron_health_check(RequestFactory().post("/healthz-cron/"))
        assert response.status_code == 405
        render_mock.assert_not_called()
