from __future__ import print_function
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bedrock.pocketfeed.models import PocketArticle


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),

    def handle(self, *args, **options):
        if settings.POCKET_CONSUMER_KEY and settings.POCKET_ACCESS_TOKEN:
            updated, deleted = PocketArticle.objects.refresh(count=8)

            if updated is None:
                raise CommandError('There was a problem updating the Pocket feed')

            if not options['quiet']:
                if updated:
                    print('Refreshed %s articles from Pocket' % updated)

                    if deleted:
                        print('Deleted %s old articles' % deleted)
                else:
                    print('Pocket feed is already up to date')
        else:
            print('Pocket API settings not found - skipping article refresh')
