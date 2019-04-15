from __future__ import print_function
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string

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
        repo = GitRepo(settings.EXTERNAL_FILES_PATH, settings.EXTERNAL_FILES_REPO,
                       branch_name=settings.EXTERNAL_FILES_BRANCH,
                       name='Community Data')
        self.output('Updating git repo')
        repo.update()
        if not (options['force'] or repo.has_changes()):
            self.output('No community data updates')
            return

        self.output('Loading community data into database')

        for fid, finfo in settings.EXTERNAL_FILES.items():
            klass = import_string(finfo['type'])
            try:
                klass(fid).update()
            except ValueError as e:
                raise CommandError(str(e))

        self.output('Community data successfully loaded')

        repo.set_db_latest()

        self.output('Saved latest git repo state to database')
        self.output('Done!')
