# coding=utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import logging

from django.conf import settings

import requests

from bedrock.events.models import Event
from bedrock.utils.management.cron_command import CronCommand

logger = logging.getLogger(__name__)


class Command(CronCommand):
    lock_key = 'ical-feeds'

    def handle_safe(*args, **options):
        # TODO get dependencies for TLS SNI installed on servers
        # see http://bugzil.la/1080571

        # if the ical feed is down catch the exception, log the error
        # and fail silently.
        # http://bugzil.la/1129961
        for feed_url in settings.EVENTS_ICAL_FEEDS:
            logger.info('Syncing ical feed: %s' % feed_url)
            try:
                resp = requests.get(feed_url, verify=False)
                if resp.status_code == 200:
                    Event.objects.sync_with_ical(resp.text, feed_url)
                else:
                    logger.error(
                        "Request returned error code: %d and error body: %s" %
                        (resp.status_code, resp.text))
            except Exception:
                logger.exception('Error parsing ical feed: ' + feed_url)

        # delete old events
        Event.objects.past().delete()
