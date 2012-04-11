import codecs
import errno
import os
from os.path import join
from tempfile import mkstemp
import re
import shutil
import sys

from django.conf import settings

from dotlang import parse as parse_lang, get_lang_path

REGEX_URL = re.compile(r'.* (\S+/\S+\.[^:]+).*')

def parse_po(path):
    msgs = {}

    if not os.path.exists(path):
        return msgs

    with codecs.open(path, 'r', 'utf-8') as lines:
        def extract_content(s):
            # strip the first word and quotes
            return s[s.find(' ')+1:].strip('"')

        msgid = None
        mshpath = None

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
            else:
                msgid = None
                msgpath = None
                
    return msgs


def po_msgs():
    return parse_po(join(settings.ROOT,
                         'locale/templates/LC_MESSAGES/messages.pot'))


def translated_strings(file_):
    path = join(settings.ROOT, 'locale/templates', file_)
    trans = parse_lang(path).keys()
    return trans


def mkdirs(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise


def lang_file(name, lang):
    return join(settings.ROOT, 'locale', lang, name)


def extract_lang_files(langs):
    all_msgs = po_msgs()

    for lang in langs:
        print 'Merging into %s...' % lang
        main_msgs = parse_lang(lang_file('main.lang', lang))

        for path, msgs in all_msgs.items():
            file_ = lang_file(get_lang_path(path), lang)

            if os.path.exists(file_):
                curr = parse_lang(file_)
            else:
                curr = {}
                dir_ = os.path.dirname(file_)
                mkdirs(dir_)

            with codecs.open(file_, 'a', 'utf-8') as out:
                for msg in msgs:
                    if msg not in curr and msg not in main_msgs:
                        out.write(';%s\n%s\n\n\n' % (msg, msg))
