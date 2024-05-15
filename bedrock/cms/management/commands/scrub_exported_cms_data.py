# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand

from wagtail.models import Revision
from wagtail_localize.models import TranslationSource

from bedrock.utils.management.decorators import alert_sentry_on_exception


@alert_sentry_on_exception
class Command(BaseCommand):
    """Purge Wagtail-managed data that we don't need in the published site
    which may be either confusing, outdated or too early to publicly share (as a draft)
    """

    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output.")

    def output(self, *args):
        if not self.quiet:
            print(*args)

    def handle(self, *args, **options):
        self.quiet = options["quiet"]

        user_results = User.objects.all().delete()
        self.output("Deleted Users:", user_results)

        session_results = Session.objects.all().delete()
        self.output("Deleted Sessions:", session_results)

        # Delete all Revisions so that the exported DB doesn't contain
        # pre-publishing versions, stale versions or interim draft versions of
        # data that may be not yet ready for the public, or now incorrect
        revisions_result = Revision.objects.all().delete()
        self.output("Deleted non-live Revisions:", revisions_result)

        # Delete all TranslationSources, as these are not needed for a published page
        # and may contain sensitive or inaccurate draft or stale data.
        translationsource_result = TranslationSource.objects.all().delete()
        self.output("Deleted TranslationSources:", translationsource_result)
