# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from collections import defaultdict
from typing import List

from django.conf import settings

from bedrock.contentful.models import ContentfulEntry


def can_use_locale(
    content_type: str,
    classification: str,
    locale: str,
    default_locale: str = "en-US",
) -> bool:
    """Is there enough of this content type, of this classification,
    in the given locale, compared to the default locale to, for example,
    show a listing page of it?"""

    active_locales = get_active_locales(
        content_type,
        classification,
        default_locale,
    )
    return locale in active_locales


# TODO? Cache this
def get_active_locales(
    content_type: str,
    classification: str,
    default_locale: str = "en-US",
) -> List:
    """How many locales do we have 'enough' of to consider them an active locale?"""

    all_locales = ContentfulEntry.objects.filter(
        content_type=content_type,
        classification=classification,
    ).values_list("locale", flat=True)

    locale_counts = defaultdict(int)
    for locale in all_locales:
        locale_counts[locale] += 1

    default_locale_count = locale_counts.pop(default_locale, 0)
    active_locales = set()

    if default_locale_count > 0:
        active_locales.add(default_locale)
    else:
        # no default locale count, and also not possible to say the other
        # locales are more active relative to it, because of division by zero
        return []

    for locale, count in locale_counts.items():
        relative_pc = (count / default_locale_count) * 100
        if relative_pc >= settings.CONTENTFUL_LOCALE_ACTIVATION_PERCENTAGE:
            active_locales.add(locale)

    return sorted(active_locales)
