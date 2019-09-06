# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
from io import StringIO
from hashlib import md5
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.test import override_settings
from django.utils.functional import cached_property

from lib.l10n_utils.dotlang import parse as parse_lang, convert_variables, get_translations_for_langfile
from lib.l10n_utils.fluent import get_metadata_file_path
from lib.l10n_utils.utils import get_ftl_file_data


def format_ftl_string(ftl_id, string, comment):
    output = f'# {comment}\n' if comment else ''
    return output + f'{ftl_id} = {string}\n\n'


class Command(BaseCommand):
    help = 'Convert existing transations in .lang files to .ftl files'
    _filename = None
    force = False

    def add_arguments(self, parser):
        parser.add_argument('filename')
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),
        parser.add_argument('-f', '--force', action='store_true', dest='force', default=False,
                            help='Overwrite the FTL file if it exists.'),

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

    @property
    def file_path(self):
        return settings.FLUENT_LOCAL_PATH.joinpath('en', self.filename)

    @property
    def metadata_path(self):
        return get_metadata_file_path(self.filename)

    @property
    def metadata(self):
        try:
            with self.metadata_path.open() as mdf:
                return json.load(mdf)
        except (IOError, ValueError):
            return {}

    def write_metadata(self, data):
        if not self.metadata_path.exists():
            self.metadata_path.parent.mkdir(parents=True, exist_ok=True)

        with self.metadata_path.open('w') as mdf:
            json.dump(data, mdf, indent=2, sort_keys=True)

    @property
    def lang_file_path(self):
        return Path(self.filename).with_suffix('.lang')

    @cached_property
    def ftl_file_data(self):
        return get_ftl_file_data(self.filename)

    def get_ftl_id(self, str_id):
        data = self.ftl_file_data
        hashed_id = md5(str_id.encode()).hexdigest()
        return data.get(hashed_id)

    def translated_filepaths(self):
        for path in settings.LOCALES_PATH.glob(f'*/{self.lang_file_path}'):
            lang = path.relative_to(settings.LOCALES_PATH).parts[0]
            if lang not in ['en-US', 'templates']:
                yield path

    def get_translation(self, path):
        return parse_lang(path, skip_untranslated=True, extract_comments=True)

    def write_ftl_file(self, path, data):
        ftl_path = path.relative_to(settings.LOCALES_PATH).with_suffix('.ftl')
        ftl_path = settings.FLUENT_REPO_PATH.joinpath(ftl_path)
        if ftl_path.exists() and not self.force:
            return False

        ftl_path.parent.mkdir(parents=True, exist_ok=True)
        with ftl_path.open('w') as ftlf:
            for ftl_id, ftl_info in data.items():
                ftlf.write(format_ftl_string(ftl_id, **ftl_info))

        return True

    def write_ftl_translations(self):
        wrote_all = True
        for path in self.translated_filepaths():
            translation = self.get_translation(path)
            all_strings = {}
            for str_id, string in translation.items():
                comment, string = string
                if comment and comment.startswith('TAG:'):
                    # ignore tag comments
                    comment = None
                ftl_id = self.get_ftl_id(str_id)
                if ftl_id:
                    all_strings[ftl_id] = {
                        'string': convert_variables(string),
                        'comment': comment,
                    }
                else:
                    relative_path = path.relative_to(settings.LOCALES_PATH)
                    self.stderr.write(f'WARNING: Could not find a match for "{str_id}"\n'
                                      f'in {relative_path}')

            wrote = self.write_ftl_file(path, all_strings)
            if not wrote:
                wrote_all = False

            self.stdout.write('.' if wrote else 'x', ending='')
            self.stdout.flush()

        self.stdout.write('')  # carriage return
        if not wrote_all:
            self.stdout.write('Did not modify existing files. Use --force to overwrite.')

    @override_settings(DEV=False)
    def record_active_translations(self):
        translations = get_translations_for_langfile(self.lang_file_path.with_suffix(''))
        data = self.metadata
        data['active_locales'] = translations
        self.write_metadata(data)
        self.stdout.write(f'Recorded active translations in {self.metadata_path}')

    def write_default_file(self):
        en_file_path = self.file_path
        dest_file_path = self.file_path.relative_to(settings.FLUENT_LOCAL_PATH)
        dest_file_path = settings.FLUENT_REPO_PATH.joinpath(dest_file_path)
        if not dest_file_path.exists():
            dest_file_path.parent.mkdir(parents=True, exist_ok=True)

        with en_file_path.open() as enf:
            lines = [l for l in enf if not l.startswith('# LANG_ID_HASH')]

        with dest_file_path.open('w') as dfp:
            dfp.writelines(lines)

    def handle(self, *args, **options):
        self.filename = options['filename']
        self.force = options['force']
        if options['quiet']:
            self.stdout._out = StringIO()

        call_command('l10n_update', quiet=options['quiet'])
        self.record_active_translations()
        self.write_ftl_translations()
        self.write_default_file()
        self.stdout.write('Done')
