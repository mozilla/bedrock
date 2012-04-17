"""This library parses dotlang files migrated over from the old PHP
system.

It caches them using the django caching library, but it could
potentially just use thread-local variables. Caching seems safer at
the expense of another caching layer."""

import codecs
import os

from django.conf import settings
from django.core.cache import cache
from django.utils import translation

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
                    source = line[1:]
                elif source:
                    for tag in ('{ok}', '{l10n-extra}'):
                        if line.endswith(tag):
                            line = line[:-len(tag)]
                    trans[source] = line.strip()

    return trans


def fix_case(locale):
    """Convert lowercase locales to uppercase: en-us -> en-US"""
    parts = locale.split('-')
    if len(parts) == 1:
        return locale
    else:
        return '%s-%s' % (parts[0], parts[1].upper())


def translate(text, files):
    """Search a list of .lang files for a translation"""
    lang = fix_case(translation.get_language())

    for file_ in files:
        key = "dotlang-%s-%s" % (lang, file_)

        trans = cache.get(key)
        if not trans:
            path = os.path.join(settings.ROOT, 'locale', lang,
                                '%s.lang' % file_)
            trans = parse(path)
            cache.set(key, trans, settings.DOTLANG_CACHE)

        if text in trans:
            return trans[text]
    return text


def _(text, *args):
    """Translate a piece of text from the global files"""
    text = translate(text, settings.DOTLANG_FILES)
    if args:
        text = text % args
    return text


def get_lang_path(path):    
    """Generate the path to a lang file from a django path. 
    /apps/foo/templates/foo/bar.html -> /foo/bar.lang
    /templates/foo.html -> /foo.lang
    /foo/bar.html -> /foo/bar.lang"""

    p = path.split('/')

    try:
        i = p.index('templates')
        p = p[i+1:]
    except ValueError: pass

    path =  '/'.join(p)
    (base, ext) = os.path.splitext(path)
    return '%s.lang' % base
