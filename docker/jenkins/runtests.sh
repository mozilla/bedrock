#!/bin/bash
#
# Runs unit_tests
#
# Needs DOCKER_REPOSITORY
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#
set -ex

# Create a temporary virtualenv to install docker-compose
TDIR=`mktemp -d`
virtualenv $TDIR
. $TDIR/bin/activate
pip install docker-compose==1.2.0

# Pull locales, we probably need to move this elsewhere.
git submodule update --init --recursive

DOCKER_COMPOSE="docker-compose --project-name jenkins${JOB_NAME}${BUILD_NUMBER} -f docker/docker-compose.yml"

$DOCKER_COMPOSE build

# Start the database and give it some time to boot up
$DOCKER_COMPOSE up -d db

docker save `echo jenkins${JOB_NAME}${BUILD_NUMBER}| sed s/_//g`_web | sudo docker-squash -t `echo jenkins${JOB_NAME}${BUILD_NUMBER}| sed s/_//g`_web | docker load


$DOCKER_COMPOSE run -T web ./manage.py test

# Cleanup
$DOCKER_COMPOSE stop
rm -rf $TDIR

# Tag docker image. This intentionally goes after cleanup to allow
# docker-compose to stop containers.
CURRENT_TAG=`echo jenkins${JOB_NAME}${BUILD_NUMBER}| sed s/_//g`_web
docker tag -f $CURRENT_TAG $DOCKER_REPOSITORY:$GIT_COMMIT
docker tag -f $CURRENT_TAG $DOCKER_REPOSITORY:latest
