from django.core.management.base import BaseCommand
from django.conf import settings
from _humans import generate_file


class Command(BaseCommand):
    args = 'None'
    help = 'Generates humans.txt in the MEDIA_ROOT Directory' +\
           ' using HUMANSTXT_*_REPO in settings.py'

    def handle(self, *args, **options):
        repos = settings.HUMANSTXT_REPOS
        target = open(settings.MEDIA_ROOT + "/humans.txt", 'w')
        with open(settings.MEDIA_ROOT + "/humans.txt", 'w') as target:
            generate_file(target, repos)
        self.stdout.write('Done')
