#!/bin/bash
# Needs DOCKER_REPOSITORY and FROM_DOCKER_REPOSITORY
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#
set -xe

# Used to trigger downstream Jenkins jobs
TRIGGER_FILE=.docker-updated
rm -rf $TRIGGER_FILE

if [[ $BUILD_CAUSE == "TIMERTRIGGER" ]]
then
    SVN_STATUS=`svn status -uq locale | wc -l`
    if [[ $SVN_STATUS == "0" ]]
    then
        # No updates, just exit
        echo "No locale updates"
        exit 0;
    else
        # Set GIT_COMMIT to the current deployed to prod commit
        COMMIT_URL=${COMMIT_URL:-https://www.mozilla.org/static/revision.txt}
        GIT_COMMIT=`curl  $COMMIT_URL 2> /dev/null`
    fi
fi

DOCKER_IMAGE_TAG=${DOCKER_REPOSITORY}:${GIT_COMMIT}

touch $TRIGGER_FILE

set +e
svn cleanup locale
set -e
svn co http://svn.mozilla.org/projects/mozilla.com/trunk/locales/ locale


cat docker/dockerfiles/bedrock_l10n | envsubst > ./locale/Dockerfile
echo ".svn" > ./locale/.dockerignore

docker build -f locale/Dockerfile -t $DOCKER_IMAGE_TAG locale
