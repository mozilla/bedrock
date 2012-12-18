# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import itertools
import re
import os, errno
from os import path
from optparse import make_option
import codecs
from contextlib import closing
from StringIO import StringIO

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

                    if ext in ['.txt', '.html']:
                        full_path = os.path.join(root, filename)
                        yield full_path.replace(tmpl_dir, '').lstrip('/')


def update_templates(langs):
    """List templates with outdated/incorrect l10n blocks"""

    for tmpl in list_templates():
        print "%s..." % tmpl

        # Parse the reference template that will provide new content
        # and only get the blocks from it
        parser = L10nParser()
        blocks = list(parser.parse_template(app_tmpl(tmpl),
                                            only_blocks=True))

        for lang in langs:
            if path.exists(l10n_tmpl(tmpl, lang)):
                update_template(tmpl, blocks, lang)
            else:
                copy_template(tmpl, blocks, lang)


def get_todays_version():
    """Return the template version string for today"""

    return datetime.date.today().strftime('%Y%m%d')


def ensure_dir_exists(path):
    """Create directories for this path, like mkdir -p"""

    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise


def update_template(tmpl, blocks, lang):
    """Detect outdated l10n blocks and update the template"""

    def get_ref_block(name):
        """Return the reference block"""

        for block in blocks:
            if block['name'] == name:
                return block

    def transfer_content(l10n_block, ref_block):
        """Transfer any new content from the reference block"""

        if ref_block:
            # Update if the l10n file is older than this block
            if l10n_block['version'] < ref_block['version']:
                # Move the main content to the else content only if it
                # doesn't already exist, and then update the main content
                if not l10n_block['was']:
                    l10n_block['was'] = l10n_block['main']
                l10n_block['main'] = ref_block['main']

        return l10n_block

    parser = L10nParser()
    file_version = None
    dest_tmpl = l10n_tmpl(tmpl, lang)
    halted = False
    written_blocks = []

    # Make sure the templates directory for this locale and app exists
    ensure_dir_exists(os.path.dirname(dest_tmpl))

    # Parse the l10n template, run through it and update it where
    # appropriate into a new template file
    with closing(StringIO()) as buffer:
        for token in parser.parse_template(dest_tmpl, strict=False,
                                           halt_on_content=True):
            if not token:
                # If False is returned, that means a content block
                # exists so we don't do anything to the template since
                # it's customized
                return
            elif token[0] == 'content':
                buffer.write(token[1])
            elif token[0] == 'version':
                buffer.write('{# Version: %s #}' % get_todays_version())
                file_version = token[1]
            elif token[0] == 'block':
                if not file_version:
                    raise Exception('l10n file version tag does not exist '
                                    'before initial l10n block')

                # We have an l10n block, set its version and keep
                # track of it for later use
                l10n_block = token[1]
                l10n_block['version'] = file_version
                name = l10n_block['name']
                written_blocks.append(name)

                # Update the block and write it out
                l10n_block = transfer_content(l10n_block,
                                              get_ref_block(name))
                write_block(l10n_block, buffer)

        # Check for any missing blocks
        for block in blocks:
            if block['name'] not in written_blocks:
                buffer.write('\n\n')
                write_block(block, buffer)

        # Write out the result to the l10n template
        with codecs.open(dest_tmpl, 'w', 'utf-8') as dest:
            dest.write(buffer.getvalue())

    print '%s: %s' % (lang, tmpl)

def write_block(block, dest, force_was=False):
    """Write out a block to an l10n template"""

    dest.write('{%% l10n %s %%}\n' % block['name'])
    dest.write(block['main'])
    if block['was'] or force_was:
        dest.write('\n{% was %}')
        dest.write('\n%s' % block['was'] if block['was'] else '')
    dest.write('\n{% endl10n %}')


def copy_template(tmpl, blocks, lang):
    """Create a new l10n template by copying the l10n blocks"""

    dest_file = l10n_tmpl(tmpl, lang)

    if blocks:
        # Make sure the templates directory for this locale and app exists
        ensure_dir_exists(os.path.dirname(dest_file))

        with codecs.open(dest_file, 'w', 'utf-8') as dest:
            dest.write('{# Version: %s #}\n\n' % get_todays_version())
            dest.write('{%% extends "%s" %%}\n\n' % tmpl)

            for block in blocks:
                write_block(block, dest)
                dest.write('\n\n')


