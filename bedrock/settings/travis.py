# flake8: noqa

import logging


ROOT_URLCONF = 'bedrock.urls'
LOG_LEVEL = logging.ERROR

# need these for some email tests apparently
ADMINS = ('thedude@example.com',)
MANAGERS = ADMINS

HMAC_KEYS = {
    '2013-01-01': 'prositneujahr',
}

PROD_DETAILS_STORAGE = 'product_details.storage.PDFileStorage'
