from __future__ import print_function

from django.conf import settings
from django.core.management.base import BaseCommand

from bedrock.utils.git import GitRepo


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),

    def handle(self, *args, **options):
        repo = GitRepo(settings.RELEASE_NOTES_PATH, settings.RELEASE_NOTES_REPO,
                       branch_name=settings.RELEASE_NOTES_BRANCH)
        repo.update()
        if not options['quiet']:
            print('Release Notes Successfully Updated')
