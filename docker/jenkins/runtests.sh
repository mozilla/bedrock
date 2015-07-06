#!/bin/bash
#
# Runs unit_tests
#
set -ex

# Create a temporary virtualenv to install docker-compose
TDIR=`mktemp -d`
virtualenv $TDIR
. $TDIR/bin/activate
pip install docker-compose==1.2.0

# Pull locales, we probably need to move this elsewhere.
git submodule update --init --recursive

set +e
svn cleanup locale
set -e
svn co http://svn.mozilla.org/projects/mozilla.com/trunk/locales/ locale

DOCKER_COMPOSE="docker-compose --project-name jenkins${JOB_NAME}${BUILD_NUMBER} -f docker/docker-compose.yml"

$DOCKER_COMPOSE build

docker save `echo jenkins${JOB_NAME}${BUILD_NUMBER}| sed s/_//g`_web | sudo docker-squash -t `echo jenkins${JOB_NAME}${BUILD_NUMBER}| sed s/_//g`_web | docker load

# Does nothing atm.

# Delete virtualenv
rm -rf $TDIR
