# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Remove porting process artifacts like hash comments'
    _filenames = None
    base_path = settings.FLUENT_LOCAL_PATH

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='*',
                            help='File(s) to clean.')
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),

    @property
    def filenames(self):
        return self._filenames

    @filenames.setter
    def filenames(self, value):
        if value:
            self._filenames = [f'{f}.ftl' if not f.endswith('.ftl') else f for f in value]

    def clean_file(self, filename):
        file_path = Path(filename)
        if not file_path.exists():
            # might be just a ftl name
            file_path = self.base_path.joinpath('en', file_path)
            if not file_path.exists():
                self.stderr.write(f'Can not find {filename}')
                return

        with file_path.open() as fpr:
            lines = [l for l in fpr.readlines() if not l.startswith('# LANG_ID_HASH:')]

        with file_path.open('w') as fpw:
            fpw.writelines(lines)

        self.stdout.write(f'Cleaned {filename}')

    def handle(self, *args, **options):
        self.filenames = options['filename']
        if options['quiet']:
            self.stdout._out = StringIO()

        if not self.filenames:
            raise CommandError('At least one filename is required')

        for filename in self.filenames:
            self.clean_file(filename)
