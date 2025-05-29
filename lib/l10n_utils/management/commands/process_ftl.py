# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import shutil
from subprocess import CalledProcessError

from django.conf import settings
from django.core.management.base import CommandError

from fluent.syntax.parser import FluentParser, ParseError

from lib.l10n_utils.fluent import fluent_l10n, get_metadata, write_metadata

from ._ftl_repo_base import FTLRepoCommand

GIT_COMMIT_EMAIL = "meao-bots+mozmarrobot@mozilla.com"
GIT_COMMIT_NAME = "MozMEAO Bot"


class NoisyFluentParser(FluentParser):
    """A parser that will raise exceptions.

    The one from fluent.syntax doesn't raise exceptions, but will
    return instances of fluent.syntax.ast.Junk instead.
    """

    def get_entry_or_junk(self, ps):
        """Allow the ParseError to bubble up"""
        entry = self.get_entry(ps)
        ps.expect_line_end()
        return entry


class Command(FTLRepoCommand):
    help = "Processes .ftl files from l10n team for use in bedrock"
    parser = None

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("--push", action="store_true", dest="push", default=False, help="Push the changes to the MEAO Fluent files repo.")
        parser.add_argument("--reset", action="store_true", dest="reset", default=False, help="Delete and recreate the activation metadata.")

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.parser = NoisyFluentParser()
        self.update_fluent_files()
        self.update_l10n_team_files()
        no_errors = self.copy_ftl_files()
        self.set_activation(reset=options["reset"])
        self.copy_configs()
        if options["push"]:
            changes = self.commit_changes()
            if changes:
                self.push_changes()

        if not no_errors:
            raise CommandError("Some errors were discovered in some .ftl files and they were not updated. See above for details.")

    def config_fluent_repo(self):
        """Set user config so that committing will work"""
        self.meao_repo.git("config", "user.email", GIT_COMMIT_EMAIL)
        self.meao_repo.git("config", "user.name", GIT_COMMIT_NAME)

    def commit_changes(self):
        self.config_fluent_repo()
        self.meao_repo.git("add", ".")
        try:
            self.meao_repo.git("commit", "-m", "Update files from l10n repo")
        except CalledProcessError:
            self.stdout.write("No changes to commit")
            return False

        self.stdout.write("Committed changes to local repo")
        return True

    def push_changes(self):
        try:
            self.meao_repo.git("push", self.git_push_url, "HEAD:master")
        except CalledProcessError:
            raise CommandError(f"There was a problem pushing to {self.meao_repo.remote_url}")

        commit = self.meao_repo.git("rev-parse", "--short", "HEAD")
        self.stdout.write(f"Pushed {commit} to {self.meao_repo.remote_url}")

    @property
    def git_push_url(self):
        if not settings.FLUENT_REPO_AUTH:
            raise CommandError("Git push authentication not configured")

        return self.meao_repo.remote_url_auth(settings.FLUENT_REPO_AUTH)

    def _copy_file(self, filepath):
        relative_filepath = filepath.relative_to(self.l10n_repo.path)
        to_filepath = self.meao_repo.path.joinpath(relative_filepath)
        to_filepath.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(filepath), str(to_filepath))
        self.stdout.write(".", ending="")
        self.stdout.flush()

    def copy_configs(self):
        count = 0
        for filepath in self.l10n_repo.path.rglob("*.toml"):
            self._copy_file(filepath)
            count += 1

        self.stdout.write(f"\nCopied {count} .toml files")

    def copy_ftl_files(self):
        count = 0
        errors = []
        for filepath in self.l10n_repo.path.rglob("*.ftl"):
            if not self.lint_ftl_file(filepath):
                errors.append(filepath.relative_to(self.l10n_repo.path))
                continue

            self._copy_file(filepath)
            count += 1

        self.stdout.write(f"\nCopied {count} .ftl files")
        if errors:
            self.stdout.write("The following files had parse errors and were not copied:")
            for fpath in errors:
                self.stdout.write(f"- {fpath}")
            return False

        return True

    def lint_ftl_file(self, filepath):
        with filepath.open() as ftl:
            try:
                self.parser.parse(ftl.read())
            except ParseError:
                return False

            return True

    def _get_all_ftl_file_names(self):
        paths = self.meao_repo.path.rglob("*.ftl")
        return [str(p.relative_to(self.meao_repo.path)) for p in paths]

    def set_activation(self, reset=False):
        updated_ftl = set()
        if reset:
            ftl_files = self._get_all_ftl_file_names()
            shutil.rmtree(self.meao_repo.path.joinpath("metadata"))
        else:
            ftl_files, _ = self.meao_repo.modified_files()

        for fname in ftl_files:
            if not fname.endswith(".ftl"):
                continue

            locale, ftl_name = fname.split("/", 1)
            updated_ftl.add(ftl_name)

        for ftl_name in updated_ftl:
            self.calculate_activation(ftl_name)

    def calculate_activation(self, ftl_file):
        translations = self.meao_repo.path.glob(f"*/{ftl_file}")
        metadata = get_metadata(ftl_file)
        active_locales = metadata.get("active_locales", [])
        inactive_locales = metadata.get("inactive_locales", [])
        percent_required = metadata.get("percent_required", settings.FLUENT_DEFAULT_PERCENT_REQUIRED)
        all_locales = {str(x.relative_to(self.meao_repo.path)).split("/", 1)[0] for x in translations}
        locales_to_check = all_locales.difference(["en"], active_locales, inactive_locales)
        new_activations = []
        for locale in locales_to_check:
            l10n = fluent_l10n([locale, "en"], [ftl_file])
            if not l10n.has_required_messages:
                continue

            percent_trans = l10n.percent_translated
            if percent_trans < percent_required:
                continue

            new_activations.append(locale)

        if new_activations:
            active_locales.extend(new_activations)
            metadata["active_locales"] = sorted(active_locales)
            write_metadata(ftl_file, metadata)
            self.stdout.write(f"Activated {len(new_activations)} new locales for {ftl_file}")
