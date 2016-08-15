# flake8: noqa

import logging
import os

ROOT_URLCONF = 'bedrock.urls'
LOG_LEVEL = logging.ERROR

ADMINS = ('thedude@example.com',)
MANAGERS = ADMINS

JENKINS_JOB_NAME = os.getenv('JOB_NAME', 'bedrock')

# Database name has to be set because of sphinx
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'NAME': JENKINS_JOB_NAME,
        'USER': os.getenv('DB_USER'),
        'PASSWORD': '',
        'OPTIONS': {'init_command': 'SET storage_engine=InnoDB'},
        'TEST_NAME': 'test_' + JENKINS_JOB_NAME,
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    }
}

HMAC_KEYS = {
    '2013-01-01': 'prositneujahr',
}
