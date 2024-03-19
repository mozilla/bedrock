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


def _fix_case(lang_code):
    """Convert lowercase language code to uppercase: en-us -> en-US

    Note: this is less exhaustive than bedrock.base.i18n.normalize_language
    because we don't want it to potentially fall back to to a two-char lang code.

    Indeed, because we have normalize_language running earlier in the
    request-response cycle the odds of getting a bad lang code are likely
    zero, so our default for more complex locale codes (e.g. zh-Hant-TW) is
    to leave them untouched. If this proves unreliable, we can merge this with
    normalize_locales and add a do-not-fall-back option to that function
    """

    if not lang_code:
        return None
    parts = lang_code.split("-")

    if len(parts) == 1:
        return lang_code
    if len(parts) > 2 or len(parts[1]) != 2:
        # Don't touch complex codes
        return lang_code
    else:
        return f"{parts[0].lower()}-{parts[1].upper()}"


def get_language():
    lang = _fix_case(translation.get_language())
    return lang or settings.LANGUAGE_CODE


def get_language_bidi():
    return translation.get_language_bidi()
