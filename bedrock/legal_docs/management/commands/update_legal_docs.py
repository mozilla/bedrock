# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.management.base import BaseCommand

import requests

from bedrock.legal_docs.models import LegalDoc
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

    def snitch(self):
        if settings.LEGAL_DOCS_DMS_URL:
            requests.get(settings.LEGAL_DOCS_DMS_URL)

    def handle(self, *args, **options):
        self.quiet = options["quiet"]
        repo = GitRepo(settings.LEGAL_DOCS_PATH, settings.LEGAL_DOCS_REPO, branch_name=settings.LEGAL_DOCS_BRANCH, name="Legal Docs")
        self.output("Updating git repo")
        repo.update()
        if not (options["force"] or repo.has_changes()):
            self.output("No legal docs updates")
            self.snitch()
            return

        self.output("Loading legal docs into database")
        count, errors = LegalDoc.objects.refresh()
        self.output(f"{count} legal docs successfully loaded")
        if errors:
            self.output(f"Encountered {errors} errors while loading docs")
        else:
            # only set latest if there are no errors so that it will try the errors again next time
            # also so that it will fail again and thus not ping the snitch so that we'll be notified
            repo.set_db_latest()
            self.output("Saved latest git repo state to database")
            self.snitch()

        self.output("Done!")
