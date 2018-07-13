# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from django.contrib.staticfiles.storage import staticfiles_storage
from django.db import models
from django.db.utils import DatabaseError

from jinja2 import Markup
from raven.contrib.django.raven_compat.models import client as sentry_client

from bedrock.pocketfeed.api import get_articles_data, complete_articles_data


class PocketArticleManager(models.Manager):
    # called by cron job
    def refresh(self, count=None):
        # request data from the API
        articles = get_articles_data(count=count)

        if articles and len(articles['recommendations']) > 0:
            # if API gave us data, insert/update new data
            # returns tuple: number updated, number deleted
            return self.update_articles(articles['recommendations'])

        # no data returned. something wrong.
        return None, None

    # returns a tuple: updated article count, deleted article count
    def update_articles(self, articles):
        update_count = 0
        del_count = 0
        article_ids = []
        articles_to_update = []
        for article in articles:
            article_ids.append(article['id'])

            try:
                # look for an object in the db with the article's id
                obj = self.get(pocket_id=article['id'])
            except PocketArticle.DoesNotExist:
                # this article from Pocket will be added to the db
                articles_to_update.append((None, article))
            else:
                # this existing 'obj' will be updated in the db with
                # (potentially) new info contained in 'article'
                articles_to_update.append((obj, article))

        # converts 'id' key to 'pocket_id' and converts 'time_shared' from
        # unix timestamp to datetime
        complete_articles_data(articles_to_update)

        for obj, article in articles_to_update:
            try:
                if obj:
                    for key, value in article.iteritems():
                        setattr(obj, key, value)
                    obj.save()
                else:
                    self.create(**article)
            except DatabaseError:
                sentry_client.captureException()
                raise

            update_count += 1

        # clean up after changes
        if update_count:
            expired_articles = self.exclude(pocket_id__in=article_ids)
            del_count = expired_articles.count()
            expired_articles.delete()

        return update_count, del_count


class PocketArticle(models.Model):
    pocket_id = models.IntegerField()
    url = models.URLField()
    domain = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image_src = models.URLField(null=True)  # points to Pocket's image CDN
    time_shared = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    objects = PocketArticleManager()

    class Meta:
        get_latest_by = 'time_shared'
        ordering = ['-time_shared']

    def __unicode__(self):
        return self.title

    @staticmethod
    def fallback_image():
        return staticfiles_storage.url('img/pocket/pocket-feed-default.png')

    @property
    def display_title(self):
        return Markup(self.title).unescape()

    @property
    def image(self):
        return self.image_src or self.fallback_image()
