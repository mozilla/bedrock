# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings

from bedrock.mozorg.models import TwitterCache
from bedrock.mozorg.util import get_tweets
from bedrock.utils.management.cron_command import CronCommand


class Command(CronCommand):
    lock_key = 'update-tweets'

    def handle_safe(self, *args, **options):
        if not settings.TWITTER_APP_KEYS['consumer_key']:
            # twitter auth not configured
            return

        for account in settings.TWITTER_ACCOUNTS:
            tweets = get_tweets(account)

            if tweets:
                account_cache, created = TwitterCache.objects.get_or_create(
                    account=account, defaults={'tweets': tweets})
                if not created:
                    account_cache.tweets = tweets
                    account_cache.save()
