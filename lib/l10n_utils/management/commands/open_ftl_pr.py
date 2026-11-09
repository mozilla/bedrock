# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import filecmp
import shutil
from datetime import datetime
from os import getenv
from pathlib import Path
from subprocess import CalledProcessError

from django.conf import settings
from django.core.management.base import CommandError
from django.template.defaultfilters import slugify
from django.utils.functional import cached_property

from dirsync import sync

from bedrock.utils import github

from ._ftl_repo_base import FTLRepoCommand

GIT_HASH = getenv("GIT_SHA", None)


class Command(FTLRepoCommand):
    help = "Open a pull-request on the L10n Team's repo for FTL file changes"
    branch_prefix = "update-from-bedrock"
    open_branch = None
    open_pr_url = None
    github = None

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        client = github.get_client()
        if client:
            self.github = client.get_repo(settings.FLUENT_L10N_TEAM_REPO)

        super().__init__(stdout, stderr, no_color, force_color)

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.get_open_pr()
        self.update_l10n_team_files()
        self.create_branch()
        self.sync_dirs()
        changed = self.commit_changes()
        if changed:
            self.push_changes()
            self.open_pr()

    @cached_property
    def branch_name(self):
        if self.open_branch:
            return self.open_branch

        if GIT_HASH:
            branch_suffix = GIT_HASH[:8]
        else:
            branch_suffix = slugify(datetime.now().isoformat())

        return f"{self.branch_prefix}-{branch_suffix}"

    @property
    def commit_message(self):
        message = "Updates from bedrock\n\n"
        if GIT_HASH:
            message += f"From file changes in https://github.com/mozilla/bedrock/commit/{GIT_HASH}"
        else:
            message += "From file changes in https://github.com/mozilla/bedrock/commits/main"

        return message

    def sync_dirs(self):
        """Mirror bedrock's l10n files into the l10n team repo.

        The root of the l10n team repo also contains all the locale folders,
        so it can't be synced with `purge`. Instead, each top-level folder
        that bedrock owns (e.g. `en`, `en-US`, `configs`) is synced and purged
        individually, so that files removed from bedrock are also removed from
        the l10n team repo. Top-level files (e.g. `l10n-pontoon.toml`) are only
        copied over.
        """
        source_path = Path(settings.FLUENT_LOCAL_PATH)
        target_path = Path(self.l10n_repo.path)
        for source in sorted(source_path.iterdir()):
            target = target_path / source.name
            if source.is_dir():
                sync(source, target, "sync", content=True, create=True, purge=True)
            elif not target.is_file() or not filecmp.cmp(source, target, shallow=False):
                shutil.copy2(source, target)

    def create_branch(self):
        if self.open_branch:
            self.stdout.write(f"Using existing branch: {self.branch_name}")
        else:
            self.l10n_repo.git("checkout", "-b", self.branch_name)
            self.stdout.write(f"Created branch: {self.branch_name}")

    def commit_changes(self):
        self.config_git()
        self.l10n_repo.git("add", ".")

        try:
            self.l10n_repo.git("commit", "-m", self.commit_message)
        except CalledProcessError:
            self.stdout.write("No changes to commit")
            return False

        self.stdout.write("Committed changes to local repo")
        return True

    def push_changes(self):
        if not self.l10n_repo.auth:
            raise CommandError("Git push authentication not configured")
        try:
            result = self.l10n_repo.push(f"HEAD:{self.branch_name}")
            self.stdout.write(result)
        except CalledProcessError as cpe:
            raise CommandError(f"There was a problem pushing to {self.l10n_repo.remote_url}: {cpe}\n{cpe.output}")

        commit = self.l10n_repo.git("rev-parse", "--short", "HEAD")
        self.stdout.write(f"Pushed {commit} to {self.l10n_repo.remote_url} as {self.branch_name}")

    def get_open_pr(self):
        if self.github is None:
            return

        for pr in self.github.get_pulls(state="open"):
            if pr.head.ref.startswith(self.branch_prefix):
                self.open_branch = pr.head.ref
                self.open_pr_url = pr.html_url
                self.l10n_repo.branch_name = self.open_branch
                return

    def open_pr(self):
        if self.github is None:
            return

        if self.open_branch:
            self.stdout.write(f"Updated existing pull-request: {self.open_pr_url}")
            return

        title, body = self.commit_message.split("\n\n")
        pr = self.github.create_pull(
            title=title,
            body=body,
            base=self.l10n_repo.branch_name,
            head=self.branch_name,
        )
        self.stdout.write(f"Opened a pull-request: {pr.html_url}")
