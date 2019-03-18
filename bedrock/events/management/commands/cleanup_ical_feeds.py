# coding=utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import logging

from bedrock.events.models import Event
from bedrock.utils.management.cron_command import CronCommand

logger = logging.getLogger(__name__)


class Command(CronCommand):
    help = 'Delete old events'
    lock_key = 'cleanup-ical-feeds'

    def handle_safe(*args, **options):
        Event.objects.past().delete()
