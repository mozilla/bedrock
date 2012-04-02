import sys
import os
from os.path import join
import codecs

from django.conf import settings

from dotlang import parse as parse_lang


def parse_po(path):
    msgs = []

    if not os.path.exists(path):
        return msgs

    with codecs.open(path, 'r', 'utf-8') as lines:
        def extract_content(s):
            # strip the first word and quotes
            return s[s.find(' ')+1:].strip('"')

        msgid = None

        for line in lines:
            line = line.strip()
            if line.startswith('msgid'):
                msgid = extract_content(line)
            elif line.startswith('msgstr') and msgid:
                msgs.append(msgid)
            else:
                msgid = None
                
    return msgs


def po_msgs():
    return parse_po(join(settings.ROOT,
                         'locale/templates/LC_MESSAGES/messages.pot'))


def lang_translations():
    trans = []

    for f in settings.DOTLANG_FILES:
        path = join(settings.ROOT, 'locale/templates', f)
        trans.extend(parse_lang(path).keys())

    return trans


def extract_lang(output_file):
    lang_trans = lang_translations()
    
    if os.path.exists(output_file):
        res = False
        while res != 'y' and res != 'n':
            res = raw_input('Output file exists, overwite? [y/n]')
        if res == 'n':
            return
    
    with codecs.open(output_file, 'w', 'utf-8') as out:
        for msg in po_msgs():
            if msg not in lang_trans:
                out.write(";%s\n%s\n\n\n" % (msg, msg))
