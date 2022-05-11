# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from io import StringIO

from django.conf import settings
from django.core.management.base import BaseCommand

from bedrock.utils.git import GitRepo


class Command(BaseCommand):
    help = "Clones or updates l10n info from github"

    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output."),
        parser.add_argument(
            "-c", "--clean", action="store_true", dest="clean", default=False, help="Remove old repos if they exist and do fresh clones."
        ),

    def handle(self, *args, **options):
        if options["quiet"]:
            self.stdout._out = StringIO()

        self.update_fluent_files(options["clean"])

    def update_fluent_files(self, clean=False):
        for site, params in settings.FLUENT_L10N_UPDATE_PARAMS.items():
            repo = GitRepo(**params)
            if clean:
                repo.reclone()
            else:
                repo.update()

            repo.update()
            self.stdout.write(f"Updated .ftl files for {site}")
