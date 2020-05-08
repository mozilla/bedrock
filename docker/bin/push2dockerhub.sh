#!/bin/bash
set -exo pipefail

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

FROM_DOCKER_REPOSITORY="$1"

# Push to docker hub
docker push $FROM_DOCKER_REPOSITORY:${GIT_COMMIT}

if [[ "$BRANCH_NAME" == "master" ]]; then
    docker tag $FROM_DOCKER_REPOSITORY:${GIT_COMMIT} $FROM_DOCKER_REPOSITORY:latest
    docker push $FROM_DOCKER_REPOSITORY:latest
fi

if [[ "$BRANCH_NAME" == "prod" ]]; then
    docker tag $FROM_DOCKER_REPOSITORY:${GIT_COMMIT} $FROM_DOCKER_REPOSITORY:prod-latest
    docker push $FROM_DOCKER_REPOSITORY:prod-latest
fi

if [[ "$GIT_TAG_DATE_BASED" == true ]]; then
    docker tag $FROM_DOCKER_REPOSITORY:${GIT_COMMIT} $FROM_DOCKER_REPOSITORY:$GIT_TAG
    docker push $FROM_DOCKER_REPOSITORY:$GIT_TAG
fi
