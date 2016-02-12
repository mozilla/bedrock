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

# Push to docker hub
docker push $DOCKER_REPOSITORY:$COMMIT

GIT_TAG="$(git describe --tags --exact-match $GIT_COMMIT 2> /dev/null)"
if [[ ! -z $GIT_TAG ]]; then
    # tag and push docker image with git tag
    docker tag -f $FROM_DOCKER_REPOSITORY:$COMMIT $DOCKER_REPOSITORY:$GIT_TAG
    docker push $DOCKER_REPOSITORY:$GIT_TAG

    # tag and push docker image with "latest"
    docker tag -f $FROM_DOCKER_REPOSITORY:$COMMIT $DOCKER_REPOSITORY:latest
    docker push $DOCKER_REPOSITORY:latest

    # tag and push base image with latest
    BASE_IMAGE="$(docker run mozorg/bedrock bash -c "head -n 1 Dockerfile" | sed "s/FROM //")"
    BASE_REPO="$(cut -d : -f 1 <<< $BASE_IMAGE)"
    docker tag -f $BASE_IMAGE $BASE_REPO:latest
    docker push $BASE_REPO:latest
fi;
