# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""This library parses dotlang files migrated over from the old PHP
system.

It caches them using the django caching library, but it could
potentially just use thread-local variables. Caching seems safer at
the expense of another caching layer."""

from django.core.cache import caches
from django.utils.functional import lazy

from jinja2 import Markup

cache = caches["l10n"]


def translate(text, files):
    """
    An almost no-op to avoid triggering the old l10n machinery.
    """
    return Markup(text)


def gettext(text, *args, **kwargs):
    """
    An almost no-op to avoid triggering the old l10n machinery.
    """
    return text


_lazy_proxy = lazy(gettext, str)


def gettext_lazy(*args, **kwargs):
    return _lazy_proxy(*args, **kwargs)


# backward compat
_ = gettext
_lazy = gettext_lazy
