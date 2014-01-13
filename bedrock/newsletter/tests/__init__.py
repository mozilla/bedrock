from mock import Mock

from bedrock.newsletter import utils


# patch basket client to never hit the network
# causes get_newsletters to use fallback newsletters
# in settings/newsletters.py
news_mock = Mock(side_effect=utils.basket.BasketException)
utils.basket.get_newsletters = news_mock

# Test data for newsletters
# In the format returned by utils.get_newsletters()
newsletters = {
    u'mozilla-and-you': {
        'title': "Firefox & You",
        'languages': ['en', 'fr', 'de', 'pt', 'ru'],
        'show': True,
        'description': 'Firefox and you',
        'order': 4,
    },
    u'firefox-tips': {
        'show': True,
        'title': 'Firefox Tips',
        'languages': ['en', 'fr', 'de', 'pt', 'ru'],
        'description': 'Firefox tips',
        'order': 2,
    },
    u'beta': {
        'show': False,
        'title': 'Beta News',
        'languages': ['en'],
        'description': 'Beta News',
        'order': 3,
    },
    u'join-mozilla': {
        'show': False,
        'title': 'Join Mozilla',
        'languages': ['en', 'es'],
        'description': 'Join Mozilla',
        'order': 1,
    },
}
