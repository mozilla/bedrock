# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import codecs
import logging

from django.conf import settings
from django.core.cache import cache

import cronjobs
import feedparser
import requests

from bedrock.mozorg.credits import get_credits_last_modified
from bedrock.mozorg.models import TwitterCache
from bedrock.mozorg.util import TwitterAPI


log = logging.getLogger(__name__)


@cronjobs.register
def update_feeds():
    for name, url in settings.FEEDS.items():
        feed_info = feedparser.parse(url)
        # Cache for a year (it will be set by the cron job no matter
        # what on a set interval)
        cache.set('feeds-%s' % name, feed_info, 60 * 60 * 24 * 365)


@cronjobs.register
def update_tweets():
    for account in settings.TWITTER_ACCOUNTS:
        try:
            tweets = TwitterAPI(account).user_timeline(screen_name=account)
        except Exception:
            tweets = None

        if tweets:
            account_cache, created = TwitterCache.objects.get_or_create(
                account=account, defaults={'tweets': tweets})
            if not created:
                account_cache.tweets = tweets
                account_cache.save()


@cronjobs.register
def update_credits(force=False):
    log.info('Updating Credits.')
    filename = settings.CREDITS_NAMES_FILE
    headers = {}
    if not force:
        last_updated = get_credits_last_modified()
        if last_updated:
            headers['if-modified-since'] = last_updated

    try:
        resp = requests.get(settings.CREDITS_NAMES_URL, headers=headers, verify=True)
    except requests.RequestException:
        log.exception('Unknown error connecting to %s' % settings.CREDITS_NAMES_URL)
        return

    if resp.status_code == 304:
        log.info('Credits already up-to-date.')

    elif resp.status_code == 200:
        with codecs.open(filename, 'wb', 'utf8') as credits_fh:
            credits_fh.write(resp.text)

        with open(settings.CREDITS_NAMES_UPDATED_FILE, 'wb') as lu_fh:
            lu_fh.write(resp.headers['last-modified'])

        log.info('Successfully update Credits.')

    else:
        log.error('Unknown error occurred updating Credits (%s): %s' % (resp.status_code,
                                                                        resp.text))
