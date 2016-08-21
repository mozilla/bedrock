# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jinja2
from babel.core import Locale, UnknownLocaleError
from babel.dates import format_date
from babel.numbers import format_number
from django_jinja import library

from django.conf import settings

from lib.l10n_utils.dotlang import lang_file_has_tag, translate
from lib.l10n_utils.gettext import template_has_tag
from lib.l10n_utils.translation import get_language


babel_format_locale_map = {
    'hsb': 'de',
    'dsb': 'de',
}


def install_lang_files(ctx):
    """Install the initial set of .lang files"""
    req = ctx['request']

    if not hasattr(req, 'langfiles'):
        files = list(settings.DOTLANG_FILES)
        langfile = ctx.get('langfile')
        if langfile:
            files.insert(0, langfile)
        req.langfiles = files


def add_lang_files(ctx, files):
    """Install additional .lang files"""
    req = ctx['request']

    if hasattr(req, 'langfiles'):
        req.langfiles = files + req.langfiles


# TODO: make an ngettext compatible function. The pluaralize clause of a
#       trans block won't work untill we do.
@jinja2.contextfunction
def gettext(ctx, text):
    """Translate a string, loading the translations for the locale if
    necessary."""
    install_lang_files(ctx)
    return translate(text, ctx['request'].langfiles)


@library.global_function
@jinja2.contextfunction
def lang_files(ctx, *files):
    """Add more lang files to the translation object"""
    # Filter out empty files
    install_lang_files(ctx)
    add_lang_files(ctx, [f for f in files
                         if f and f not in settings.DOTLANG_FILES])


# backward compatible for imports
_ = gettext


@library.filter
def js_escape(string):
    import json
    return json.dumps(string)[1:-1].replace('&nbsp;', '\\u00A0')


@library.global_function
@jinja2.contextfunction
def l10n_has_tag(ctx, tag, langfile=None):
    """Return boolean whether the given template's lang files have the given tag."""
    if langfile:
        return lang_file_has_tag(langfile, ctx['LANG'], tag)
    else:
        return template_has_tag(ctx['template'], ctx['LANG'], tag)


def get_locale(lang):
    """Return a babel Locale object for lang. defaults to LANGUAGE_CODE."""
    lang = babel_format_locale_map.get(lang) or lang
    try:
        return Locale.parse(lang, sep='-')
    except (UnknownLocaleError, ValueError):
        return Locale(*settings.LANGUAGE_CODE.split('-'))


def current_locale():
    """
    Return the current Locale object (from Babel). Defaults to locale
    based on settings.LANGUAGE_CODE if locale does not exist.
    """
    return get_locale(get_language())


@library.filter
@jinja2.contextfilter
def l10n_format_date(ctx, date, format='long'):
    """
    Formats a date according to the current locale. Wraps around
    babel.dates.format_date.
    """
    lang = get_locale(ctx['LANG'])
    return format_date(date, locale=lang, format=format)


@library.filter
@jinja2.contextfilter
def l10n_format_number(ctx, number):
    """
    Formats a number according to the current locale. Wraps around
    babel.numbers.format_number.
    """
    lang = get_locale(ctx['LANG'])
    return format_number(number, locale=lang)
