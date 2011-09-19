import datetime
import itertools
import re
import os, errno
from os import path
from optparse import make_option
import codecs

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from jinja2 import Environment, TemplateNotFound
from jinja2.parser import Parser


def l10n_file(*args):
    return path.join(settings.ROOT, 'locale', *args)


def l10n_tmpl(tmpl, lang):
    return l10n_file(lang, 'templates', tmpl)


def app_tmpl(tmpl):
    app = tmpl[:tmpl.index('/')]
    return path.join(settings.ROOT, 'apps', app, 'templates', tmpl)


def list_templates():
    """List all the templates in all the installed apps"""

    for app in settings.INSTALLED_APPS:
        tmpl_dir = path.join(settings.ROOT, 'apps', app, 'templates')

        if path.exists(tmpl_dir):
            # Find all the .html files
            for root, dirs, files in os.walk(tmpl_dir):
                for filename in files:
                    name, ext = os.path.splitext(filename)

                    if ext == '.html':
                        full_path = os.path.join(root, filename)
                        yield full_path.replace(tmpl_dir, '').lstrip('/')


def update_templates(langs):
    """List templates with outdated/incorrect l10n blocks"""

    for tmpl in list_templates():
        for lang in langs:
            if path.exists(l10n_tmpl(tmpl, lang)):
                update_template(tmpl, lang)
            else:
                copy_template(tmpl, lang)


def update_template(tmpl, lang):
    """Detect outdated/incorrect l10n block and notify"""

    parser = L10nParser()
    blocks = parser.parse_template(app_tmpl(tmpl))

    t = l10n_tmpl(tmpl, lang)
    l10n_blocks = parser.parse_template(t, strict=False)
    l10n_version = parser.parse_tmpl_version(t)

    for name, data in blocks.iteritems():
        if name in l10n_blocks:
            old = l10n_blocks[name]

            if l10n_version < data['version']:
                # Move the main content to the else content only if it
                # doesn't already exist, and then update the main content
                if not old['else_content']:
                    old['else_content'] = old['main_content']
                old['main_content'] = data['main_content']
        else:
            l10n_blocks[name] = data

    write_l10n_template(l10n_blocks, tmpl, lang)


def write_l10n_template(blocks, tmpl, lang):
    """Write out blocks to an l10n template"""
    dest = l10n_tmpl(tmpl, lang)

    # Make sure the template dir exists
    try:
        os.makedirs(os.path.dirname(dest))
    except OSError as exc:
        if exc.errno == errno.EEXIST: pass
        else: raise

    with open(dest, 'w+') as file:
        today = datetime.date.today()
        file.write('{# Version: %s #}\n' % today.strftime('%Y%m%d'))
        file.write('{# DO NOT MODIFY THE ABOVE LINE #}\n\n')

        for (name, data) in blocks.iteritems():
            file.write('{%% l10n %s %%}\n' % name)
            file.write(data['main_content'])
            if(data['else_content']):
                file.write('\n{% else %}\n')
                file.write(data['else_content'])
            file.write('\n{% endl10n %}\n\n')


def copy_template(tmpl, lang):
    """Create a new l10n template by copying the l10n blocks"""

    parser = L10nParser()
    blocks = parser.parse_template(app_tmpl(tmpl))
    if blocks:
        write_l10n_template(blocks, tmpl, lang)


class L10nParser():

    file_version_re = re.compile('{# Version: (\d+) #}')

    def __init__(self):
        self.tmpl = None

    def parse_tmpl_version(self, tmpl):
        line = codecs.open(tmpl, encoding='utf-8').readline().strip()
        matches = self.file_version_re.match(line)
        if matches:
            return int(matches.group(1))
        return None

    def parse_template(self, tmpl, strict=True):
        """Read a template and parse the l10n blocks"""
        self.tmpl = tmpl
        return self.parse(codecs.open(tmpl, encoding='utf-8').read(),
                          strict=strict)

    def parse(self, src, strict=True):
        """Analyze a template and get the l10n block information"""

        env = Environment()
        self.tokens = env.lex(src)
        blocks = {}

        for name, version in self.parse_blocks(strict):
            main_content, else_content = self.block_content()

            blocks[name] = {'version': version,
                            'main_content': main_content,
                            'else_content': else_content}

        return blocks

    def parse_blocks(self, strict):
        """Extract tags from the l10n block"""

        while self.scan_until('block_begin'):
            self.scan_ignore('whitespace')
            name = self.scan_next('name')

            if name != 'l10n':
                continue

            self.scan_ignore('whitespace')

            block_name = self.scan_next('name')
            block_version = None

            if self.scan_next('operator') == ',':
                self.scan_ignore('whitespace')
                block_version = self.scan_next('integer')
                error = False

                # Version must be in the date format YYYYMMDD
                if len(block_version) != 8:
                    error = True

                try:
                    block_version = int(block_version)
                except ValueError:
                    error = True

                if error:
                    raise Exception("Invalid l10n block declaration: "
                                    "bad version '%s' in %s"
                                    % (block_name, self.tmpl))
            elif strict:
                raise Exception("Invalid l10n block declaration: "
                                "missing date for block '%s' in %s"
                                % (block_name, self.tmpl))

            self.scan_until('block_end')
            yield [block_name, block_version]

    def block_content(self):
        """Parse the content from an l10n block"""

        in_else = False
        main_content = []
        else_content = []

        for token in self.tokens:
            if token[1] == 'block_begin':
                self.scan_ignore('whitespace')
                name = self.scan_next('name')

                if name == 'endl10n':
                    self.scan_until('block_end')
                    break
                elif name == 'else':
                    in_else = True
                    self.scan_until('block_end')
                    continue

            buffer = else_content if in_else else main_content
            buffer.append(token[2])

        return [''.join(x).replace('\\n', '\n').strip() 
                for x in [main_content, else_content]]
        
    def scan_until(self, name):
        for token in self.tokens:
            if token[1] == name:
                return True
        return False

    def scan_ignore(self, name):
        for token in self.tokens:
            if token[1] != name:
                # Put it back on the list
                self.tokens = itertools.chain([token], self.tokens)
                break

    def scan_next(self, name):
        token = self.tokens.next()
        if token and token[1] == name:
            return token[2]
        return False


class Command(BaseCommand):
    args = ''
    help = 'Checks which content needs to be localized.'

    def handle(self, *args, **options):
        # Look through languages passed in, or all of them
        if args:
            langs = args
        else:
            langs = os.listdir(l10n_file())

        update_templates(langs)
