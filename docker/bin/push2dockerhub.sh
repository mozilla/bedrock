#!/bin/bash
# Needs DOCKER_USERNAME, DOCKER_PASSWORD, DOCKER_REPOSITORY,
# FROM_DOCKER_REPOSITORY environment variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#
set -exo pipefail

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

if [[ "$FROM_DOCKER_REPOSITORY" == "mozorg/bedrock" ]]; then
    DOCKER_TAG="${BRANCH_AND_COMMIT}"
else
    DOCKER_TAG="${GIT_COMMIT}"
fi

# Push to docker hub
docker push $FROM_DOCKER_REPOSITORY:${DOCKER_TAG}

if [[ "$BRANCH_NAME" == "master" ]]; then
    docker tag $FROM_DOCKER_REPOSITORY:${DOCKER_TAG} $FROM_DOCKER_REPOSITORY:latest
    docker push $FROM_DOCKER_REPOSITORY:latest
fi

if [[ "$GIT_TAG_DATE_BASED" == true ]]; then
    docker tag $FROM_DOCKER_REPOSITORY:${DOCKER_TAG} $FROM_DOCKER_REPOSITORY:$GIT_TAG
    docker tag $FROM_DOCKER_REPOSITORY:${DOCKER_TAG} $FROM_DOCKER_REPOSITORY:prod-latest
    docker push $FROM_DOCKER_REPOSITORY:$GIT_TAG
    docker push $FROM_DOCKER_REPOSITORY:prod-latest
fi
