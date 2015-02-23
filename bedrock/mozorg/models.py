from django.core.cache import cache
from django.db import models
from django.db.utils import DatabaseError

from picklefield import PickledObjectField
from django_extensions.db.fields import ModificationDateTimeField


class TwitterCacheManager(models.Manager):
    def get_tweets_for(self, account):
        cache_key = 'tweets-for-' + str(account)
        tweets = cache.get(cache_key)
        if tweets is None:
            try:
                tweets = self.get(account=account).tweets
            except (TwitterCache.DoesNotExist, DatabaseError):
                # TODO: see if we should catch other errors
                tweets = []

            cache.set(cache_key, tweets, 60 * 60 * 6)  # 6 hours, same as cron

        return tweets


class TwitterCache(models.Model):
    account = models.CharField(max_length=100, db_index=True, unique=True)
    tweets = PickledObjectField(default=list)
    updated = ModificationDateTimeField()

    objects = TwitterCacheManager()

    def __unicode__(self):
        return u'Tweets from @' + self.account
