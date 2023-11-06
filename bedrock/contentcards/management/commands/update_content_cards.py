# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.management.base import BaseCommand

from bedrock.contentcards.models import ContentCard
from bedrock.utils.git import GitRepo
from bedrock.utils.management.decorators import alert_sentry_on_exception


@alert_sentry_on_exception
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output.")
        parser.add_argument("-f", "--force", action="store_true", dest="force", default=False, help="Load the data even if nothing new from git.")

    def output(self, msg):
        if not self.quiet:
            print(msg)

    def handle(self, *args, **options):
        self.quiet = options["quiet"]
        repo = GitRepo(settings.CONTENT_CARDS_PATH, settings.CONTENT_CARDS_REPO, branch_name=settings.CONTENT_CARDS_BRANCH, name="Content Cards")
        self.output("Updating git repo")
        repo.update()
        if not (options["force"] or repo.has_changes()):
            self.output("No content card updates")
            return

        self.output("Loading content cards into database")
        count = ContentCard.objects.refresh()

        self.output(f"{count} content cards successfully loaded")

        repo.set_db_latest()

        self.output("Saved latest git repo state to database")
        self.output("Done!")
