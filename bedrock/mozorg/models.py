from builtins import str
from builtins import object
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.db.utils import DatabaseError
from django.dispatch import receiver

from picklefield import PickledObjectField
from django_extensions.db.fields import ModificationDateTimeField


CONTRIBUTOR_SOURCE_NAMES = {
    'all': None,
    'sumo': 'team',
    'reps': 'team',
    'qa': 'team',
    'firefox': 'team',
    'firefoxos': 'team',
    'firefoxforandroid': 'team',
    'bugzilla': 'source',
    'github': 'source',
}


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

    def __unicode__(self):
        return u'Tweets from @' + self.account


@receiver(post_save, sender=TwitterCache)
def twitter_cache_post_save(sender, **kwargs):
    instance = kwargs['instance']
    cache_tweets(instance.account, instance.tweets)


class ContributorActivityManager(models.Manager):
    def group_by_date_and_source(self, source):
        try:
            source_type = CONTRIBUTOR_SOURCE_NAMES[source]
        except KeyError:
            raise ContributorActivity.DoesNotExist

        qs = self.values('date')
        if source_type is not None:
            field_name = source_type + '_name'
            qs = qs.filter(**{field_name: source})

        # dates are grouped in weeks. 52 results gives us a year.
        return qs.annotate(models.Sum('total'), models.Sum('new'))[:52]


class ContributorActivity(models.Model):
    date = models.DateField()
    source_name = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)
    total = models.IntegerField()
    new = models.IntegerField()

    objects = ContributorActivityManager()

    class Meta(object):
        unique_together = ('date', 'source_name', 'team_name')
        get_latest_by = 'date'
        ordering = ['-date']
