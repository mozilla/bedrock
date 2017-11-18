from __future__ import print_function

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bedrock.wordpress.models import BlogPost


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),

    def handle(self, *args, **options):
        errors = []
        for feed_id in settings.WP_BLOGS:
            updated, deleted = BlogPost.objects.refresh(feed_id)
            if updated is None:
                errors.append('There was a problem updating the %s blog' % feed_id)
                continue

            if not options['quiet']:
                if updated:
                    print('Refreshed %s posts from the %s blog' % (updated, feed_id))
                    if deleted:
                        print('Deleted %s old posts from the %s blog' % (deleted, feed_id))
                else:
                    print('The %s blog is already up to date' % feed_id)

        if errors:
            raise CommandError('\n'.join(errors))
