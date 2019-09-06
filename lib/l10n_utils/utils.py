# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
import re

from django.conf import settings

from fluent.runtime import FluentResourceLoader
from fluent.syntax.ast import Message


FTL_LOADER = FluentResourceLoader(f'{settings.FLUENT_LOCAL_PATH}/{{locale}}/')
COMMENT_RE = re.compile(r'LANG_ID_HASH: (\w{32})')


def get_ftl_file_data(filename):
    data = {}
    for resources in FTL_LOADER.resources('en', [filename]):
        for resource in resources:
            for item in resource.body:
                if isinstance(item, Message):
                    match = COMMENT_RE.search(item.comment.content)
                    if match:
                        data[match.group(1)] = item.id.name

    return data


class ContainsEverything:
    """An object whose instances will claim to contain anything."""
    def __contains__(self, item):
        return True


def strip_whitespace(message):
    """Collapses all whitespace into single spaces.

    Borrowed from Tower.
    """
    return re.compile(r'\s+', re.UNICODE).sub(' ', message).strip()


def get_l10n_path(path):
    """Generate the path to a lang file from a django path.
    /apps/foo/templates/foo/bar.html -> foo/bar
    /templates/foo.html -> foo
    /foo/bar.html -> foo/bar"""

    # filter empty path parts
    parts = [p for p in path.split('/') if p]

    try:
        i = parts.index('templates')
        parts = parts[i + 1:]
    except ValueError:
        pass

    path = '/'.join(parts)
    base, ext = os.path.splitext(path)
    return base
