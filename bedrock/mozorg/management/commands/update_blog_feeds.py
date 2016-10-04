from __future__ import print_function

from django.core.management.base import BaseCommand

from bedrock.mozorg.models import BlogArticle


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),
        parser.add_argument('--database', default='default',
                            help=('Specifies the database to use, if using a db. '
                                  'Defaults to "default".')),
        parser.add_argument('--articles', default=5, type=int,
                            help='Number of articles to store from each feed. Defaults to 5.')

    def handle(self, *args, **options):
        BlogArticle.update_feeds(options['database'], options['articles'])
