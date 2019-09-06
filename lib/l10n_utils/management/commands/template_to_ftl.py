# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from hashlib import md5
from io import StringIO
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.utils.functional import cached_property

from lib.l10n_utils.extract import tweak_message
from lib.l10n_utils.utils import get_ftl_file_data


GETTEXT_RE = re.compile(r'\b_\([\'"](?P<string>.+?)[\'"]\)'
                        r'(\s*\|\s*format\((?P<args>\w.+?)\))?', re.S)
TRANS_BLOCK_RE = re.compile(r'{%-?\s+trans\s+((?P<args>\w.+?)\s+)?-?%\}\s*'
                            r'(?P<string>.+?)'
                            r'\s*{%-?\s+endtrans\s+-?%\}', re.S)
STR_VARIABLE_RE = re.compile(r'{{\s*(?P<var>\w+?)\s*}}')


class Command(BaseCommand):
    help = 'Convert a template to use Fluent for l10n'
    _filename = None
    _template = None

    def add_arguments(self, parser):
        parser.add_argument('ftl_file')
        parser.add_argument('template')
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),
        parser.add_argument('-f', '--force', action='store_true', dest='force', default=False,
                            help='Overwrite the FTL template if it exists.'),

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
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = Path(value)

    @property
    def ftl_template(self):
        ftl_template = f'{self.template.stem}_ftl.html'
        return self.template.with_name(ftl_template)

    @cached_property
    def ftl_file_data(self):
        return get_ftl_file_data(self.filename)

    def template_replace(self, match):
        trans_block = match[0].startswith('{%')
        ftl_data = self.ftl_file_data
        str_id = tweak_message(match['string'])
        if '%s' in str_id:
            self.stderr.write('WARNING: Place-holder with no variable name found in string. '
                              'Convert "%s" to a Fluent variable in the new file.')
        str_id = STR_VARIABLE_RE.sub(r'%(\1)s', str_id)
        str_hash = md5(str_id.encode()).hexdigest()
        ftl_id = ftl_data.get(str_hash)
        if ftl_id:
            if match['args']:
                new_str = f"ftl('{ftl_id}', {match['args']})"
            else:
                new_str = f"ftl('{ftl_id}')"

            if trans_block:
                new_str = f"{{{{ {new_str} }}}}"

            return new_str

        self.stderr.write(f'NO MATCH: {str_id}')
        return match[0]

    def ftl_template_lines(self):
        with self.template.open('r') as tfp:
            template_str = tfp.read()
            template_str = GETTEXT_RE.sub(self.template_replace, template_str)
            template_str = TRANS_BLOCK_RE.sub(self.template_replace, template_str)
            self.stdout.write('.', ending='')
            self.stdout.flush()

        return template_str

    def write_ftl_template(self):
        with self.ftl_template.open('w') as ftlt:
            ftlt.writelines(self.ftl_template_lines())

    def handle(self, *args, **options):
        self.filename = options['ftl_file']
        self.template = options['template']
        if options['quiet']:
            self.stdout._out = StringIO()

        if self.ftl_template.exists() and not options['force']:
            raise CommandError('Output file exists. Use --force to overwrite.')

        self.write_ftl_template()
        self.stdout.write('\nDone')
