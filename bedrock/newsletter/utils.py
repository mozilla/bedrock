# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.core.cache import cache

import basket

from bedrock.newsletter.models import Newsletter


def get_newsletters():
    """Return a dictionary with our information about newsletters.
    Keys are the internal keys we use to designate newsletters to basket.
    Values are dictionaries with the remaining newsletter information.
    """
    _key = "serialized_newsletters"
    serialized_newsletters = cache.get(_key)
    if serialized_newsletters is None:
        serialized_newsletters = Newsletter.objects.serialize()
        cache.set(_key, serialized_newsletters, timeout=settings.CACHE_TIME_LONG)
    return serialized_newsletters


def get_languages_for_newsletters(newsletters=None):
    """Return a set of language codes supported by the newsletters.

    If no newsletters are provided, it will return language codes
    supported by all newsletters.
    """
    all_newsletters = get_newsletters()
    if newsletters is None:
        newsletters = list(all_newsletters.values())
    else:
        if isinstance(newsletters, str):
            newsletters = [nl.strip() for nl in newsletters.split(",")]
        newsletters = [all_newsletters.get(nl, {}) for nl in newsletters]

    langs = set()
    for newsletter in newsletters:
        langs.update(newsletter.get("languages", []))

    return langs


def custom_unsub_reason(token, reason):
    """Call basket. Pass along their reason for unsubscribing.

    This is calling a basket API that's custom to Mozilla, that's
    why there's not a helper in the basket-client package."""
    data = {
        "token": token,
        "reason": reason,
    }
    return basket.request("post", "custom_unsub_reason", data=data)
