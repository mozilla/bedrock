from django.conf import settings
from django.core.cache import cache

import basket
import commonware.log

log = commonware.log.getLogger('b.newsletter')

NEWSLETTERS_CACHE_KEY = "newsletter-data"
NEWSLETTER_LANGUAGES_CACHE_KEY = "newsletter-languages"


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
        cache.set(NEWSLETTERS_CACHE_KEY, data, 3600)
        cache.delete(NEWSLETTER_LANGUAGES_CACHE_KEY)
    return data


def get_newsletter_languages():
    """Return a set of the language codes supported by our newsletters.
    Any language supported by any newletter is included.

    These are 2-letter language codes and `do not` include the country part,
    even if the newsletter languages list does.  E.g. this returns 'pt',
    not 'pt-Br'
    """
    # Cache this for a little while.  get_newsletters() will invalidate our
    # cache if the newsletters change.
    langs = cache.get(NEWSLETTER_LANGUAGES_CACHE_KEY)
    if langs is None:
        langs = set()
        for newsletter in get_newsletters().values():
            langs.update(locale[:2] for locale in newsletter.get('languages', []))
        # Long cache okay; get_newsletters() invalidates our cache if the
        # newsletters change
        cache.set(NEWSLETTER_LANGUAGES_CACHE_KEY, langs, 3600 * 24 * 7)
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


def clear_caches():
    # Just for testing
    cache.delete(NEWSLETTERS_CACHE_KEY)
    cache.delete(NEWSLETTER_LANGUAGES_CACHE_KEY)
