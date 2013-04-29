# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""This library parses dotlang files migrated over from the old PHP
system.

It caches them using the django caching library, but it could
potentially just use thread-local variables. Caching seems safer at
the expense of another caching layer."""
import codecs
import inspect
import os
import re
from functools import partial

from django.conf import settings
from django.core.cache import cache
from django.utils import translation
from django.utils.functional import lazy

from jinja2 import Markup
from tower.management.commands.extract import tweak_message


FORMAT_IDENTIFIER_RE = re.compile(r"""(%
                                      (?:\((\w+)\))? # Mapping key
                                      s)""", re.VERBOSE)


def parse(path, skip_untranslated=True):
    """
    Parse a dotlang file and return a dict of translations.
    :param path: Absolute path to a lang file.
    :param skip_untranslated: Exclude strings for which the ID and translation
                              match.
    :return: dict
    """
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
                line = line.strip()
                if skip_untranslated and source == line:
                    continue
                trans[source] = line

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

    # don't attempt to translate the default language.
    if lang == settings.LANGUAGE_CODE:
        return Markup(text)

    tweaked_text = tweak_message(text)

    for file_ in files:
        key = "dotlang-%s-%s" % (lang, file_)
        rel_path = os.path.join('locale', lang, '%s.lang' % file_)

        trans = cache.get(key)
        if trans is None:
            path = os.path.join(settings.ROOT, rel_path)
            trans = parse(path)
            cache.set(key, trans, settings.DOTLANG_CACHE)

        if tweaked_text in trans:
            original = FORMAT_IDENTIFIER_RE.findall(text)
            translated = FORMAT_IDENTIFIER_RE.findall(trans[tweaked_text])
            if set(original) != set(translated):
                explanation = ('The translation has a different set of '
                               'replaced text (aka %s)')
                message = '%s\n\n%s\n%s' % (explanation, text,
                                            trans[tweaked_text])
                mail_error(rel_path, message)
                return Markup(text)
            return Markup(trans[tweaked_text])
    return Markup(text)


def _get_extra_lang_files():
    frame = inspect.currentframe()
    new_lang_files = []
    if frame is None:
        if settings.DEBUG:
            import warnings
            warnings.warn('Your Python runtime does not support the frame '
                          'stack. Extra LANG_FILES specified in Python '
                          'source files will not work.', RuntimeWarning)
    else:
        try:
            # gets value of LANG_FILE constant in calling module if specified.
            # have to go back 2x to compensate for this function.
            new_lang_files = frame.f_back.f_back.f_globals.get('LANG_FILES', [])
        finally:
            del frame
        if new_lang_files:
            if isinstance(new_lang_files, basestring):
                new_lang_files = [new_lang_files]
    return [lf for lf in new_lang_files if lf not in settings.DOTLANG_FILES]


def _(text, *args, **kwargs):
    """
    Translate a piece of text from the global files. If `LANG_FILES` is defined
    in the module from which this function is called, those files (or file)
    will be searched first for the translation, followed by the default files.

    :param text: string to translate
    :param args: items for interpolation into `text`
    :param lang_files: extra lang file names to search for a translation.
        NOTE: DO NOT USE THIS for string extraction. It will NOT respect
        the values in this kwarg when extracting strings. This is only useful
        if you know the string is in a different file but you don't want to
        add that file for the whole module via the `LANG_FILES` constant.
    :return: translated string
    """
    lang_files = kwargs.pop('lang_files', [])
    if isinstance(lang_files, list):
        lang_files = lang_files[:]
    else:
        lang_files = [lang_files]
    if not lang_files:
        lang_files += _get_extra_lang_files()
    lang_files += settings.DOTLANG_FILES

    text = translate(text, lang_files)
    if args:
        text = text % args
    return text


_lazy_proxy = lazy(_, unicode)


def _lazy(*args, **kwargs):
    lang_files = _get_extra_lang_files()
    if lang_files:
        return partial(_lazy_proxy, lang_files=lang_files)(*args, **kwargs)
    return _lazy_proxy(*args, **kwargs)


def get_lang_path(path):
    """Generate the path to a lang file from a django path.
    /apps/foo/templates/foo/bar.html -> foo/bar
    /templates/foo.html -> foo
    /foo/bar.html -> foo/bar"""

    p = path.split('/')

    try:
        i = p.index('templates')
        p = p[i + 1:]
    except ValueError:
        pass

    path = '/'.join(p)
    base, ext = os.path.splitext(path)
    return base


def lang_file_is_active(path, lang):
    """
    If the lang file for a locale exists and has the correct comment returns
    True, and False otherwise.
    :param path: the relative lang file name
    :param lang: the language code
    :return: bool
    """
    rel_path = os.path.join('locale', lang, '%s.lang' % path)
    cache_key = 'active:%s' % rel_path
    is_active = cache.get(cache_key)
    if is_active is None:
        is_active = False
        fpath = os.path.join(settings.ROOT, rel_path)
        try:
            with codecs.open(fpath, 'r', 'utf-8', errors='replace') as lines:
                firstline = lines.readline()
                # Filter out Byte order Mark
                firstline = firstline.replace(u'\ufeff', '')
                if firstline.startswith('## active ##'):
                    is_active = True
        except IOError:
            pass

        cache.set(cache_key, is_active, settings.DOTLANG_CACHE)

    return is_active
