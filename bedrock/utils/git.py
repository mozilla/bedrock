# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import base64
import contextlib
import os
from datetime import datetime
from hashlib import sha256
from io import StringIO
from pathlib import Path
from shutil import rmtree
from subprocess import STDOUT, CalledProcessError, check_output
from time import time
from urllib.parse import urlparse

from django.conf import settings
from django.utils.encoding import force_str

import timeago

from bedrock.utils.models import GitRepoState

GIT = getattr(settings, "GIT_BIN", "git")

# Conventional GitHub username for token-only auth (fine-grained PATs).
DEFAULT_AUTH_USERNAME = "x-access-token"


class GitRepo:
    def __init__(self, path, remote_url=None, branch_name="main", name=None, auth=None):
        self.path = Path(path)
        self.path_str = str(self.path)
        self.remote_url = remote_url
        self.branch_name = branch_name
        self.auth = auth or None
        db_latest_key = f"{self.path_str}:{remote_url or ''}:{branch_name}"
        self.db_latest_key = sha256(db_latest_key.encode()).hexdigest()
        self.repo_name = name or self.path.name

    def git(self, *args, env=None):
        """Run a git command against the current repo"""
        curdir = os.getcwd()
        try:
            os.chdir(self.path_str)
            kwargs = {"stderr": STDOUT}
            if env is not None:
                kwargs["env"] = {**os.environ, **env}
            output = check_output((GIT,) + args, **kwargs)
        finally:
            os.chdir(curdir)

        return force_str(output.strip())

    def _split_auth(self):
        """Return (username, token) parsed from self.auth.

        Accepts either ``"<username>:<token>"`` (matches the existing
        ``FLUENT_REPO_AUTH`` convention) or a bare ``"<token>"``. Returns
        ``(None, None)`` if no auth is configured.
        """
        if not self.auth:
            return None, None
        if ":" in self.auth:
            username, token = self.auth.split(":", 1)
            return (username or DEFAULT_AUTH_USERNAME), token
        return DEFAULT_AUTH_USERNAME, self.auth

    @contextlib.contextmanager
    def _auth_env(self):
        """Yield env overrides that authenticate git via HTTP Basic auth.

        Uses git's ``GIT_CONFIG_COUNT`` / ``GIT_CONFIG_KEY_N`` /
        ``GIT_CONFIG_VALUE_N`` env-var protocol (git >= 2.31) to set
        ``http.extraheader`` for the duration of the subprocess. The token
        lives only in the subprocess environment — it never enters argv,
        git's error output, or the ``CalledProcessError`` payload that the
        ``@alert_sentry_on_exception`` decorator would otherwise ship.

        Yields ``None`` when no auth is configured.
        """
        if not self.auth:
            yield None
            return

        username, token = self._split_auth()
        basic = base64.b64encode(f"{username}:{token}".encode()).decode("ascii")
        yield {
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": self._extraheader_config_key(),
            "GIT_CONFIG_VALUE_0": f"AUTHORIZATION: Basic {basic}",
            "GIT_TERMINAL_PROMPT": "0",
        }

    def _extraheader_config_key(self):
        """Return the git config key for the http.extraheader setting,
        scoped to the remote's scheme+host when possible.

        Per git's URL-specific HTTP config rules, ``http.<url>.extraheader``
        only applies to requests whose URL is prefix-matched by ``<url>``.
        Scoping to e.g. ``http.https://github.com/.extraheader`` means
        the ``Authorization`` header won't follow off-host redirects or
        LFS fetches against unrelated hosts during the clone/fetch.

        Falls back to the global ``http.extraheader`` if the remote URL
        isn't usable HTTPS (e.g. SSH form, missing host).
        """
        parsed = urlparse(self.remote_url or "")
        if parsed.scheme in ("http", "https") and parsed.hostname:
            return f"http.{parsed.scheme}://{parsed.hostname}/.extraheader"
        return "http.extraheader"

    @property
    def current_hash(self):
        """The git revision ID (hash) of the current HEAD or None if no repo"""
        try:
            return self.git("rev-parse", "HEAD")
        except (OSError, CalledProcessError):
            return None

    @property
    def current_commit_timestamp(self):
        """The UNIX timestamp of the latest commit"""
        try:
            return int(self.git("show", "-s", "--format=%ct", "HEAD"))
        except (OSError, CalledProcessError, ValueError):
            return 0

    @property
    def last_updated(self):
        if self.current_commit_timestamp:
            latest_datetime = datetime.fromtimestamp(self.current_commit_timestamp)
            return timeago.format(latest_datetime)

        return "unknown"

    def diff(self, start_hash, end_hash):
        """Return a 2 tuple: (modified files, deleted files)"""
        diff_out = StringIO(self.git("diff", "--name-status", start_hash, end_hash))
        return self._parse_git_status(diff_out)

    def modified_files(self):
        """Return a list of new or modified files according to git"""
        self.git("add", ".")
        status = StringIO(self.git("status", "--porcelain"))
        return self._parse_git_status(status)

    def _parse_git_status(self, lines):
        modified = set()
        removed = set()
        for line in lines:
            parts = line.split()
            # delete
            if parts[0] == "D":
                removed.add(parts[1])
            # rename
            elif parts[0][0] == "R":
                removed.add(parts[1])
                modified.add(parts[2])
            # everything else
            else:
                # some types (like copy) have two file entries
                for part in parts[1:]:
                    modified.add(part)

        return modified, removed

    def clone(self):
        """Clone the repo specified in the initial arguments"""
        if not self.remote_url:
            raise RuntimeError("remote_url required to clone")

        self.path.mkdir(parents=True, exist_ok=True)
        with self._auth_env() as env:
            extra = {"env": env} if env else {}
            self.git("clone", "--depth", "1", "--branch", self.branch_name, self.remote_url, ".", **extra)

    def reclone(self):
        """Safely get a fresh clone of the repo"""
        if self.path.exists():
            new_path = self.path.with_suffix(f".{int(time())}")
            new_repo = GitRepo(new_path, self.remote_url, self.branch_name, auth=self.auth)
            new_repo.clone()
            # only remove the old after the new clone succeeds
            rmtree(self.path_str, ignore_errors=True)
            new_path.rename(self.path)
        else:
            self.clone()

    def pull(self):
        """Update the repo to the latest of the remote and branch

        Return the previous hash and the new hash."""
        old_hash = self.current_hash
        with self._auth_env() as env:
            extra = {"env": env} if env else {}
            self.git("fetch", "-f", self.remote_url, self.branch_name, **extra)
        self.git("checkout", "-f", "FETCH_HEAD")
        return old_hash, self.current_hash

    def update(self):
        """Updates a repo, cloning if necessary.

        :return a tuple of lists of modified and deleted files if updated, None if cloned
        """
        if self.path.is_dir():
            if not self.path.joinpath(".git").is_dir():
                rmtree(self.path_str, ignore_errors=True)
                self.clone()
            else:
                return self.pull()
        else:
            self.clone()

        return None, None

    def reset(self, new_head):
        self.git("reset", "--hard", new_head)

    def clean(self):
        self.git("clean", "-fd")

    def get_db_latest(self):
        try:
            return GitRepoState.objects.get(repo_id=self.db_latest_key).latest_ref
        except GitRepoState.DoesNotExist:
            return None

    def has_changes(self):
        return self.current_hash != self.get_db_latest()

    @property
    def clean_remote_url(self):
        repo_base = self.remote_url
        if repo_base.endswith(".git"):
            repo_base = repo_base[:-4]
        elif repo_base.endswith("/"):
            repo_base = repo_base[:-1]

        return repo_base

    def remote_url_auth(self, auth):
        url = self.clean_remote_url
        # remove https://
        url = url[8:]
        return f"https://{auth}@{url}"

    def set_db_latest(self, latest_ref=None):
        latest_ref = latest_ref or self.current_hash
        rs, created = GitRepoState.objects.get_or_create(
            repo_id=self.db_latest_key,
            defaults={
                "latest_ref": latest_ref,
                "repo_name": self.repo_name,
                "repo_url": self.clean_remote_url,
                "latest_ref_timestamp": self.current_commit_timestamp,
            },
        )
        if not created:
            rs.latest_ref = latest_ref
            rs.repo_name = self.repo_name
            rs.repo_url = self.clean_remote_url
            rs.latest_ref_timestamp = self.current_commit_timestamp
            rs.save()
