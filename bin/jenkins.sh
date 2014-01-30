#!/bin/sh
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This script makes sure that Jenkins can properly run your tests against your
# codebase.
set -e

if [ -z $WORKSPACE ] ; then
  WORKSPACE=`/bin/pwd`
fi

cd $WORKSPACE
VENV=$WORKSPACE/venv

DB_HOST="localhost"
DB_USER="hudson"

echo "Starting build on executor $EXECUTOR_NUMBER..."

# Make sure there's no old pyc files around.
find . -name '*.pyc' -exec rm {} \;

if [ ! -d "$VENV/bin" ]; then
  echo "No virtualenv found.  Making one..."
  virtualenv $VENV --no-site-packages
  . $VENV/bin/activate
  pip install --upgrade pip
  pip install coverage
fi

git submodule sync -q
git submodule update --init --recursive

if [ ! -d "$WORKSPACE/vendor" ]; then
    echo "No /vendor... crap."
    exit 1
fi

. $VENV/bin/activate
pip install -q -r requirements/compiled.txt
pip install -q -r requirements/dev.txt

cat > bedrock/settings/local.py <<SETTINGS
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
        'HOST': '${DB_HOST}',
        'NAME': '${JOB_NAME}',
        'USER': 'hudson',
        'PASSWORD': '',
        'OPTIONS': {'init_command': 'SET storage_engine=InnoDB'},
        'TEST_NAME': 'test_${JOB_NAME}',
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
NOSE_ARGS = ['--with-xunit']

SETTINGS

echo "Creating database if we need it..."
echo "CREATE DATABASE IF NOT EXISTS \`${JOB_NAME}\`"|mysql -u $DB_USER -h $DB_HOST

echo "Update product_details"
python manage.py update_product_details

echo "collectstatic to workaround a jingo-minify bug"
python manage.py collectstatic --clear --no-default-ignore --noinput --verbosity=0

echo "Check PEP-8"
flake8 bedrock lib

echo "Starting tests..."
export FORCE_DB=1
coverage run manage.py test --noinput
coverage xml $(find bedrock lib -name '*.py')

echo "FIN"
