# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

import jinja2
from babel.core import Locale, UnknownLocaleError
from babel.dates import format_date
from babel.numbers import format_number
from django_jinja import library

from lib.l10n_utils.translation import get_language

babel_format_locale_map = {
    "hsb": "de",
    "dsb": "de",
}


def get_locale(lang):
    """Return a babel Locale object for lang. defaults to LANGUAGE_CODE."""
    lang = babel_format_locale_map.get(lang) or lang
    try:
        return Locale.parse(lang, sep="-")
    except (UnknownLocaleError, ValueError):
        return Locale(*settings.LANGUAGE_CODE.split("-"))


def current_locale():
    """
    Return the current Locale object (from Babel). Defaults to locale
    based on settings.LANGUAGE_CODE if locale does not exist.
    """
    return get_locale(get_language())


@library.filter
@jinja2.contextfilter
def l10n_format_date(ctx, date, format="long"):
    """
    Formats a date according to the current locale. Wraps around
    babel.dates.format_date.
    """
    lang = get_locale(ctx["LANG"])
    return format_date(date, locale=lang, format=format)


@library.filter
@jinja2.contextfilter
def l10n_format_number(ctx, number):
    """
    Formats a number according to the current locale. Wraps around
    babel.numbers.format_number.
    """
    lang = get_locale(ctx["LANG"])
    return format_number(number, locale=lang)
