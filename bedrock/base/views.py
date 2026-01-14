# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import os.path
from datetime import datetime
from os import getenv
from time import time

from django.conf import settings
from django.shortcuts import render
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe

import timeago
from waffle.models import Switch

from bedrock.base.config_manager import config
from bedrock.base.geo import get_country_from_request
from bedrock.base.i18n import get_language_from_headers
from bedrock.base.middleware import BedrockLocaleMiddleware
from bedrock.utils import git
from lib import l10n_utils


class GeoTemplateView(l10n_utils.L10nTemplateView):
    """Use the template appropriate to the request country

    Set the `geo_template_names` variable to a mapping of country codes to template names.

    If the requesting country isn't in the list it falls back to the `template_name`
    setting like the normal TemplateView class.
    """

    # dict of country codes to template names
    geo_template_names = {}

    def get_template_names(self):
        country_code = get_country_from_request(self.request)
        template = self.geo_template_names.get(country_code)
        if template:
            return [template]

        return super().get_template_names()


SQLITE_DB_IN_USE = settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
LOCAL_DB_UPDATE = config("LOCAL_DB_UPDATE", default="False", parser=bool)

HEALTH_FILES = [
    # Format: (file name, max seconds since last run)
    ("update_locales", 600),
]

# Only check download_database health when using SQLite AND downloading from S3
# (not when doing local DB updates)
if SQLITE_DB_IN_USE and not LOCAL_DB_UPDATE:
    HEALTH_FILES.insert(
        0,
        ("download_database", 600),
    )

DB_INFO_FILE = getenv("AWS_DB_JSON_DATA_FILE", f"{settings.DATA_PATH}/bedrock_db_info.json")
GIT_SHA = getenv("GIT_SHA")
BUCKET_NAME = getenv("AWS_DB_S3_BUCKET", "bedrock-db-dev")
REGION_NAME = os.getenv("AWS_DB_REGION", "us-west-2")
S3_BASE_URL = f"https://s3-{REGION_NAME}.amazonaws.com/{BUCKET_NAME}"


def get_l10n_repo_info():
    fluent_repo = git.GitRepo(settings.FLUENT_REPO_PATH, settings.FLUENT_REPO_URL, settings.FLUENT_REPO_BRANCH)
    data = {
        "latest_ref": fluent_repo.current_hash,
        "last_updated": fluent_repo.last_updated,
        "repo_url": fluent_repo.clean_remote_url,
    }
    try:
        data["last_updated_timestamp"] = datetime.fromtimestamp(fluent_repo.current_commit_timestamp)
    except AttributeError:
        pass
    return data


def get_db_file_url(filename):
    return "/".join([S3_BASE_URL, filename])


def get_extra_server_info():
    server_name = [getattr(settings, x) for x in ["HOSTNAME", "CLUSTER_NAME"]]
    server_name = ".".join(x for x in server_name if x)
    server_info = {
        "name": server_name,
        "git_sha": GIT_SHA,
    }
    try:
        with open(DB_INFO_FILE) as fp:
            db_info = json.load(fp)
    except (OSError, ValueError):
        pass
    else:
        last_updated_timestamp = datetime.fromtimestamp(db_info["updated"])
        db_info["last_updated_timestamp"] = last_updated_timestamp
        db_info["last_update"] = timeago.format(last_updated_timestamp)
        db_info["file_url"] = get_db_file_url(db_info["file_name"])
        for key, value in db_info.items():
            server_info[f"db_{key}"] = value

    return server_info


@require_safe
@never_cache
def cron_health_check(request):
    results = []
    check_pass = True
    for fname, max_time in HEALTH_FILES:
        fpath = f"{settings.DATA_PATH}/last-run-{fname}"
        try:
            last_check = os.path.getmtime(fpath)
        except OSError:
            check_pass = False
            results.append((fname, max_time, "None", False))
            continue

        time_since = int(time() - last_check)
        if time_since > max_time:
            task_pass = False
            check_pass = False
        else:
            task_pass = True

        results.append((fname, max_time, time_since, task_pass))

    git_repos = git.GitRepoState.objects.exclude(repo_name="").order_by("repo_name", "-latest_ref_timestamp")
    unique_repos = {}
    for repo in git_repos:
        if repo.repo_name in unique_repos:
            continue
        unique_repos[repo.repo_name] = repo
        setattr(
            unique_repos[repo.repo_name],
            "last_updated_timestamp",
            datetime.fromtimestamp(repo.latest_ref_timestamp),
        )

    try:
        most_recent_data_change_ts = sorted([x.last_updated_timestamp for x in unique_repos.values()])[-1]
    except IndexError:
        most_recent_data_change_ts = None

    return render(
        request,
        "cron-health-check.html",
        {
            "results": results,
            "server_info": get_extra_server_info(),
            "success": check_pass,
            "git_repos": unique_repos.values(),
            "fluent_repo": get_l10n_repo_info(),
            "SQLITE_DB_IN_USE": SQLITE_DB_IN_USE,
            "most_recent_data_change_ts": most_recent_data_change_ts,
            "switches": Switch.objects.order_by("name"),
        },
        status=200 if check_pass else 500,
    )


def server_error_view(request, template_name="500.html"):
    """500 error handler that runs context processors."""
    return l10n_utils.render(request, template_name, ftl_files=["500"], status=500)


def page_not_found_view(request, exception=None, template_name="404.html"):
    """404 error handler that runs context processors."""
    return l10n_utils.render(request, template_name, ftl_files=["404", "500"], status=404)


def page_gone_view(request, exception=None, template_name="410.html"):
    """410 error handler that runs context processors."""

    # In a normal request, this would happen in bedrock.base.middleware.BedrockLangCodeFixupMiddleware
    # But requests that get here don't go through that middleware
    lang_code = request.GET.get("lang", None) or get_language_from_headers(request)
    request.locale = lang_code if lang_code else ""

    locale_middleware = decorator_from_middleware(BedrockLocaleMiddleware)

    @locale_middleware
    def _view(request):
        return l10n_utils.render(request, template_name, ftl_files=["410", "500"], status=410, non_locale_url=True)

    return _view(request)


def csrf_failure(request, reason="CSRF failure", template_name="403_csrf.html"):
    return render(request, template_name, status=403)
