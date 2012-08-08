# coding=utf-8

"""This library parses dotlang files migrated over from the old PHP
system.

It caches them using the django caching library, but it could
potentially just use thread-local variables. Caching seems safer at
the expense of another caching layer."""

import codecs
import os
import re

from django.conf import settings
from django.core.cache import cache
from django.utils import translation
from django.utils.functional import lazy

FORMAT_IDENTIFIER_RE = re.compile(r"""(%
                                      (?:\((\w+)\))? # Mapping key
                                      s)""", re.VERBOSE)


def parse(path):
    """Parse a dotlang file and return a dict of translations."""
    trans = {}

    if not os.path.exists(path):
        return trans

    with codecs.open(path, 'r', 'utf-8', errors='replace') as lines:
        source = None

        for line in lines:
            if u'�' in line:
                mail_error(path, line)

            line = line.strip()
            if line == '' or line[0] == '#':
                continue

            if line[0] == ';':
                source = line[1:]
            elif source:
                for tag in ('{ok}', '{l10n-extra}'):
                    if line.endswith(tag):
                        line = line[:-len(tag)]
                trans[source] = line.strip()

    return trans


def mail_error(path, message):
    """Email managers when an error is detected"""
    from django.core import mail
    subject = '%s is corrupted' % path
    mail.mail_managers(subject, message)


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
        if trans is None:
            path = os.path.join(settings.ROOT, 'locale', lang,
                                '%s.lang' % file_)
            trans = parse(path)
            cache.set(key, trans, settings.DOTLANG_CACHE)

        if text in trans:
            original = FORMAT_IDENTIFIER_RE.findall(text)
            translated = FORMAT_IDENTIFIER_RE.findall(trans[text])
            if original != translated:
                message = '%s\n%s' % (text, trans[text])
                mail_error(file_, message)
                return text
            return trans[text]
    return text


def _(text, *args):
    """Translate a piece of text from the global files"""
    text = translate(text, settings.DOTLANG_FILES)
    if args:
        text = text % args
    return text

_lazy = lazy(_, unicode)

def get_lang_path(path):
    """Generate the path to a lang file from a django path.
    /apps/foo/templates/foo/bar.html -> /foo/bar.lang
    /templates/foo.html -> /foo.lang
    /foo/bar.html -> /foo/bar.lang"""

    p = path.split('/')

    try:
        i = p.index('templates')
        p = p[i + 1:]
    except ValueError:
        pass

    path = '/'.join(p)
    (base, ext) = os.path.splitext(path)
    return '%s.lang' % base
