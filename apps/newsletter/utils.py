from basket.base import request
from django.core.cache import cache

import basket


def get_newsletters():
    """Return a dictionary with our information about newsletters.
    Keys are the internal keys we use to designate newsletters to basket.
    Values are dictionaries with the remaining newsletter information.
    """

    # Get the newsletter data from basket - it's a dictionary of dictionaries
    # Cache it for a little while (300 secs = 5 minutes)
    key = 'newsletter_data'
    data = cache.get(key)
    if data is None:
        data = basket.get_newsletters()
        cache.set(key, data, 300)
    return data


def custom_unsub_reason(token, reason):
    """Call basket. Pass along their reason for unsubscribing.

    This is calling a basket API that's custom to Mozilla, that's
    why there's not a helper in the basket-client package."""
    data = {
        'token': token,
        'reason': reason,
    }
    return request('post', 'custom_unsub_reason', data=data)
