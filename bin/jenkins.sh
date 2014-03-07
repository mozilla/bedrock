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

export DB_HOST="localhost"
export DB_USER="hudson"

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

echo "Creating database if we need it..."
echo "CREATE DATABASE IF NOT EXISTS \`${JOB_NAME}\`"|mysql -u $DB_USER -h $DB_HOST

echo "Update product_details"
python manage.py update_product_details

echo "Check PEP-8"
flake8 bedrock lib

echo "Starting tests..."
export FORCE_DB=1
coverage run manage.py test --noinput
coverage xml $(find bedrock lib -name '*.py')

echo "FIN"
