# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import with_statement

import codecs
import os
import re
from os.path import join
from tokenize import generate_tokens, NAME, NEWLINE, OP, untokenize

from django.conf import settings
from django.core.cache import get_cache
from django.template.loader import get_template
from jinja2 import Environment

from dotlang import parse as parse_lang, get_lang_path, lang_file_is_active


REGEX_URL = re.compile(r'.* (\S+/\S+\.[^:]+).*')
cache = get_cache('l10n')


def parse_po(path):
    msgs = {}

    if not os.path.exists(path):
        return msgs

    with codecs.open(path, 'r', 'utf-8') as lines:
        def parse_string(s):
            return s.strip('"').replace('\\"', '"')

        def extract_content(s):
            # strip the first word and quotes
            return parse_string(s.split(' ', 1)[1])

        msgid = None
        msgpath = None
        msgcomment = None

        for line in lines:
            line = line.strip()
            if line.startswith('#:'):
                matches = REGEX_URL.match(line)
                if matches:
                    msgpath = matches.group(1)
            elif line.startswith('#.'):
                msgcomment = line.lstrip('#.').strip()
            elif line.startswith('msgid'):
                msgid = extract_content(line)
            elif line.startswith('msgstr') and msgid and msgpath:
                if msgpath not in msgs:
                    msgs[msgpath] = []
                msgs[msgpath].append([msgcomment, msgid])
                msgid = None
                msgpath = None
                msgcomment = None
            elif msgid is not None:
                msgid += parse_string(line)

    return msgs


def po_msgs():
    return parse_po(join(settings.ROOT, 'locale', 'templates', 'LC_MESSAGES',
                         'messages.pot'))


def translated_strings(file_):
    path = join(settings.ROOT, 'locale', 'templates', file_)
    trans = parse_lang(path).keys()
    return trans


def lang_file(name, lang):
    return join(settings.ROOT, 'locale', lang, name)


def is_template(path):
    (base, ext) = os.path.splitext(path)
    return ext == '.html'


def is_python(path):
    (base, ext) = os.path.splitext(path)
    return ext == '.py'


def parse_python(path):
    """
    Look though a python file and extract the specified `LANG_FILES` constant
    value and return it.

    `LANG_FILES` must be defined at the module level, and can be a string or
    list of strings.
    """
    result = []
    in_lang = False
    in_lang_val = False
    with codecs.open(path, encoding='utf-8') as src_f:
        tokens = generate_tokens(src_f.readline)
        for token in tokens:
            t_type, t_val, (t_row, t_col) = token[:3]
            # find the start of the constant declaration
            if t_type == NAME and t_col == 0 and t_val == 'LANG_FILES':
                in_lang = True
                continue
            if in_lang:
                # we only want the value, so start recording after the = OP
                if t_type == OP and t_val == '=':
                    in_lang_val = True
                    continue
                # stop when there's a newline. continuation newlines are a
                # different type so multiline list literals work fine
                if t_type == NEWLINE:
                    break
                if in_lang_val:
                    result.append((t_type, t_val))

    if result:
        new_lang_files = eval(untokenize(result))
        if isinstance(new_lang_files, basestring):
            new_lang_files = [new_lang_files]
        # remove empties
        return [lf for lf in new_lang_files if lf]
    return []


def parse_template(path):
    """Look through a template for the lang_files tag and extract the
    given lang files"""

    src = codecs.open(path, encoding='utf-8').read()
    tokens = Environment().lex(src)
    lang_files = []

    def ignore_whitespace(tokens):
        token = tokens.next()
        if token[1] == 'whitespace':
            return ignore_whitespace(tokens)
        return token

    for token in tokens:
        if token[1] == 'block_begin':
            block = ignore_whitespace(tokens)

            if block[1] == 'name' and block[2] in ('set_lang_files',
                                                   'add_lang_files'):
                arg = ignore_whitespace(tokens)

                # Extract all the arguments
                while arg[1] != 'block_end':
                    lang_files.append(arg[2].strip('"'))
                    arg = ignore_whitespace(tokens)

                # remove empties
                lang_files = [lf for lf in lang_files if lf]
                if lang_files:
                    return lang_files
    return []


