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
    slug: str = None,
) -> List:
    """How many locales do we have 'enough' of to consider them an active locale?"""

    kwargs = dict(
        content_type=content_type,
        classification=classification,
    )
    if slug:
        kwargs["slug"] = slug

    all_locales = ContentfulEntry.objects.filter(**kwargs).values_list("locale", flat=True)

    if slug:
        # There's no need to check the proportion of entries in each locale, because we're
        # down to a very, very specific combination of slug + content_type + classification
        # so all results will match/be viable
        return list(all_locales)

    # Otherwise, we're looking at just entries of a particular content_type and classification
    # across any number of slugs, so we do need to see if there are enough to activate the locale
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
        if relative_pc >= settings.CONTENTFUL_LOCALE_SUFFICIENT_CONTENT_PERCENTAGE:
            active_locales.add(locale)

    return sorted(active_locales)
