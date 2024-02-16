# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.management.base import BaseCommand, CommandError

import basket

from bedrock.newsletter.models import Newsletter
from bedrock.utils.management.decorators import alert_sentry_on_exception


@alert_sentry_on_exception
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output.")

    def handle(self, *args, **options):
        newsletters = basket.get_newsletters()
        if not newsletters:
            raise CommandError("No data from basket")

        count = Newsletter.objects.refresh(newsletters)
        if not options["quiet"]:
            if count:
                print(f"Updated {count} newsletters")
            else:
                print("Nothing to update")
