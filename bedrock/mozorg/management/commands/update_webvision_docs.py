# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.management.base import BaseCommand

from bedrock.mozorg.models import WebvisionDoc
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
        repo = GitRepo(settings.WEBVISION_DOCS_PATH, settings.WEBVISION_DOCS_REPO, branch_name=settings.WEBVISION_DOCS_BRANCH, name="Webvision Docs")
        self.output("Updating git repo")
        repo.update()
        if not (options["force"] or repo.has_changes()):
            self.output("No webvision docs updates")
            return

        self.output("Loading webvision docs into database")
        count, errors = WebvisionDoc.objects.refresh()
        self.output(f"{count} webvision docs successfully loaded")
        if errors:
            self.output(f"Encountered {errors} errors while loading docs")
        else:
            # Only `set_db_latest` if there are no errors so that it will try without errors again next time.
            repo.set_db_latest()
            self.output("Saved latest git repo state to database")

        self.output("Done!")
