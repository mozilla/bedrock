# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import sys

from django.core.management import call_command
from django.core.management.base import BaseCommand

import requests
from sentry_sdk import capture_exception

from bedrock.base.config_manager import config


class Command(BaseCommand):
    help = """Wraps the sync_smartling management command from
    wagtail-localize-smartling so that we can monitor its
    operation via a Dead Man's Snitch"""

    def handle(self, *args, **kwargs):
        SMARTLING_SYNC_SNITCH_URL = config("SMARTLING_SYNC_SNITCH_URL", default="")

        try:
            call_command("sync_smartling")

            sys.stdout.write(
                "\nsync_smartling executed successfully\n",
            )
            if SMARTLING_SYNC_SNITCH_URL:
                requests.get(SMARTLING_SYNC_SNITCH_URL)
                sys.stdout.write("Snitch pinged\n")
        except Exception as ex:
            sys.stderr.write(f"\nsync_smartling did not execute successfully: {ex}\n")
            capture_exception(ex)
