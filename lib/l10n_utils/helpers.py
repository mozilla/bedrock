# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jingo
import jinja2
from babel.core import Locale, UnknownLocaleError
from babel.dates import format_date

from django.conf import settings
from django.utils.translation import get_language

from dotlang import translate, lang_file_has_tag


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


@jingo.register.function
@jinja2.contextfunction
def lang_files(ctx, *files):
    """Add more lang files to the translation object"""
    # Filter out empty files
    install_lang_files(ctx)
    add_lang_files(ctx, [f for f in files
                         if f and f not in settings.DOTLANG_FILES])


# backward compatible for imports
_ = gettext


# Once tower is fixed and we only need to install the above `gettext` function
# into Jinja2 once, we should do it here. The call is simply:
# jingo.env.install_gettext_callables(gettext, gettext)

@jingo.register.filter
def js_escape(string):
    import json
    return json.dumps(string)[1:-1]


@jingo.register.function
@jinja2.contextfunction
def l10n_has_tag(ctx, tag, langfile=None):
    """Return boolean whether the given lang file has the given tag."""
    langfile = langfile or ctx.get('langfile')
    return lang_file_has_tag(langfile, tag=tag)


def current_locale():
    """
    Return the current Locale object (from Babel). Defaults to locale
    based on settings.LANGUAGE_CODE if locale does not exist.
    """
    try:
        return Locale.parse(get_language(), sep='-')
    except (UnknownLocaleError, ValueError):
        return Locale(*settings.LANGUAGE_CODE.split('-'))


@jingo.register.filter
def l10n_format_date(date, format='long'):
    """
    Formats a date according to the current locale. Wraps around
    babel.dates.format_date.
    """
    locale = current_locale()
    return format_date(date, locale=locale, format=format)
