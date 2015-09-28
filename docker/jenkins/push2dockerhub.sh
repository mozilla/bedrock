#!/bin/bash
# Needs DOCKER_USERNAME, DOCKER_PASSWORD, DOCKER_REPOSITORY,
# FROM_DOCKER_REPOSITORY environment variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#
set -ex

docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD -e $DOCKER_USERNAME@example.com

# If pull request use $ghprbActualCommit otherwise use $GIT_COMMIT
COMMIT="${ghprbActualCommit:=$GIT_COMMIT}"

# Tag using git hash
docker tag -f $FROM_DOCKER_REPOSITORY:$COMMIT $DOCKER_REPOSITORY:$COMMIT
docker push $DOCKER_REPOSITORY:$COMMIT
