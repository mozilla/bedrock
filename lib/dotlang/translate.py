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
                    trans[source[1:]] = line

    return trans

def load(lang):
    """Load the dotlang files for the specific lang and cache them in
    django."""
    trans = {}

    for f in settings.DOTLANG_FILES:
        path = os.path.join(settings.ROOT, 'locale', lang, f)
        trans.update(parse(path))

    cache.set('trans-%s' % lang, trans, settings.DOTLANG_CACHE)
    return trans

def translate(lang, text):
    """Translate a piece of text, loading the language's dotlang files
    if they aren't cached"""

    key = 'trans-%s' % lang
    trans = cache.get(key)

    if not trans:
        trans = load(lang)

    return trans.get(text, text)

    
