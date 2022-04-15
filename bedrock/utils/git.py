# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
from datetime import datetime
from hashlib import sha256
from io import StringIO
from pathlib import Path
from shutil import rmtree
from subprocess import STDOUT, CalledProcessError, check_output
from time import time

from django.conf import settings
from django.utils.encoding import force_str

import timeago

from bedrock.utils.models import GitRepoState

GIT = getattr(settings, "GIT_BIN", "git")


class GitRepo:
    def __init__(self, path, remote_url=None, branch_name="main", name=None):
        self.path = Path(path)
        self.path_str = str(self.path)
        self.remote_url = remote_url
        self.branch_name = branch_name
        db_latest_key = f"{self.path_str}:{remote_url or ''}:{branch_name}"
        self.db_latest_key = sha256(db_latest_key.encode()).hexdigest()
        self.repo_name = name or self.path.name

    def git(self, *args):
        """Run a git command against the current repo"""
        curdir = os.getcwd()
        try:
            os.chdir(self.path_str)
            output = check_output((GIT,) + args, stderr=STDOUT)
        finally:
            os.chdir(curdir)

        return force_str(output.strip())

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
        self.git("clone", "--depth", "1", "--branch", self.branch_name, self.remote_url, ".")

    def reclone(self):
        """Safely get a fresh clone of the repo"""
        if self.path.exists():
            new_path = self.path.with_suffix(f".{int(time())}")
            new_repo = GitRepo(new_path, self.remote_url, self.branch_name)
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
        self.git("fetch", "-f", self.remote_url, self.branch_name)
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
