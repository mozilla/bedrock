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

cat docker/docker-compose.yml | envsubst > ./docker-compose.yml

DOCKER_COMPOSE="docker-compose --project-name jenkins${JOB_NAME}${BUILD_NUMBER}"
# Start the database and give it some time to boot up
# TODO Uncomment when unit tests can run without locales.
## $DOCKER_COMPOSE up -d db
## sleep 10s;
## $DOCKER_COMPOSE run -T web ./manage.py test

# Cleanup
$DOCKER_COMPOSE stop
rm -rf $TDIR
