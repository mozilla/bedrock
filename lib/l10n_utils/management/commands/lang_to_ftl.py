# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from hashlib import md5
from io import StringIO
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.text import slugify

from lib.l10n_utils.dotlang import parse as parse_lang, convert_variables


def string_to_ftl_id(string):
    string = strip_tags(string)
    slug_parts = slugify(string).split('-')
    slug = slug_parts.pop(0)
    for part in slug_parts:
        slug = '-'.join([slug, part])
        if len(slug) > 30:
            break

    return slug


def format_ftl_string(ftl_id, string, string_id, comment):
    output = f'# LANG_ID_HASH: {md5(string_id.encode()).hexdigest()}\n'
    output += f'# {comment}\n' if comment else ''
    return output + f'{ftl_id} = {string}\n\n'


class Command(BaseCommand):
    help = 'Convert an en-US .lang file to an en .ftl file'
    _filename = None

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
        if not value.endswith('.lang'):
            self._filename = f'{value}.lang'
        else:
            self._filename = value

    @property
    def filename_prefix(self):
        """Return a slugified version of the .lang filename for use as a FTL string ID prefix"""
        return slugify(Path(self.filename).stem)

    @property
    def ftl_file_path(self):
        return settings.FLUENT_LOCAL_PATH.joinpath('en', self.filename).with_suffix('.ftl')

    def get_ftl_id(self, string):
        return '-'.join([self.filename_prefix, string_to_ftl_id(string)])

    def get_translations(self):
        path = settings.LOCALES_PATH.joinpath('en-US', self.filename)
        return parse_lang(path, skip_untranslated=False, extract_comments=True)

    def get_ftl_strings(self):
        translations = self.get_translations()
        all_strings = {}
        for str_id, string in translations.items():
            comment, string = string
            if comment and comment.startswith('TAG:'):
                # ignore tag comments
                comment = None

            if '%s' in string:
                self.stderr.write('WARNING: Place-holder with no variable name found in string. '
                                  'Look for "$VARIABLE_MISSING" in the new file.')
            # percent symbols are doubled in lang file strings
            # no need for this in ftl files
            # also breaks string matching in templates
            string = string.replace('%%', '%')
            str_id = str_id.replace('%%', '%')
            ftl_id = self.get_ftl_id(str_id)
            # make sure it's unique
            if ftl_id in all_strings:
                ftl_iteration = 0
                ftl_unique = ftl_id
                while ftl_unique in all_strings:
                    ftl_iteration += 1
                    ftl_unique = f'{ftl_id}_{ftl_iteration}'

                ftl_id = ftl_unique

            all_strings[ftl_id] = {
                'string': convert_variables(string),
                'string_id': str_id,
                'comment': comment,
            }

        return all_strings

    def write_ftl_file(self):
        self.ftl_file_path.parent.mkdir(parents=True, exist_ok=True)
        strings = self.get_ftl_strings()
        with self.ftl_file_path.open('w') as ftl:
            for string_id, string_info in strings.items():
                ftl.write(format_ftl_string(string_id, **string_info))

    def handle(self, *args, **options):
        self.filename = options['filename']
        if options['quiet']:
            self.stdout._out = StringIO()

        if self.ftl_file_path.exists() and not options['force']:
            raise CommandError('Output file exists. Use --force to overwrite.')

        self.write_ftl_file()
        self.stdout.write(f'Finished converting {self.filename}')
        self.stdout.write(f'Inspect the file before converting translations: {self.ftl_file_path}')
