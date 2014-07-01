# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import csv
from datetime import datetime
from functools import wraps
from operator import itemgetter

from django.conf import settings
from django.utils.http import parse_http_date_safe

from ordereddict import OrderedDict


_memoize_cache = {}


def _clear_cache():
    _memoize_cache.clear()


def memoize(f):
    """Cache the return value of a function taking no args."""
    @wraps(f)
    def wrapper():
        val = _memoize_cache.get(f.__name__, None)
        if val is None:
            val = _memoize_cache[f.__name__] = f()

        return val

    return wrapper


@memoize
def get_credits():
    """
    Returns an OrderedDict of sorted lists of names by first letter of sortkey.

    Gets data from the configured CSV file location in CREDITS_NAMES_FILE.

    Example:

    > get_credits()
    > {'D':['El Dudarino', 'The Dude'], 'S':['Walter Sobchak']}
    """
    try:
        with open(settings.CREDITS_NAMES_FILE, 'rb') as names_fh:
            return get_credits_ordered(names_fh)
    except IOError:
        return {}


def get_credits_list(credits_data):
    """
    Returns a list of lists sorted by the sortkey column.

    :param credits_data: any iterable of CSV formatted strings.
    :return: list of lists
    """
    names = []
    for row in csv.reader(credits_data):
        if len(row) == 1:
            name = sortkey = row[0]
        elif len(row) == 2:
            name, sortkey = row
        else:
            continue

        names.append([name.decode('utf8'), sortkey.upper()])

    return sorted(names, key=itemgetter(1))


def get_credits_ordered(credits_data):
    """
    Returns an OrderedDict of sorted lists of names by first letter of sortkey.

    :param credits_data: any iterable of CSV formatted strings.
    :return: OrderedDict
    """
    names = get_credits_list(credits_data)
    ordered_names = OrderedDict()
    for name, sortkey in names:
        letter = sortkey[0]
        if letter not in ordered_names:
            ordered_names[letter] = []

        ordered_names[letter].append(name)

    return ordered_names


@memoize
def get_credits_last_modified():
    """
    Return the last-modified header from the most recent names update.
    :return: str timestamp
    """
    try:
        with open(settings.CREDITS_NAMES_UPDATED_FILE) as lu_fh:
            return lu_fh.read().strip()
    except IOError:
        return None


@memoize
def get_credits_last_modified_datetime():
    """
    Return the last-modified header from the most recent names update as datetime.
    :return: datetime (or None on error)
    """
    date_str = get_credits_last_modified()
    if date_str:
        date_epoch = parse_http_date_safe(date_str)
        if date_epoch:
            return datetime.utcfromtimestamp(date_epoch)

    return None
