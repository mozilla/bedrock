"""This library parses dotlang files migrated over from the old PHP
system.

It caches them using the django caching library, but it could
potentially just use thread-local variables. Caching seems safer at
the expense of another caching layer."""

import codecs
import os

from django.conf import settings
from django.core.cache import cache


def parse(path):
    """Parse a dotlang file and return a dict of translations."""
    trans = {}

    if not os.path.exists(path):
        return trans

    with codecs.open(path, 'r', 'utf-8') as lines:
        source = None

        for line in lines:
            line = line.strip()
            if line != '':
                if line[0] == ';':
                    source = line
                elif source:
                    trans[source[1:].lower()] = line

    return trans


def load(files, lang):
    """Load the dotlang files for the specific lang and cache them in
    django. Return a single dict with all the translations."""

    final = {}

    for file_ in files:
        key = "dotlang-%s-%s" % (lang, file_)

        trans = cache.get(key)
        if not trans:
            path = os.path.join(settings.ROOT, 'locale', lang,
                                '%s.lang' % file_)
            trans = parse(path)
            cache.set(key, trans, settings.DOTLANG_CACHE)
        final.update(trans)

    return final


def translate(files, lang, text):
    """Translate a piece of text, loading the language's dotlang files
    if they aren't cached"""

    trans = load(files, lang)
    return trans.get(text, text)


def get_lang_path(path):    
    """Generate the path to a lang file from a django path. 
    /apps/foo/templates/foo/bar.html -> /foo/bar.lang
    /apps/foo/bar.py -> /foo/bar.lang
    /templates/foo.html -> /foo.lang
    /foo/bar.html -> /foo/bar.lang"""

    p = path.split('/')

    try:
        i = p.index('templates')
        p = p[i+1:]
    except ValueError:
        if p[0] == 'apps':
            p = p[1:]

    path =  '/'.join(p)
    (base, ext) = os.path.splitext(path)
    return '%s.lang' % base

class Translations(object):
    """A helper class to load and maintain translations"""

    def __init__(self):
        self.trans = {}
        self.loaded = False

    def add(self, files, locale):
        files = [files] if isinstance(files, basestring) else files
        self.trans.update(load(files, locale))
        self.loaded = True
        
    def __getitem__(self, key):
        return self.trans[key]

    def get(self, key, default=None):
        return self.trans.get(key.lower(), default)
