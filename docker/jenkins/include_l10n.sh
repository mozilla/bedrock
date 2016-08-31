#!/bin/bash
# Needs DOCKER_REPOSITORY and FROM_DOCKER_REPOSITORY
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#
set -xe

# Used to trigger downstream Jenkins jobs
PARAM_FILE=.parameters
TRIGGER_FILE=.docker-updated
FORCE_TIME_TRIGGER_UPDATE=.timetriggerupdate
rm -rf $TRIGGER_FILE $PARAM_FILE

if [[ $BUILD_CAUSE == "REMOTECAUSE" ]]
then
    LATEST_TAG=$(git describe --abbrev=0 --tags)
    # parent (~0) of latest tag is the commit that was tagged
    GIT_COMMIT=$(git rev-parse ${LATEST_TAG}~0)
fi
echo "GIT_COMMIT=$GIT_COMMIT" >> $PARAM_FILE

DOCKER_IMAGE_TAG=${DOCKER_REPOSITORY}:${GIT_COMMIT}

touch $TRIGGER_FILE

if [[ ! -e locale ]];
then
    git clone --depth 1 https://github.com/mozilla-l10n/bedrock-l10n locale
fi;

pushd locale
git fetch origin
git checkout -f origin/master
popd

cat docker/dockerfiles/bedrock_l10n | envsubst > ./locale/Dockerfile
echo ".git" > ./locale/.dockerignore

docker build -f locale/Dockerfile -t $DOCKER_IMAGE_TAG locale
