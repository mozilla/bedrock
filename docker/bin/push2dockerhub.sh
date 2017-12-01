#!/bin/bash
# Needs DOCKER_USERNAME, DOCKER_PASSWORD, DOCKER_REPOSITORY,
# FROM_DOCKER_REPOSITORY environment variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#
set -ex

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD -e $DOCKER_USERNAME@example.com

if [[ "$FROM_DOCKER_REPOSITORY" == "mozorg/bedrock_l10n" ]]; then
    DOCKER_TAG="${BRANCH_NAME/\//-}-${GIT_COMMIT}"
else
    DOCKER_TAG="${GIT_COMMIT}"
fi

if [[ "$FROM_DOCKER_REPOSITORY" != "$DOCKER_REPOSITORY" ]]; then
    # Tag using git hash
    docker tag $FROM_DOCKER_REPOSITORY:${DOCKER_TAG} $DOCKER_REPOSITORY:${DOCKER_TAG}
fi

# Push to docker hub
docker push $DOCKER_REPOSITORY:${DOCKER_TAG}

if [[ "$GIT_TAG_DATE_BASED" == true ]]; then
    docker tag $FROM_DOCKER_REPOSITORY:${DOCKER_TAG} $DOCKER_REPOSITORY:$GIT_TAG
    docker push $DOCKER_REPOSITORY:$GIT_TAG
    docker tag $FROM_DOCKER_REPOSITORY:${DOCKER_TAG} $DOCKER_REPOSITORY:latest
    docker push $DOCKER_REPOSITORY:latest
fi;
