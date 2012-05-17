import cronjobs
import feedparser
from django.conf import settings
from django.core.cache import cache

@cronjobs.register
def update_feeds():
    for name, url in settings.FEEDS.items():
        feed_info = feedparser.parse(url)
        cache.set('feeds-%s' % name, feed_info)
