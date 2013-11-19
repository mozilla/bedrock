from hashlib import md5

from django.conf import settings
from django.core.cache import cache

import basket
import commonware.log

log = commonware.log.getLogger('b.newsletter')

NEWSLETTERS_CACHE_KEY = "newsletter-data"
NEWSLETTERS_CACHE_TIMEOUT = 3600  # 1 hour


def get_newsletters():
    """Return a dictionary with our information about newsletters.
    Keys are the internal keys we use to designate newsletters to basket.
    Values are dictionaries with the remaining newsletter information.

    If we cannot get through to basket, return a default set of newsletters
    from settings.DEFAULT_NEWSLETTERS
    """

    # Get the newsletter data from basket - it's a dictionary of dictionaries
    # Cache it for a little while (300 secs = 5 minutes)
    data = cache.get(NEWSLETTERS_CACHE_KEY)
    if data is None:
        try:
            data = basket.get_newsletters()
        except basket.BasketException:
            log.exception("Error getting newsletters from basket")
            return settings.DEFAULT_NEWSLETTERS
        # Cache for an hour - newsletters very rarely change
        cache.set(NEWSLETTERS_CACHE_KEY, data, NEWSLETTERS_CACHE_TIMEOUT)
    return data


def get_languages_for_newsletters(newsletters=None):
    """Return a set of language codes supported by the newsletters.

    If no newsletters are provided, it will return language codes
    supported by all newsletters.

    These are 2-letter language codes and `do not` include the country part,
    even if the newsletter languages list does.  E.g. this returns 'pt',
    not 'pt-Br'
    """
    cache_key = 'newsletter:languages:' + md5(repr(newsletters)).hexdigest()

    langs = cache.get(cache_key)
    if langs is None:
        all_newsletters = get_newsletters()
        if newsletters is None:
            newsletters = all_newsletters.values()
        else:
            if isinstance(newsletters, basestring):
                newsletters = [nl.strip() for nl in newsletters.split(',')]
            newsletters = [all_newsletters.get(nl, {}) for nl in newsletters]

        langs = set()
        for newsletter in newsletters:
            langs.update(lang[:2].lower() for lang in newsletter.get('languages', []))

        cache.set(cache_key, langs, NEWSLETTERS_CACHE_TIMEOUT)

    return langs


def custom_unsub_reason(token, reason):
    """Call basket. Pass along their reason for unsubscribing.

    This is calling a basket API that's custom to Mozilla, that's
    why there's not a helper in the basket-client package."""
    data = {
        'token': token,
        'reason': reason,
    }
    return basket.request('post', 'custom_unsub_reason', data=data)
