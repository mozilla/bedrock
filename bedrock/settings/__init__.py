# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging.config
import sys

from .base import *  # noqa

try:
    from .local import *  # noqa
except ImportError as exc:
    'local.py is supported, but no longer necessary'


if DEV:
    ALLOWED_HOSTS = ['*']
else:
    MIDDLEWARE += ['commonware.middleware.FrameOptionsHeader']


if CACHES['default']['BACKEND'] == 'django_pylibmc.memcached.PyLibMCCache':
    CACHES['default']['BINARY'] = True
    CACHES['default']['OPTIONS'] = {  # Maps to pylibmc "behaviors"
        'tcp_nodelay': True,
        'ketama': True,
    }

# cache for lang files
CACHES['l10n'] = {
    'BACKEND': 'bedrock.base.cache.SimpleDictCache',
    'LOCATION': 'l10n',
    'TIMEOUT': DOTLANG_CACHE,
    'OPTIONS': {
        'MAX_ENTRIES': 5000,
        'CULL_FREQUENCY': 4,  # 1/4 entries deleted if max reached
    }
}

# cache for product details
CACHES['product-details'] = {
    'BACKEND': 'bedrock.base.cache.SimpleDictCache',
    'LOCATION': 'product-details',
    'OPTIONS': {
        'MAX_ENTRIES': 200,  # currently 104 json files
        'CULL_FREQUENCY': 4,  # 1/4 entries deleted if max reached
    }
}

# cache for release notes
CACHES['release-notes'] = {
    'BACKEND': 'bedrock.base.cache.SimpleDictCache',
    'LOCATION': 'release-notes',
    'TIMEOUT': 5,
    'OPTIONS': {
        'MAX_ENTRIES': 300,  # currently 564 json files but most are rarely accessed
        'CULL_FREQUENCY': 4,  # 1/4 entries deleted if max reached
    }
}

# cache for externalfiles
CACHES['externalfiles'] = {
    'BACKEND': 'bedrock.base.cache.SimpleDictCache',
    'LOCATION': 'externalfiles',
    'OPTIONS': {
        'MAX_ENTRIES': 10,  # currently 2 files
        'CULL_FREQUENCY': 4,  # 1/4 entries deleted if max reached
    }
}

MEDIA_URL = CDN_BASE_URL + MEDIA_URL
STATIC_URL = CDN_BASE_URL + STATIC_URL
logging.config.dictConfig(LOGGING)

if (len(sys.argv) > 1 and sys.argv[1] == 'test') or 'pytest' in sys.modules:
    # Using the CachedStaticFilesStorage for tests breaks all the things.
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    # TEMPLATE_DEBUG has to be True for Jinja to call the template_rendered
    # signal which Django's test client uses to save away the contexts for your
    # test to look at later.
    TEMPLATES[0]['OPTIONS']['debug'] = True
    # use default product-details data
    PROD_DETAILS_STORAGE = 'product_details.storage.PDFileStorage'

    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
