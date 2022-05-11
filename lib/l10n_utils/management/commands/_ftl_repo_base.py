# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from io import StringIO

from django.conf import settings
from django.core.management.base import BaseCommand

from bedrock.utils.git import GitRepo

GIT_COMMIT_EMAIL = "meao-bots+mozmarrobot@mozilla.com"
GIT_COMMIT_NAME = "MozMEAO Bot"


class FTLRepoCommand(BaseCommand):
    meao_repo = None
    l10n_repo = None

    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output.")

    def handle(self, *args, **options):
        if options["quiet"]:
            self.stdout._out = StringIO()

        self.l10n_repo = GitRepo(settings.FLUENT_L10N_TEAM_REPO_PATH, settings.FLUENT_L10N_TEAM_REPO_URL, settings.FLUENT_L10N_TEAM_REPO_BRANCH)
        self.meao_repo = GitRepo(settings.FLUENT_REPO_PATH, settings.FLUENT_REPO_URL, settings.FLUENT_REPO_BRANCH)

    def update_l10n_team_files(self):
        try:
            # this will fail on first run
            self.l10n_repo.clean()
        except FileNotFoundError:
            pass
        self.l10n_repo.update()
        self.stdout.write(f"Updated l10n team .ftl files for {settings.FLUENT_L10N_TEAM_REPO_URL}")

    def update_fluent_files(self):
        try:
            self.meao_repo.clean()
        except FileNotFoundError:
            pass
        self.meao_repo.update()
        self.stdout.write(f"Updated .ftl files for {settings.FLUENT_REPO_URL}")

    def config_git(self):
        """Set user config so that committing will work"""
        for repo in (self.meao_repo, self.l10n_repo):
            repo.git("config", "user.email", GIT_COMMIT_EMAIL)
            repo.git("config", "user.name", GIT_COMMIT_NAME)
