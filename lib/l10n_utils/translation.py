# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# mimic django's language activation machinery. it checks for .mo files
# and we don't need anything nearly as complex.

from django.conf import settings
from django.utils import translation


def activate(language):
    return translation.activate(language)


def deactivate():
    """
    Uninstalls the currently active language so that further _ calls
    will resolve against the default language, again.
    """
    return translation.deactivate()


def _fix_case(locale):
    """Convert lowercase locales to uppercase: en-us -> en-US

    Note: this is less exhaustive than bedrock.base.i18n.normalize_language
    because we don't want it to potentially fall back to to a lang prefix
    """
    parts = locale.split("-")
    if len(parts) == 1:
        return locale
    else:
        return f"{parts[0]}-{parts[1].upper()}"


def get_language():
    return _fix_case(translation.get_language())


def get_language_bidi():
    """
    Returns selected language's BiDi layout.

    * False = left-to-right layout
    * True = right-to-left layout
    """
    base_lang = get_language().split("-")[0]
    return base_lang in settings.LANGUAGES_BIDI
