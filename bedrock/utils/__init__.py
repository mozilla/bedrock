# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings


def expand_locale_groups(locales):
    """
    Take a list of locales and locale prefixes (groups) and expand it to a full list of locales.

    :param locales: list of locale strings
    :return: list of locale strings
    """
    all_locales = []
    for locale in locales:
        if locale in settings.LANG_GROUPS:
            all_locales.extend(settings.LANG_GROUPS[locale])
        else:
            all_locales.append(locale)

    return all_locales
