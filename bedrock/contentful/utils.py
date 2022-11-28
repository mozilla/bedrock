# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from collections import defaultdict
from typing import List

from django.conf import settings

from bedrock.contentful.models import ContentfulEntry


# TODO? Cache this
def locales_with_available_content(
    content_type: str,
    classification: str,
    default_locale: str = "en-US",
) -> List[str]:
    """
    Returns a list of locale names for which we have 'enough' content in that
    locale to merit showing a listing page.

    Why? We don't want a resource center with only one article available in it;
    better to wait a few days till translations for the rest of the content
    lands in Bedrock.

    Note that this is not about working how much of a _single_ Entry has been
    localised - it's focused on the number of localised Entries in each
    non-default locale compared to the number of entries in the default locale.
    """
    threshold_pc = settings.CONTENTFUL_LOCALE_SUFFICIENT_CONTENT_PERCENTAGE

    kwargs = dict(
        content_type=content_type,
        classification=classification,
        localisation_complete=True,
    )
    # Get all the locales _with at least one complete localisation each_
    all_locales = ContentfulEntry.objects.filter(**kwargs).values_list("locale", flat=True)

    # Build a Counter-like lookup table that simply tracks the total number of viable
    # (i.e. complete, localised) articles in each locale
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
        if relative_pc >= threshold_pc:
            active_locales.add(locale)

    return sorted(active_locales)
