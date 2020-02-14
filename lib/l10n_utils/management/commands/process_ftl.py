# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import shutil
from io import StringIO

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from fluent.syntax.parser import FluentParser, ParseError

from bedrock.utils.git import GitRepo
from lib.l10n_utils.fluent import fluent_l10n, get_metadata, write_metadata


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


class Command(BaseCommand):
    help = 'Processes .ftl files from l10n team for use in bedrock'
    meao_repo = None
    l10n_repo = None
    parser = None

    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),

    def handle(self, *args, **options):
        if options['quiet']:
            self.stdout._out = StringIO()

        self.parser = NoisyFluentParser()
        self.l10n_repo = GitRepo(settings.FLUENT_L10N_TEAM_REPO_PATH, settings.FLUENT_L10N_TEAM_REPO)
        self.meao_repo = GitRepo(settings.FLUENT_REPO_PATH, settings.FLUENT_REPO)
        self.update_fluent_files()
        self.update_l10n_team_files()
        no_errors = self.copy_ftl_files()
        self.set_activation()
        if no_errors:
            self.stdout.write('There were no errors found in the .ftl files.')
        else:
            raise CommandError('Some errors were discovered in some .ftl files and they were not updated.'
                               'See above for details.')

    def update_l10n_team_files(self):
        try:
            # this will fail on first run
            self.l10n_repo.clean()
        except FileNotFoundError:
            pass
        self.l10n_repo.update()
        self.stdout.write('Updated l10n team .ftl files')

    def update_fluent_files(self):
        try:
            self.meao_repo.clean()
        except FileNotFoundError:
            pass
        self.meao_repo.update()
        self.stdout.write('Updated .ftl files')

    def copy_ftl_files(self):
        count = 0
        errors = []
        for filepath in self.l10n_repo.path.rglob('*.ftl'):
            relative_filepath = filepath.relative_to(self.l10n_repo.path)
            if not self.lint_ftl_file(filepath):
                errors.append(relative_filepath)
                continue

            to_filepath = self.meao_repo.path.joinpath(relative_filepath)
            to_filepath.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(filepath), str(to_filepath))
            count += 1
            self.stdout.write('.', ending='')
            self.stdout.flush()

        self.stdout.write(f'\nCopied {count} .ftl files')
        if errors:
            self.stdout.write('The following files had parse errors and were not copied:')
            for fpath in errors:
                self.stdout.write(f'- {fpath}')
            return False

        return True

    def lint_ftl_file(self, filepath):
        with filepath.open() as ftl:
            try:
                self.parser.parse(ftl.read())
            except ParseError:
                return False

            return True

    def set_activation(self):
        updated_ftl = set()
        modified, _ = self.meao_repo.modified_files()
        for fname in modified:
            locale, ftl_name = fname.split('/', 1)
            updated_ftl.add(ftl_name)

        for ftl_name in updated_ftl:
            self.calculate_activation(ftl_name)

    def calculate_activation(self, ftl_file):
        translations = self.meao_repo.path.glob(f'*/{ftl_file}')
        metadata = get_metadata(ftl_file)
        active_locales = metadata.get('active_locales', [])
        inactive_locales = metadata.get('inactive_locales', [])
        percent_required = metadata.get('percent_required', settings.FLUENT_DEFAULT_PERCENT_REQUIRED)
        all_locales = {str(x.relative_to(self.meao_repo.path)).split('/', 1)[0] for x in translations}
        locales_to_check = all_locales.difference(['en'], active_locales, inactive_locales)
        new_activations = []
        for locale in locales_to_check:
            l10n = fluent_l10n([locale, 'en'], [ftl_file])
            if not l10n.has_required_messages:
                continue

            percent_trans = l10n.percent_translated
            if percent_trans < percent_required:
                continue

            new_activations.append(locale)

        if new_activations:
            active_locales.extend(new_activations)
            metadata['active_locales'] = active_locales
            write_metadata(ftl_file, metadata)
            self.stdout.write(f'Activated {len(new_activations)} new locales for {ftl_file}')
