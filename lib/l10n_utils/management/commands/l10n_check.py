import itertools
import os
from os import path
from optparse import make_option
import codecs

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from jingo import get_env
from jinja2 import Environment, TemplateNotFound
from jinja2.parser import Parser


class Command(BaseCommand):
    args = ''
    help = 'Checks which content needs to be localized.'
    
    option_list = BaseCommand.option_list + (
        make_option('-t',
                    action='store_true',
                    dest='templates',
                    default=False,
                    help='Show non-existant templates for locales'),
        )

    def handle(self, *args, **options):
        # Look through languages passed in, or all of them
        if args:
            langs = args
        else:
            langs = os.listdir(self.l10n_file())

        if options['templates']:
            self.check_templates(langs)
        else:
            self.check_blocks(langs)

    def l10n_file(self, *args):
        return path.join(settings.ROOT, 'locale', *args)

    def check_templates(self, langs):
        for tmpl in self.list_templates():
            for lang in langs:
                fullpath = self.l10n_file(lang, 'templates', tmpl)
                if not path.exists(fullpath):
                    print fullpath
                

    def check_blocks(self, langs):
        # Check all the l10n blocks in all the main templates against
        # the blocks in the localized templates

        for tmpl in self.list_templates():
            for lang in langs:
                fullpath = self.l10n_file(lang, 'templates', tmpl)

                if path.exists(fullpath):
                    blocks = self.parse_template(tmpl)
                    l10n_blocks = self.parse_template(fullpath)
                    
                    self.compare_versions(tmpl, lang, blocks, l10n_blocks)


    def compare_versions(self, tmpl, lang, latest, localized):
        for name, version in latest.iteritems():
            if version:
                if not name in localized:
                    print "%s: %s needs %s localized" % (tmpl, lang, name)
                elif not localized[name]:
                    print ("%s: %s has unversioned %s but should be v%s"
                           % (tmpl, lang, name, version))
                elif localized[name] < version:
                    print ("%s: %s has %s at v%s but needs to be at v%s" 
                           % (tmpl, lang, name, localized[name], version))
        
    def list_templates(self):
        for app in settings.INSTALLED_APPS:
            tmpl_dir = path.join(settings.ROOT, 'apps', app, 'templates')

            if path.exists(tmpl_dir):
                # Find all the .html files
                for root, dirs, files in os.walk(tmpl_dir):
                    for filename in files:
                        name, ext = os.path.splitext(filename)

                        if ext == '.html':
                            full_path = os.path.join(root, filename)

                            # Strip the path to get just the
                            # namespaced template name
                            yield full_path.replace(tmpl_dir, '').lstrip('/')
                            
    def parse_template(self, tmpl):
        env = get_env()

        try:
            src = env.loader.get_source(env, tmpl)
        except TemplateNotFound:
            src = codecs.open(tmpl, encoding='utf-8').read()

        self.tokens = env.lex(src)
        blocks = {}

        while self.scan_until('block_begin'):
            self.scan_ignore('whitespace')
            blockname = self.scan_next('name')

            if blockname == 'l10n':
                self.scan_ignore('whitespace')
                name = self.scan_next('name')
                self.scan_ignore('whitespace')

                if self.scan_next('operator') == ',':
                    self.scan_ignore('whitespace')
                    
                    version = self.scan_next('integer')
                    
                    try:
                        version = int(version)
                    except ValueError:
                        raise Exception("Invalid l10n block declaration '%s' in %s"
                                        % (name, tmpl))

                    blocks[name] = version
                else:
                    blocks[name] = False    
        return blocks

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
