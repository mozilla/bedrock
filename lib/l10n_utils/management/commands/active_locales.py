# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.management.base import BaseCommand

from lib.l10n_utils.fluent import get_active_locales


class Command(BaseCommand):
    help = 'Report the active locales for a .ftl file'
    _filename = None

    @property
    def filename(self):
        if self._filename is None:
            return ''

        return self._filename

    @filename.setter
    def filename(self, value):
        if not value.endswith('.ftl'):
            self._filename = f'{value}.ftl'
        else:
            self._filename = value

    def add_arguments(self, parser):
        parser.add_argument('ftl_file')

    def print_report(self):
        active_locales = get_active_locales(self.filename)
        num_locales = len(active_locales)
        if num_locales == 1:
            self.stdout.write(f'There is 1 active locale for {self.filename}:')
        else:
            self.stdout.write(f'There are {num_locales} active locales for {self.filename}:')

        for locale in active_locales:
            self.stdout.write(f'- {locale}')

    def handle(self, *args, **options):
        self.filename = options['ftl_file']
        self.print_report()
