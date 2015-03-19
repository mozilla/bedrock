#!/bin/sh
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This script makes sure that Jenkins can properly run your tests against your
# codebase.
set -ex

cd /app
apt-get update
apt-get install -y libmysqlclient-dev libxml2-dev libxslt1-dev python-dev subversion


# Make sure there's no old pyc files around.
find . -name '*.pyc' -exec rm {} \;

git submodule sync -q
git submodule update --init --recursive

if [ -d "$WORKSPACE/locale" ]; then
    svn up locale
else
    svn checkout https://svn.mozilla.org/projects/mozilla.com/trunk/locales/ locale
fi

pip install -q -r requirements/dev.txt

#TODO: get mysql working in new jenkins
#echo "Creating database if we need it..."
#echo "CREATE DATABASE IF NOT EXISTS \`${JOB_NAME}\`"|mysql -u $DB_USER -h $DB_HOST

echo Django version
python manage.py version

python manage.py syncdb --noinput --migrate

echo collectstatic
python manage.py collectstatic --noinput -v 0

echo "Update product_details"
python manage.py update_product_details

echo "Check PEP-8"
flake8 bedrock lib

echo "Starting tests..."
export FORCE_DB=1
coverage run manage.py test --noinput
coverage xml $(find bedrock lib -name '*.py')

echo "FIN"
