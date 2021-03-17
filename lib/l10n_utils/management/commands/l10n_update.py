# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from io import StringIO

from django.core.management.base import BaseCommand
from django.conf import settings

from bedrock.utils.git import GitRepo


class Command(BaseCommand):
    help = 'Clones or updates l10n info from github'

    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),
        parser.add_argument('-c', '--clean', action='store_true', dest='clean', default=False,
                            help='Remove old repos if they exist and do fresh clones.'),

    def handle(self, *args, **options):
        if options['quiet']:
            self.stdout._out = StringIO()

        self.update_lang_files(options['clean'])
        self.update_fluent_files(options['clean'])

    def update_lang_files(self, clean=False):
        repo = GitRepo(settings.LOCALES_PATH, settings.LOCALES_REPO)
        if clean:
            repo.reclone()
        else:
            repo.update()

        self.stdout.write('Updated .lang files')

    def update_fluent_files(self, clean=False):
        repo = GitRepo(settings.FLUENT_REPO_PATH, settings.FLUENT_REPO_URL)
        if clean:
            repo.reclone()
        else:
            repo.update()

        repo.update()
        self.stdout.write('Updated .ftl files')