def template_is_active(path, lang):
    """Given a template path, determine if it should be active for a locale.

    It is active if either the template's lang file, or the lang file
    specified in the "set_lang_files" template tag has the active tag.

    :param path: relative path to the template.
    :param lang: language code
    :return: boolean
    """
    if settings.DEV:
        return True

    cache_key = 'template_active:{lang}:{path}'.format(lang=lang, path=path)
    is_active = cache.get(cache_key)
    if is_active is None:
        # try the quicker and more efficient check first
        is_active = lang_file_is_active(get_lang_path(path), lang)

        if not is_active:
            template = get_template(path)
            lang_files = parse_template(template.filename)
            is_active = lang_files and lang_file_is_active(lang_files[0], lang)

        cache.set(cache_key, is_active, settings.DOTLANG_CACHE)

    return is_active


def langfiles_for_path(path):
    """
    Find and return any extra lang files specified in templates or python
    source files, or the first entry in the DOTLANG_FILES setting if none.

    :param path: path to a file containing strings to translate
    :return: list of langfile names.
    """
    lang_files = None

    if is_template(path):
        # If the template explicitly specifies lang files, use those
        lang_files = parse_template(join(settings.ROOT, path))
        # Otherwise, normalize the path name to a lang file
        if not lang_files:
            lang_files = [get_lang_path(path)]
    elif is_python(path):
        # If the python file explicitly specifies lang files, use those
        lang_files = parse_python(join(settings.ROOT, path))

    if not lang_files:
        # All other sources use the first main file
        lang_files = settings.DOTLANG_FILES[:1]

    return lang_files


def pot_to_langfiles():
    """Update the lang files in /locale/templates with extracted
    strings."""

    all_msgs = po_msgs()
    root = 'templates'

    # Start off with some global lang files so that strings don't
    # get duplicated everywhere
    main_msgs = {}
    for default_file in settings.DOTLANG_FILES:
        main_msgs.update(parse_lang(lang_file(default_file + '.lang', root),
                                    skip_untranslated=False))

    # Walk through the msgs and put them in the appropriate place. The
    # complex part about this is that templates and python files can
    # specify a list of lang files to pull from, so we need to check
    # all of them for the strings and add it to the first lang file
    # specified if not found.
    for path, msgs in all_msgs.items():
        lang_files = [lang_file('%s.lang' % f, root)
                      for f in langfiles_for_path(path)]

        # Get the current translations
        curr = {}
        for f in lang_files:
            curr.update(parse_lang(f, skip_untranslated=False))

        # Filter out the already translated
        new_msgs = [msg for msg in msgs
                    if msg[1] not in curr and msg[1] not in main_msgs]

        if new_msgs:
            # Add translations to the first lang file
            target = lang_files[0]

            _append_to_lang_file(target, new_msgs)


def find_lang_files(lang):
    for root, dirs, files in os.walk(lang_file(lang, '')):
        parts = root.split('locale/%s/' % lang)
        if len(parts) > 1:
            base = parts[1]
        else:
            base = ''

        for filename in files:
            name, ext = os.path.splitext(filename)

            if ext == '.lang':
                yield os.path.join(base, filename)


def merge_lang_files(langs):
    for lang in langs:
        print 'Merging into %s...' % lang

        for f in find_lang_files('templates'):
            # Make sure the directory exists (might be a subdirectory)
            d = os.path.dirname(f)
            if d:
                d = lang_file(d, lang)
                if not os.path.exists(d):
                    os.makedirs(d)

            dest = lang_file(f, lang)
            src_msgs = parse_lang(lang_file(f, 'templates'),
                                  skip_untranslated=False,
                                  extract_comments=True)
            dest_msgs = parse_lang(dest, skip_untranslated=False)
            new_msgs = [src_msgs[msg] for msg in src_msgs if msg not in dest_msgs]

            _append_to_lang_file(dest, new_msgs)


def _append_to_lang_file(dest, new_msgs):
    # make sure directory exists
    if not os.path.exists(dest):
        d = os.path.dirname(dest)
        if not os.path.exists(d):
            os.makedirs(d)

    with codecs.open(dest, 'a', 'utf-8') as out:
        for msg in new_msgs:
            if isinstance(msg, basestring):
                msg = [None, msg]
            out_str = u'\n\n'
            if msg[0]:
                out_str += u'# {comment}\n'
            out_str += u';{msg}\n{msg}\n'
            out.write(out_str.format(msg=msg[1], comment=msg[0]))
