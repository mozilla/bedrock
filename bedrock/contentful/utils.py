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
    default_locale_count = ContentfulEntry.objects.filter(
        content_type=content_type,
        classification=classification,
        locale=default_locale,
    ).count()

    active_locales = set()

    if default_locale_count > 0:
        active_locales.add(default_locale)
    else:
        return []

    other_locales = (
        ContentfulEntry.objects.filter(
            content_type=content_type,
            classification=classification,
        )
        .exclude(locale=default_locale)
        .values_list("locale", flat=True)
    )
    other_locale_counts = defaultdict(int)
    for locale in other_locales:
        other_locale_counts[locale] += 1
    print("other_locale_counts", other_locale_counts)
    for locale, count in other_locale_counts.items():
        relative_pc = (count / default_locale_count) * 100
        if relative_pc >= settings.CONTENTFUL_LOCALE_ACTIVATION_PERCENTAGE:
            active_locales.add(locale)

    return sorted(active_locales)
