from __future__ import print_function

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import DatabaseError
from django.db import transaction

from feedparser import parse

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
        for feed_id, feed_options in settings.BLOG_FEEDS.items():
            feed_url = feed_options.get('feed_url', None)
            if feed_url is None:
                feed_url = '%s/feed/atom/' % feed_options['url'].rstrip('/')
            feed = parse(feed_url)
            if feed.entries:
                with transaction.atomic(using=options['database']):
                    count = 0
                    BlogArticle.objects.filter(blog_slug=feed_id).delete()
                    for article in feed.entries:
                        try:
                            BlogArticle.objects.create(
                                blog_slug=feed_id,
                                blog_name=feed_options['name'],
                                published=article.published,
                                updated=article.updated,
                                title=article.title,
                                summary=article.summary,
                                link=article.link,
                            )
                        except DatabaseError:
                            continue
                        count += 1
                        if count >= options['articles']:
                            break
