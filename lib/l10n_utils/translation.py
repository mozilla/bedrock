# mimic django's language activation machinery. it checks for .mo files
# and we don't need anything nearly as complex.

from _threading_local import local

from django.conf import settings


_active = local()


def activate(language):
    """
    Installs the given language as the language for the current thread.
    """
    _active.value = language


def deactivate():
    """
    Uninstalls the currently active language so that further _ calls
    will resolve against the default language, again.
    """
    if hasattr(_active, "value"):
        del _active.value


def _fix_case(locale):
    """Convert lowercase locales to uppercase: en-us -> en-US"""
    parts = locale.split('-')
    if len(parts) == 1:
        return locale
    else:
        return '%s-%s' % (parts[0], parts[1].upper())


def get_language(fix_case=False):
    """Returns the currently selected language."""
    lang = getattr(_active, "value", None)
    if lang is None:
        return settings.LANGUAGE_CODE

    if fix_case:
        lang = _fix_case(lang)

    return lang


def get_language_bidi():
    """
    Returns selected language's BiDi layout.

    * False = left-to-right layout
    * True = right-to-left layout
    """
    base_lang = get_language().split('-')[0]
    return base_lang in settings.LANGUAGES_BIDI
