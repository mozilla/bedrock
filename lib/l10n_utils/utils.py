# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from builtins import object
import re


class ContainsEverything(object):
    """An object whose instances will claim to contain anything."""
    def __contains__(self, item):
        return True


def strip_whitespace(message):
    """Collapses all whitespace into single spaces.

    Borrowed from Tower.
    """
    return re.compile(r'\s+', re.UNICODE).sub(' ', message).strip()
