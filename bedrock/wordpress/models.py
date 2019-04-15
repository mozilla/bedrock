# -*- coding: utf-8 -*-

import operator
import random

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.utils import DatabaseError
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, utc

import bleach
from django_extensions.db.fields.json import JSONField
from jinja2 import Markup
from raven.contrib.django.raven_compat.models import client as sentry_client

from bedrock.wordpress.api import get_posts_data, complete_posts_data
from functools import reduce


def make_datetime(datestr):
    return make_aware(parse_datetime(datestr), timezone=utc)


def strip_tags(text):
    return bleach.clean(text, tags=[], strip=True).strip()


def post_to_dict(blog_slug, post):
    try:
        return dict(
            wp_id=post['id'],
            wp_blog_slug=blog_slug,
            date=make_datetime(post['date_gmt']),
            modified=make_datetime(post['modified_gmt']),
            title=strip_tags(post['title']['rendered']),
            excerpt=process_excerpt(post['excerpt']['rendered']),
            link=post['link'],
            featured_media=post['featured_media'],
            tags=post['tags'],
        )
    except Exception:
        return None


def process_excerpt(excerpt):
    summary = strip_tags(excerpt)
    if summary.lower().endswith('continue reading'):
        summary = summary[:-16]

    if summary.lower().endswith('read more'):
        summary = summary[:-9]

    if summary.lower().endswith('[&hellip;]'):
        summary = summary[:-10] + '…'

    if summary.endswith('[…]'):
        summary = summary[:-3] + '…'

    return summary


class BlogPostQuerySet(models.QuerySet):
    def filter_by_blogs(self, *blog_slugs):
        return self.filter(wp_blog_slug__in=blog_slugs)

    def filter_by_tags(self, *tags):
        tag_qs = [Q(tags__contains='"{}"'.format(t)) for t in tags]
        return self.filter(reduce(operator.or_, tag_qs))


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def filter_by_blogs(self, *blog_slugs):
        return self.get_queryset().filter_by_blogs(*blog_slugs)

    def filter_by_tags(self, *tags):
        return self.get_queryset().filter_by_tags(*tags)

    def update_posts(self, blog_slug, posts):
        update_count = 0
        del_count = 0
        post_ids = []
        posts_to_update = []
        for post in posts:
            modified = make_datetime(post['modified_gmt'])
            post_ids.append(post['id'])
            try:
                obj = self.get(wp_id=post['id'], wp_blog_slug=blog_slug)
            except BlogPost.DoesNotExist:
                posts_to_update.append((None, post))
            else:
                if obj.modified != modified:
                    posts_to_update.append((obj, post))

        if not posts_to_update:
            return 0, 0

        complete_posts_data(blog_slug, posts_to_update)
        for obj, post in posts_to_update:
            post = post_to_dict(blog_slug, post)
            if not post:
                continue

            try:
                if obj:
                    for key, value in post.iteritems():
                        setattr(obj, key, value)
                    obj.save()
                else:
                    self.create(**post)
            except DatabaseError:
                sentry_client.captureException()
                raise

            update_count += 1

        # clean up after changes
        if update_count:
            expired_posts = self.filter_by_blogs(blog_slug).exclude(wp_id__in=post_ids)
            del_count = expired_posts.count()
            expired_posts.delete()

        return update_count, del_count

    def refresh(self, feed_id, num_posts=None):
        posts = get_posts_data(feed_id, num_posts)
        if posts:
            return self.update_posts(feed_id, posts)

        # no data returned. something wrong.
        return None, None


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
        return Markup(self.excerpt)

    @property
    def blog_title(self):
        return Markup(self.title).unescape()

    @property
    def blog_link(self):
        return settings.WP_BLOGS[self.wp_blog_slug]['url']

    @property
    def blog_name(self):
        return settings.WP_BLOGS[self.wp_blog_slug]['name']

    def get_featured_tag(self, tags):
        """Return a tag present both in the post and the passed in list.

        If no tag matches something odd has happened, so just return blank.
        """
        matching_tags = list(set(self.tags) & set(tags))
        if matching_tags:
            return random.choice(matching_tags)
        else:
            return ''

    def get_featured_image_url(self, size='large'):
        try:
            return self.featured_media['media_details']['sizes'][size]['source_url']
        except (KeyError, TypeError):
            return None
