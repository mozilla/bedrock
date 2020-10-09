from django.core.management.base import BaseCommand

from bedrock.contentful.models import ContentfulEntry


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),
        parser.add_argument('-f', '--force', action='store_true', dest='force', default=False,
                            help='Load the data even if nothing new from git.'),

    def log(self, msg):
        if not self.quiet:
            print(msg)

    def handle(self, *args, **options):
        self.quiet = options['quiet']
        self.log('Updating Contentful Data')
        added, updated = ContentfulEntry.objects.refresh(options['force'])
        self.log(f'Done. Added: {added}. Updated: {updated}')
