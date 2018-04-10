import basket

from bedrock.newsletter.models import Newsletter


def get_newsletters():
    """Return a dictionary with our information about newsletters.
    Keys are the internal keys we use to designate newsletters to basket.
    Values are dictionaries with the remaining newsletter information.
    """
    return Newsletter.objects.serialize()


def get_languages_for_newsletters(newsletters=None):
    """Return a set of language codes supported by the newsletters.

    If no newsletters are provided, it will return language codes
    supported by all newsletters.
    """
    all_newsletters = get_newsletters()
    if newsletters is None:
        newsletters = all_newsletters.values()
    else:
        if isinstance(newsletters, basestring):
            newsletters = [nl.strip() for nl in newsletters.split(',')]
        newsletters = [all_newsletters.get(nl, {}) for nl in newsletters]

    langs = set()
    for newsletter in newsletters:
        langs.update(newsletter.get('languages', []))

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
