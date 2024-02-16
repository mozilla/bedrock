# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from io import StringIO

from django.conf import settings
from django.core.management.base import BaseCommand

from bedrock.utils.git import GitRepo

ROOT_FILES = settings.ROOT_PATH / "root_files"


class Command(BaseCommand):
    help = "Clones or updates sitemaps info from github"

    def add_arguments(self, parser):
        parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False, help="If no error occurs, swallow all output.")

    def handle(self, *args, **options):
        if options["quiet"]:
            self.stdout._out = StringIO()

        data_path = settings.SITEMAPS_PATH.joinpath("data")
        repo = GitRepo(settings.SITEMAPS_PATH, settings.SITEMAPS_REPO, settings.SITEMAPS_REPO_BRANCH)
        repo.update()

        for src_path in data_path.rglob("*.*"):
            rel_path = src_path.relative_to(data_path)
            if rel_path.parts[0] == "sitemaps":
                rel_path = rel_path.relative_to("sitemaps")
            target_path = ROOT_FILES.joinpath(rel_path)
            if target_path.exists():
                if target_path.is_symlink():
                    continue
                else:
                    target_path.unlink()

            target_path.parent.mkdir(exist_ok=True)
            target_path.symlink_to(src_path)

        self.stdout.write("Updated sitemaps files")
