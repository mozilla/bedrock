# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bedrock.utils.management.decorators import alert_sentry_on_exception
from bedrock.wordpress.models import BlogPost


@alert_sentry_on_exception
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output."),

    def handle(self, *args, **options):
        errors = []
        for feed_id in settings.WP_BLOGS:
            updated, deleted = BlogPost.objects.refresh(feed_id)
            if updated is None:
                errors.append(f"There was a problem updating the {feed_id} blog")
                continue

            if not options["quiet"]:
                if updated:
                    print(f"Refreshed {updated} posts from the {feed_id} blog")
                    if deleted:
                        print(f"Deleted {deleted} old posts from the {feed_id} blog")
                else:
                    print(f"The {feed_id} blog is already up to date")

        if errors:
            raise CommandError("\n".join(errors))
