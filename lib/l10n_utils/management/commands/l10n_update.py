# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.conf import settings

from bedrock.utils.git import GitRepo
from lib.l10n_utils.models import LangFile


class Command(BaseCommand):
    help = 'Clones or updates l10n info from github'
    quiet = False

    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),
        parser.add_argument('-f', '--force', action='store_true', dest='force', default=False,
                            help='Load the data even if nothing new from git. Implies -r.'),
        parser.add_argument('-r', '--refresh', action='store_true', dest='refresh', default=False,
                            help='Load l10n data into the DB if necessary.'),

    def output(self, msg):
        if not self.quiet:
            print(msg)

    def handle(self, *args, **options):
        self.quiet = options['quiet']
        repo = GitRepo(settings.LOCALES_PATH, settings.LOCALES_REPO)
        force = options['force']
        refresh = options['refresh'] or force

        self.output('Updating git repo')
        repo.update()
        if not refresh:
            self.output('Skipping database update')
            return

        if not (force or repo.has_changes()):
            self.output('No l10n updates')
            return

        self.output('Loading l10n data into the database')
        count = LangFile.objects.refresh()
        self.output('Successfully loaded %d lang files' % count)
        repo.set_db_latest()
        self.output('Saved latest git repo state to database')
        self.output('Done!')
