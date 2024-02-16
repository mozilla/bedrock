# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.db import models
from django.db.utils import DatabaseError

from markupsafe import Markup
from sentry_sdk import capture_exception

from bedrock.pocketfeed.api import complete_articles_data, get_articles_data


class PocketArticleManager(models.Manager):
    # called by cron job
    def refresh(self, count=None):
        # request data from the API
        articles = get_articles_data(count=count)

        if articles and len(articles["recommendations"]) > 0:
            # if API gave us data, insert/update new data
            # returns tuple: number updated, number deleted
            return self.update_articles(articles["recommendations"])

        # no data returned. something wrong.
        return None, None

    # returns a tuple: updated article count, deleted article count
    def update_articles(self, articles):
        update_count = 0
        del_count = 0
        article_ids = []
        articles_to_update = []
        for article in articles:
            # apparently it's possible for an article to be
            # in the feed multiple times ¯\_(ツ)_/¯
            if article["id"] in article_ids:
                continue

            article_ids.append(article["id"])

            try:
                # look for an object in the db with the article's id
                obj = self.get(pocket_id=article["id"])
            except PocketArticle.DoesNotExist:
                # this article from Pocket will be added to the db
                articles_to_update.append((None, article))
            except PocketArticle.MultipleObjectsReturned:
                # multiple articles with the same ID snuck in. Fix that here.
                self.filter(pocket_id=article["id"]).delete()
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
                    if obj.time_shared != article["time_shared"]:
                        for key, value in article.items():
                            setattr(obj, key, value)
                        obj.save()
                        update_count += 1
                else:
                    self.create(**article)
                    update_count += 1
            except DatabaseError:
                capture_exception()
                raise

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
    image_src = models.URLField(null=True)  # points to Pocket's image CDN  # noqa: DJ001
    time_shared = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    objects = PocketArticleManager()

    class Meta:
        get_latest_by = "time_shared"
        ordering = ["-time_shared"]

    def __str__(self):
        return self.title

    @property
    def display_title(self):
        return Markup(self.title).unescape()
