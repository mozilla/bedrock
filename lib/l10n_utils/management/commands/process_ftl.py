# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from io import StringIO

from django.core.management.base import BaseCommand
from django.conf import settings

from bedrock.utils.git import GitRepo


class Command(BaseCommand):
    help = 'Processes .ftl files from l10n team for use in bedrock'

    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),

    def handle(self, *args, **options):
        if options['quiet']:
            self.stdout._out = StringIO()

        self.update_fluent_files()
        self.update_l10n_team_files()

    def update_l10n_team_files(self):
        repo = GitRepo(settings.FLUENT_L10N_TEAM_REPO_PATH, settings.FLUENT_L10N_TEAM_REPO)
        repo.update()
        self.stdout.write('Updated l10n team .ftl files')

    def update_fluent_files(self):
        repo = GitRepo(settings.FLUENT_REPO_PATH, settings.FLUENT_REPO)
        repo.update()
        self.stdout.write('Updated .ftl files')
