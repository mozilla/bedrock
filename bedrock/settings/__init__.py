# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
import sys

from .base import *  # noqa

if os.getenv('TRAVIS', False):
    from .travis import *  # noqa

elif os.getenv('JENKINS_HOME', False):
    from .jenkins import *  # noqa

else:
    if os.getenv('C9_USER'):
        from .c9 import *  # noqa
    try:
        from .local import *  # noqa
    except ImportError as exc:
        'local.py is supported, but no longer necessary'


if DEV:
    ALLOWED_HOSTS = ['*']
else:
    MIDDLEWARE_CLASSES += ('commonware.middleware.FrameOptionsHeader',)


# waffle flags, switches, and samples should default to True in DEV mode
WAFFLE_FLAG_DEFAULT = WAFFLE_SWITCH_DEFAULT = WAFFLE_SAMPLE_DEFAULT = DEV

# Any databases configured other than "default" should be
# read-only slaves, which our default router
# should use with this setting.
if 'manage.py' not in sys.argv:
    SLAVE_DATABASES = [db for db in DATABASES if db != 'default']

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

if (len(sys.argv) > 1 and sys.argv[1] == 'test') or sys.argv[0].endswith('py.test'):
    # Using the CachedStaticFilesStorage for tests breaks all the things.
    STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
    # Turn off less compilation in tests
    PIPELINE_ENABLED = True
    # TEMPLATE_DEBUG has to be True for jingo to call the template_rendered
    # signal which Django's test client uses to save away the contexts for your
    # test to look at later.
    TEMPLATE_DEBUG = True
    # don't cache product-details
    CACHES['product-details']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
    # use default product-details data
    PROD_DETAILS_STORAGE = 'product_details.storage.PDFileStorage'
