from __future__ import print_function
from django.conf import settings
from django.core.management.base import BaseCommand

from bedrock.releasenotes.models import ProductRelease
from bedrock.utils.git import GitRepo


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),
        parser.add_argument('-f', '--force', action='store_true', dest='force', default=False,
                            help='Load the data even if nothing new from git.'),

    def output(self, msg):
        if not self.quiet:
            print(msg)

    def handle(self, *args, **options):
        self.quiet = options['quiet']
        repo = GitRepo(settings.RELEASE_NOTES_PATH, settings.RELEASE_NOTES_REPO,
                       branch_name=settings.RELEASE_NOTES_BRANCH, name='Release Notes')
        self.output('Updating git repo')
        repo.update()
        if not (options['force'] or repo.has_changes()):
            self.output('No release note updates')
            return

        self.output('Loading releases into database')
        count = ProductRelease.objects.refresh()

        self.output('%s release notes successfully loaded' % count)

        repo.set_db_latest()

        self.output('Saved latest git repo state to database')
        self.output('Done!')
