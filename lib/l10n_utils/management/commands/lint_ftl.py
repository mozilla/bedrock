# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.functional import cached_property

from fluent.syntax.parser import FluentParser, ParseError


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
    help = 'Check .ftl files for errors'
    _filenames = None
    parser = None
    base_path = None

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='*',
                            help='Optional: Specific files to check. Finds files in a directory if none given.')
        parser.add_argument('-d', '--dir', dest='directory',
                            help='The directory to check (optional: overrides --repo)')
        parser.add_argument('-r', '--repo', action='store_const', dest='repo',
                            const=settings.FLUENT_REPO_PATH, default=settings.FLUENT_LOCAL_PATH,
                            help='Check files in the external Fluent Repo instead of the bedrock files.')
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),

    def handle(self, *args, **options):
        self.parser = NoisyFluentParser()
        self.filenames = options['filename']
        if options['directory']:
            self.base_path = Path(options['directory']).resolve()
        else:
            self.base_path = options['repo']

        if options['quiet']:
            self.stdout._out = StringIO()

        if not self.filenames:
            self.stdout.write(f'Checking {self.base_path}')

        count, errors = self.lint()
        self.stdout.write(f'\nChecked {count} .ftl file(s)')
        if errors:
            msgs = [f'Found {len(errors)} error(s)']
            for path, msg in errors:
                relative_path = path.relative_to(self.base_path)
                msgs.append(f'- {relative_path}: {msg}')

            raise CommandError('\n'.join(msgs))

    @property
    def filenames(self):
        return self._filenames

    @filenames.setter
    def filenames(self, value):
        if value:
            self._filenames = [f'{f}.ftl' if not f.endswith('.ftl') else f for f in value]

    @property
    def all_file_paths(self):
        if not self.base_path.is_dir():
            raise CommandError(f'Requested directory does not exist: {self.base_path}')

        return self.base_path.rglob('*.ftl')

    @cached_property
    def file_paths(self):
        if self.filenames:
            return [self.base_path.joinpath(f) for f in self.filenames]
        else:
            return self.all_file_paths

    def lint(self):
        count = 0
        errors = []
        for path in self.file_paths:
            with path.open() as ftl:
                try:
                    self.parser.parse(ftl.read())
                    self.stdout.write('.', ending='')
                except ParseError as e:
                    self.stdout.write('x', ending='')
                    errors.append((path, e.message))

                self.stdout.flush()
                count += 1

        return count, errors
