from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.db.utils import DatabaseError
from django.dispatch import receiver

from picklefield import PickledObjectField
from django_extensions.db.fields import ModificationDateTimeField


def twitter_cache_key(account):
    return 'tweets-for-' + str(account)


def cache_tweets(account, tweets, timeout=6 * 60 * 60):
    cache.set(twitter_cache_key(account), tweets, timeout)


class TwitterCacheManager(models.Manager):
    def get_tweets_for(self, account):
        tweets = cache.get(twitter_cache_key(account))
        if tweets is None:
            try:
                tweets = self.get(account=account).tweets
            except (TwitterCache.DoesNotExist, DatabaseError):
                # TODO: see if we should catch other errors
                tweets = []
                cache_tweets(account, tweets, 10)  # try again in 10 seconds
            else:
                cache_tweets(account, tweets)
        return tweets


class TwitterCache(models.Model):
    account = models.CharField(max_length=100, db_index=True, unique=True)
    tweets = PickledObjectField(default=list)
    updated = ModificationDateTimeField()
    objects = TwitterCacheManager()

    def __str__(self):
        return u'Tweets from @' + self.account


@receiver(post_save, sender=TwitterCache)
def twitter_cache_post_save(sender, **kwargs):
    instance = kwargs['instance']
    cache_tweets(instance.account, instance.tweets)
