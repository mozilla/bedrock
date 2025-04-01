# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from io import StringIO

from django.core.management.base import BaseCommand

from bedrock.sitemaps.models import SitemapURL
from bedrock.utils.management.decorators import alert_sentry_on_exception


@alert_sentry_on_exception
class Command(BaseCommand):
    help = "Updates sitemaps data in the database"

    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output.")

    def handle(self, *args, **options):
        if options["quiet"]:
            self.stdout._out = StringIO()

        SitemapURL.objects.refresh()
        self.stdout.write("Updated sitemaps data")
