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
from jinja2 import Environment

from dotlang import parse as parse_lang, get_lang_path


REGEX_URL = re.compile(r'.* (\S+/\S+\.[^:]+).*')


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

        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                matches = REGEX_URL.match(line)
                if matches:
                    msgpath = matches.group(1)
            elif line.startswith('msgid'):
                msgid = extract_content(line)
            elif line.startswith('msgstr') and msgid and msgpath:
                if msgpath not in msgs:
                    msgs[msgpath] = []
                msgs[msgpath].append(msgid)
                msgid = None
                msgpath = None
            elif msgid is not None:
                msgid += parse_string(line)

    return msgs


def po_msgs():
    return parse_po(join(settings.ROOT,
                         'locale/templates/LC_MESSAGES/messages.pot'))


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
        return new_lang_files
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

                lang_files = filter(lambda x: x, lang_files)
                if lang_files:
                    return lang_files
    return []


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
    main_msgs = parse_lang(lang_file('main.lang', root))
    main_msgs.update(parse_lang(lang_file('base.lang', root)))
    main_msgs.update(parse_lang(lang_file('newsletter.lang', root)))

    # Walk through the msgs and put them in the appropriate place. The
    # complex part about this is that templates and python files can
    # specify a list of lang files to pull from, so we need to check
    # all of them for the strings and add it to the first lang file
    # specified if not found.
    for path, msgs in all_msgs.items():
        target = None
        lang_files = [lang_file('%s.lang' % f, root)
                      for f in langfiles_for_path(path)]

        # Get the current translations
        curr = {}
        for f in lang_files:
            if os.path.exists(f):
                curr.update(parse_lang(f))

        # Add translations to the first lang file
        target = lang_files[0]

        if not os.path.exists(target):
            d = os.path.dirname(target)
            if not os.path.exists(d):
                os.makedirs(d)

        with codecs.open(target, 'a', 'utf-8') as out:
            for msg in msgs:
                if msg not in curr and msg not in main_msgs:
                    out.write(';%s\n%s\n\n\n' % (msg, msg))


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
            src_msgs = parse_lang(lang_file(f, 'templates'))
            dest_msgs = parse_lang(dest)

            with codecs.open(dest, 'a', 'utf-8') as out:
                for msg in src_msgs:
                    if msg not in dest_msgs:
                        out.write('\n\n;%s\n%s\n' % (msg, msg))
