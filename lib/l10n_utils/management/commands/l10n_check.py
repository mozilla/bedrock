import itertools
import os
from os import path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from jingo import get_env
from jinja2 import Environment
from jinja2.parser import Parser


class Command(BaseCommand):
    args = ''
    help = 'Checks which content needs to be localized.'

    def handle(self, *args, **options):
        l10n_dir = False

        # Find the directory with localized templates
        for tmpl_dir in settings.TEMPLATE_DIRS:
            d = path.join(tmpl_dir, 'l10n')
            if path.exists(d):
                l10n_dir = d
                break

        if not l10n_dir:
            print "No l10n template directory found."
            return

        # Check all the l10n blocks in all the main templates against
        # the localized ones and print any that are out of date
        for tmpl in self.list_templates():
            for lang in os.listdir(l10n_dir):
                localized_tmpl = path.join('l10n', lang, tmpl)
                localized_path = path.join(l10n_dir, lang, tmpl)

                if path.exists(localized_path):
                    blocks = self.parse_template(tmpl)
                    l10n_blocks = self.parse_template(localized_tmpl)
                    
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
        src = env.loader.get_source(env, tmpl)

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
