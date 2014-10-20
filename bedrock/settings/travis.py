# flake8: noqa

import logging


ROOT_URLCONF = 'bedrock.urls'
LOG_LEVEL = logging.ERROR

ADMINS = ('thedude@example.com',)
MANAGERS = ADMINS

# Database name has to be set because of sphinx
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bedrock_test',
        'USER': 'travis',
        'OPTIONS': {'init_command': 'SET storage_engine=InnoDB'},
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    }
}

HMAC_KEYS = {
    '2013-01-01': 'prositneujahr',
}

# TEMPLATE_DEBUG has to be True for jingo to call the template_rendered
# signal which Django's test client uses to save away the contexts for your
# test to look at later.
TEMPLATE_DEBUG = True
