# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from io import StringIO

from django.core.management.base import BaseCommand
from django.conf import settings

from bedrock.sitemaps.models import SitemapURL
from bedrock.utils.git import GitRepo


class Command(BaseCommand):
    help = 'Clones or updates sitemaps info from github'

    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),
        parser.add_argument('-f', '--force', action='store_true', dest='force', default=False,
                            help='Load the data even if nothing new from git.'),

    def handle(self, *args, **options):
        if options['quiet']:
            self.stdout._out = StringIO()

        repo = GitRepo(settings.SITEMAPS_PATH, settings.SITEMAPS_REPO,
                       name='Sitemaps')
        self.stdout.write('Updating git repo')
        repo.update()
        if not (options['force'] or repo.has_changes()):
            self.stdout.write('No sitemap updates')
            return

        SitemapURL.objects.refresh()
        repo.set_db_latest()
        self.stdout.write('Updated sitemaps files')
