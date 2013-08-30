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
import logging

ROOT_URLCONF = 'bedrock.urls'
LOG_LEVEL = logging.ERROR

ADMINS = ('foo@bar.com',)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    },
}

HMAC_KEYS = {
    '2013-01-01': 'prositneujahr',
}

# TEMPLATE_DEBUG has to be True for jingo to call the template_rendered
# signal which Django's test client uses to save away the contexts for your
# test to look at later.
TEMPLATE_DEBUG = True
SETTINGS

echo "Update product_details"
./manage.py update_product_details

echo "Check PEP-8"
flake8 bedrock

echo "Starting tests..."
export FORCE_DB=1
coverage run manage.py test --noinput --with-xunit
coverage xml $(find bedrock lib -name '*.py')

echo "FIN"
