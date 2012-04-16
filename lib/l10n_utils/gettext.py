import codecs
import errno
import os
from os.path import join
from tempfile import mkstemp
import re
import shutil
import sys

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


def merge_lang_files(langs):
    all_msgs = po_msgs()

    for lang in langs:
        print 'Merging into %s...' % lang

        # Start off with some global lang files so that strings don't
        # get duplicated everywhere
        main_msgs = parse_lang(lang_file('main.lang', lang))
        main_msgs.update(parse_lang(lang_file('base.lang', lang)))
        main_msgs.update(parse_lang(lang_file('newsletter.lang', lang)))

        for path, msgs in all_msgs.items():
            target = None
            lang_files = None

            if is_template(path):
                # If the template explicitly specifies lang files, use those
                lang_files = [lang_file('%s.lang' % f, lang)
                              for f in parse_template(join(settings.ROOT, path))]
                # Otherwise, normalize the path name to a lang file
                if not lang_files:
                    lang_files = [lang_file(get_lang_path(path), lang)]
            else:
                # All other sources use the first main file
                lang_files = [lang_file('%s.lang' % settings.DOTLANG_FILES[0],
                                        lang)]

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
