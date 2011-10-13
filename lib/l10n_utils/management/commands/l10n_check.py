from datetime import date
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
    blocks = [x[1] for x in parser.parse_template(app_tmpl(tmpl))
               if x and x[0] == 'block']
    file_version = None
    dest_tmpl = l10n_tmpl(tmpl, lang)
    dest = open('%s.tmp' % dest_tmpl, 'w')

    halted = False
    written_blocks = []

    for token in parser.parse_template(dest_tmpl, strict=False,
                                       halt_on_content=True):
        if not token:
            # If False is returned, we halt
            halted = True
            break
        elif token[0] == 'content':
            dest.write(token[1])
        elif token[0] == 'version':
            dest.write('{# Version: %s #}' % date.today().strftime('%Y%m%d'))
            file_version = token[1]
        elif token[0] == 'block':
            if not file_version:
                raise Exception('l10n file version tag does not exist '
                                'before initial l10n block')

            # We have an l10n block, get the reference block from the
            # list of blocks
            l10n_block = token[1]
            block = next((x for x in blocks
                          if x['name'] == l10n_block['name']), None)

            # Keep track of the l10n blocks for later use
            written_blocks.append(l10n_block['name'])

            if block:
                # Update if the l10n file is older than this block
                if file_version < block['version']:
                    # Move the main content to the else content only if it
                    # doesn't already exist, and then update the main content
                    if not l10n_block['else']:
                        l10n_block['else'] = l10n_block['main']
                    l10n_block['main'] = block['main']
            
            write_block(l10n_block, dest)

    # Check for any missing blocks
    for block in blocks:
        if block['name'] not in written_blocks:
            dest.write('\n\n')
            write_block(block, dest, force_else=True)

    if halted:
        dest.close()
        # remove the file
    else: pass
        # move the file over

    print 'done!'

def write_block(block, dest, force_else=False):
    """Write out a block to an l10n template"""

    dest.write('{%% l10n %s %%}\n' % block['name'])
    dest.write(block['main'])
    if block['else'] or force_else:
        dest.write('\n{% else %}')
        dest.write('\n%s' % block['else'] if block['else'] else '')
    dest.write('\n{% endl10n %}')


def copy_template(tmpl, lang):
    """Create a new l10n template by copying the l10n blocks"""

    parser = L10nParser()
    blocks = parser.parse_template(app_tmpl(tmpl))
    if blocks:
        write_l10n_template(blocks, tmpl, lang)


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

    def parse_template(self, tmpl, strict=True, halt_on_content=False):
        """Read a template and parse the l10n blocks"""

        self.tmpl = tmpl
        for x in self.parse(codecs.open(tmpl, encoding='utf-8').read(),
                            strict,
                            halt_on_content):
            yield x

    def parse(self, src, strict=True, halt_on_content=False):
        """Analyze a template and get the l10n block information"""

        self.tokens = Environment().lex(src)
        for x in self._parse(strict, halt_on_content):
            yield x

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

        (main, else_) = self.block_content()
        yield ('block', {'name': block_name,
                         'version': block_version,
                         'main': main,
                         'else': else_})

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
