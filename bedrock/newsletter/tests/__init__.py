# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import Mock

from bedrock.newsletter import utils

# patch basket client to never hit the network
# causes get_newsletters to use fallback newsletters
# in settings/newsletters.py
news_mock = Mock(side_effect=utils.basket.BasketException)
utils.basket.get_newsletters = news_mock

# Test data for newsletters
# In the format returned by utils.get_newsletters()
newsletters = {
    "mozilla-and-you": {
        "active": True,
        "show": True,
        "title": "Firefox & You",
        "languages": ["en", "fr", "de", "pt", "ru"],
        "description": "Firefox and you",
        "order": 4,
    },
    "firefox-tips": {
        "active": True,
        "show": True,
        "title": "Firefox Tips",
        "languages": ["en", "fr", "de", "pt", "ru"],
        "description": "Firefox tips",
        "order": 2,
    },
    "beta": {
        "active": False,
        "show": False,
        "title": "Beta News",
        "languages": ["en"],
        "description": "Beta News",
        "order": 3,
    },
    "join-mozilla": {
        "active": True,
        "show": False,
        "title": "Join Mozilla",
        "languages": ["en", "es"],
        "description": "Join Mozilla",
        "order": 1,
    },
}
