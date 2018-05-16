# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import codecs
import os
import re


TAG_REGEX = re.compile(r"^## ([\w-]+) ##")
WS_REGEX = re.compile(r'\s+', re.UNICODE)


class ContainsEverything(object):
    """An object whose instances will claim to contain anything."""
    def __contains__(self, item):
        return True


def strip_whitespace(message):
    """Collapses all whitespace into single spaces.

    Borrowed from Tower.
    """
    return WS_REGEX.sub(' ', message).strip()


def mail_error(path, message):
    """Email managers when an error is detected"""
    from django.core import mail
    subject = '%s is corrupted' % path
    mail.mail_managers(subject, message)


def parse(path, skip_untranslated=True, extract_comments=False):
    """
    Parse a dotlang file and return a dict of translations.
    :param path: Absolute path to a lang file.
    :param skip_untranslated: Exclude strings for which the ID and translation
                              match.
    :param extract_comments: Extract one line comments from template if True
    :return: dict
    """
    trans = {}

    if not os.path.exists(path):
        return trans

    with codecs.open(path, 'r', 'utf-8', errors='replace') as lines:
        source = None
        comment = None

        for line in lines:
            l10n_tag = None
            if u'�' in line:
                mail_error(path, line)

            line = line.strip()
            if not line:
                continue

            if line[0] == '#':
                comment = line.lstrip('#').strip()
                continue

            if line[0] == ';':
                source = line[1:]
            elif source:
                for tag in ('{ok}', '{l10n-extra}'):
                    if line.lower().endswith(tag):
                        l10n_tag = tag.strip('{}')
                        line = line[:-len(tag)]
                line = line.strip()
                if skip_untranslated and source == line and l10n_tag != 'ok':
                    continue
                if extract_comments:
                    trans[source] = [comment, line]
                    comment = None
                else:
                    trans[source] = line

    return trans


def parse_tags(path):
    """Return a list of tags for a lang file path"""
    tag_set = set()
    try:
        with codecs.open(path, 'r', 'utf-8', errors='replace') as lines:
            for line in lines:
                # Filter out Byte order Mark
                line = line.replace(u'\ufeff', '')
                m = TAG_REGEX.match(line)
                if m:
                    tag_set.add(m.group(1))
                else:
                    # Stop at the first non-tag line.
                    break
    except IOError:
        pass

    return list(tag_set)
