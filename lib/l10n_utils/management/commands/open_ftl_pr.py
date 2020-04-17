# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime
from os import getenv
from subprocess import CalledProcessError

from django.core.management.base import CommandError
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.functional import cached_property

from bedrock.utils import github

from dirsync import sync

from ._ftl_repo_base import FTLRepoCommand


GIT_HASH = getenv('GIT_SHA', None)


class Command(FTLRepoCommand):
    help = "Open a pull-request on the L10n Team's reop for FTL file changes"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.update_l10n_team_files()
        self.create_branch()
        self.sync_dirs()
        changed = self.commit_changes()
        if changed:
            self.push_changes()
            self.open_pr()

    @cached_property
    def branch_name(self):
        if GIT_HASH:
            branch_suffix = GIT_HASH[:8]
        else:
            branch_suffix = slugify(datetime.now().isoformat())

        return f'update-from-bedrock-{branch_suffix}'

    @property
    def commit_message(self):
        message = 'Updates from bedrock\n\n'
        if GIT_HASH:
            message += f'From file changes in https://github.com/mozilla/bedrock/commit/{GIT_HASH}'
        else:
            message += 'From file changes in https://github.com/mozilla/bedrock/commits/master'

        return message

    def sync_dirs(self):
        sync(settings.FLUENT_LOCAL_PATH, self.l10n_repo.path, 'sync', content=True)

    def create_branch(self):
        self.l10n_repo.git('checkout', '-b', self.branch_name)
        self.stdout.write(f'Created branch: {self.branch_name}')

    def commit_changes(self):
        self.config_git()
        self.l10n_repo.git('add', '.')

        try:
            self.l10n_repo.git('commit', '-m', self.commit_message)
        except CalledProcessError:
            self.stdout.write('No changes to commit')
            return False

        self.stdout.write('Committed changes to local repo')
        return True

    def push_changes(self):
        try:
            self.l10n_repo.git('push', self.git_push_url, 'HEAD')
        except CalledProcessError:
            raise CommandError(f'There was a problem pushing to {self.l10n_repo.remote_url}')

        commit = self.l10n_repo.git('rev-parse', '--short', 'HEAD')
        self.stdout.write(f'Pushed {commit} to {self.l10n_repo.remote_url} as {self.branch_name}')

    @property
    def git_push_url(self):
        if not settings.FLUENT_REPO_AUTH:
            raise CommandError('Git push authentication not configured')

        return self.l10n_repo.remote_url_auth(settings.FLUENT_REPO_AUTH)

    def open_pr(self):
        client = github.get_client()
        if not client:
            return

        title, body = self.commit_message.split('\n\n')
        repo = client.get_repo(settings.FLUENT_L10N_TEAM_REPO)
        pr = repo.create_pull(
            title=title,
            body=body,
            base='master',
            head=self.branch_name,
        )
        self.stdout.write(f'Opened a pull-request: {pr.html_url}')
