# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bedrock.pocketfeed.models import PocketArticle
from bedrock.utils.management.decorators import alert_sentry_on_exception


@alert_sentry_on_exception
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output.")

    def handle(self, *args, **options):
        if settings.POCKET_CONSUMER_KEY and settings.POCKET_ACCESS_TOKEN:
            updated, deleted = PocketArticle.objects.refresh(count=8)

            if updated is None:
                raise CommandError("There was a problem updating the Pocket feed")

            if not options["quiet"]:
                if updated:
                    print(f"Refreshed {updated} articles from Pocket")

                    if deleted:
                        print(f"Deleted {deleted} old articles")
                else:
                    print("Pocket feed is already up to date")
        else:
            print("Pocket API settings not found - skipping article refresh")
