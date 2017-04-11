from __future__ import print_function, unicode_literals

import operator
from django.conf import settings
from django.db import models, transaction
from django.db.models import Q
from django.db.utils import DatabaseError
from django.utils.html import strip_tags

import bleach
from django_extensions.db.fields.json import JSONField
from jinja2 import Markup
from raven.contrib.django.raven_compat.models import client as sentry_client

from bedrock.wordpress.api import get_posts_data


class BlogPostQuerySet(models.QuerySet):
    def filter_by_blog(self, blog_slug):
        return self.filter(wp_blog_slug=blog_slug)

    def filter_by_tags(self, *tags):
        tag_qs = [Q(tags__contains='"{}"'.format(t)) for t in tags]
        return self.filter(reduce(operator.or_, tag_qs))


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def filter_by_blog(self, blog_slug):
        return self.get_queryset().filter_by_blog(blog_slug)

    def filter_by_tags(self, *tags):
        return self.get_queryset().filter_by_tags(*tags)

    def update_posts(self, data, database='default'):
        with transaction.atomic(using=database):
            count = 0
            posts = data['posts']
            self.filter_by_blog(data['wp_blog_slug']).delete()
            for post in posts:
                try:
                    self.create(
                        wp_id=post['id'],
                        wp_blog_slug=data['wp_blog_slug'],
                        date=post['date_gmt'],
                        modified=post['modified_gmt'],
                        title=bleach.clean(post['title']['rendered']),
                        excerpt=bleach.clean(post['excerpt']['rendered']),
                        link=post['link'],
                        featured_media=post['featured_media'],
                        tags=post['tags'],
                    )
                    count += 1
                except (DatabaseError, KeyError):
                    sentry_client.captureException()
                    raise

            return count

    def refresh(self, feed_id, database='default', num_posts=None):
        data = get_posts_data(feed_id, num_posts)
        if data:
            return self.update_posts(data, database)

        # no data returned. something wrong.
        return 0


class BlogPost(models.Model):
    wp_id = models.IntegerField()
    wp_blog_slug = models.CharField(max_length=50)
    date = models.DateTimeField()
    modified = models.DateTimeField()
    title = models.CharField(max_length=255)
    excerpt = models.TextField()
    link = models.URLField()
    featured_media = JSONField()
    tags = JSONField()

    objects = BlogPostManager()

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']

    def __unicode__(self):
        return '%s: %s' % (self.blog_name, self.title)

    def get_absolute_url(self):
        return self.link

    def htmlify(self):
        summary = strip_tags(self.excerpt).strip()
        if summary.lower().endswith('continue reading'):
            summary = summary[:-16]

        return Markup(summary)

    @property
    def blog_title(self):
        title = strip_tags(self.title).strip()
        return Markup(title).unescape()

    @property
    def blog_link(self):
        return settings.WP_BLOGS[self.wp_blog_slug]['url']

    @property
    def blog_name(self):
        return settings.WP_BLOGS[self.wp_blog_slug]['name']

    def get_featured_image_url(self, size='large'):
        try:
            return self.featured_media['media_details']['sizes'][size]['source_url']
        except KeyError:
            return None