class L10nParser():

    file_version_re = re.compile('\W*Version: (\d+)\W*')

    def __init__(self):
        self.tmpl = None

    def parse_tmpl_version(self, tmpl):
        line = codecs.open(tmpl, encoding='utf-8').readline().strip()
        matches = self.file_version_re.match(line)
        if matches:
            return int(matches.group(1))
        return None

    def parse_template(self, tmpl, strict=True, halt_on_content=False,
                       only_blocks=False):
        """Read a template and parse the l10n blocks"""

        self.tmpl = tmpl
        for token in self.parse(codecs.open(tmpl, encoding='utf-8').read(),
                                strict,
                                halt_on_content,
                                only_blocks):
            yield token

    def parse(self, src, strict=True, halt_on_content=False,
              only_blocks=False):
        """Analyze a template and get the l10n block information"""

        self.tokens = Environment().lex(src)

        for token in self._parse(strict, halt_on_content):
            # Only return the block structure if requesting blocks,
            # otherwise return the full token
            if only_blocks:
                if token[0] == 'block':
                    yield token[1]
            else:
                yield token

    def _parse(self, strict, halt_on_content):
        """Walk through a list of tokens and parse them. This function
        yields 2 element tuples in the form (<type>, <content>), where
        <type> is of the following:

        * version: the version of the l10n file
        * content: a raw string of content from the template
        * block: an l10n block structure

        The full template is effectively emitted as a stream of the
        above tokens.
        """

        for token in self.tokens:
            name = token[1]

            if name == 'comment_begin':
                # Check comments for the version string
                comment = self.tokens.next()[2]

                matches = self.file_version_re.match(comment)
                if matches:
                    # Found the file version. call the callback and
                    # ignore the rest of the comment

                    version = self.parse_version(matches.group(1))

                    if not version:
                        raise Exception('Invalid version metadata in '
                                        'template: %s '% self.tmpl)

                    yield ('version', version)
                    self.scan_until('comment_end')
                else:
                    # It's a regular comment, so continue on normally
                    yield ('content', token[2])
                    yield ('content', comment)

            elif name == 'block_begin':
                space = self.tokens.next()
                block = self.tokens.next()

                if block[1] == 'name':
                    type = block[2]

                    # Start queue of tokens to yield, because we need
                    # to control when they are yielded
                    token_queue = []

                    if type == 'l10n':
                        # Parse l10n block into a useful structure
                        self.scan_ignore('whitespace')
                        for x in self.parse_block(strict):
                            yield x
                    else:
                        token_queue = [token, space, block]

                    if type == 'block' and halt_on_content:
                        # If it's a block, check if the name is
                        # "content" and stop parsing if it is because
                        # that means the template has been customized
                        # and we shouldn't touch it

                        ident_space = self.tokens.next()
                        ident = self.tokens.next()

                        if ident[2] == 'content':
                            # This is the content block, stop parsing
                            yield False
                            break
                        else:
                            # Otherwise, queue up the seen tokens for
                            # yielding
                            token_queue.extend([ident_space, ident])

                    for x in token_queue:
                        yield ('content', x[2])
                else:
                    raise Exception("Invalid block syntax: %s", self.tmpl)
            else:
                yield ('content', token[2])

    def parse_version(self, version_str):
        # Version must be in the date format YYYYMMDD
        if len(version_str) != 8:
            return None

        try:
            return int(version_str)
        except ValueError:
            return None

    def parse_block(self, strict=True):
        """Parse out the l10n block metadata and content"""

        block_name = self.scan_next('name')
        block_version = None

        self.scan_ignore('whitespace')
        if self.scan_next('operator') == ',':
            self.scan_ignore('whitespace')
            version_str = self.scan_next('integer')
            block_version = self.parse_version(version_str)

            if not block_version:
                raise Exception("Invalid l10n block declaration: "
                                "bad version '%s' in %s"
                                % (block_name, self.tmpl))

            self.scan_until('block_end')
        elif strict:
            raise Exception("Invalid l10n block declaration: "
                            "missing date for block '%s' in %s"
                            % (block_name, self.tmpl))

        (main, was_) = self.block_content()
        yield ('block', {'name': block_name,
                         'version': block_version,
                         'main': main,
                         'was': was_})

    def block_content(self):
        """Parse the content from an l10n block"""

        in_was = False
        main_content = []
        was_content = []

        for token in self.tokens:
            buffer = was_content if in_was else main_content

            if token[1] == 'block_begin':
                space = self.tokens.next()[2]
                name = self.tokens.next()[2]

                if name == 'endl10n':
                    self.scan_until('block_end')
                    break
                elif name == 'was':
                    in_was = True
                    self.scan_until('block_end')
                    continue
                else:
                    buffer.append(token[2])
                    buffer.append(space)
                    buffer.append(name)
                    continue
            else:
                buffer.append(token[2])

        return [''.join(x).replace('\\n', '\n').strip()
                for x in [main_content, was_content]]

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
            langs = filter(lambda x: x[0] != '.' , langs)

        update_templates(langs)
