# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.management.base import BaseCommand

from bedrock.products.models import Breach
from bedrock.utils.management.decorators import alert_sentry_on_exception


@alert_sentry_on_exception
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output."),

    def output(self, msg):
        if not self.quiet:
            print(msg)

    def handle(self, *args, **options):
        self.quiet = options["quiet"]

        added, updated = Breach.objects.sync_db()
        self.output(f"Breaches added: {added}")
        self.output(f"Breaches updated: {updated}")

        Breach.objects.sync_logos(verbose=not self.quiet)
