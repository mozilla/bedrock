from __future__ import print_function

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bedrock.wordpress.models import BlogPost


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),
        parser.add_argument('--database', default='default',
                            help=('Specifies the database to use. '
                                  'Defaults to "default".')),

    def handle(self, *args, **options):
        errors = []
        for feed_id in settings.WP_BLOGS:
            updated = BlogPost.objects.refresh(feed_id, options['database'])
            if updated and not options['quiet']:
                print('Refreshed %s posts from the %s blog' % (updated, feed_id))

            if not updated:
                errors.append('Something has gone wrong with refreshing the %s blog' % feed_id)

        if errors:
            raise CommandError('\n'.join(errors))
