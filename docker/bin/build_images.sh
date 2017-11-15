#!/bin/bash

set -exo pipefail

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

DOCKER_IMAGE_TAG="mozorg/bedrock:${BRANCH_NAME/\//-}-${GIT_COMMIT}"
TEST_IMAGE_TAG="mozorg/bedrock_test:${GIT_COMMIT}"
DOCKER_REBUILD=false
# test mode will build the unit testing image containing the testing requirements
TEST_MODE=false

# parse cli args
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -r|--rebuild)
            DOCKER_REBUILD=true
            ;;
        -t|--test)
            TEST_MODE=true
            ;;
    esac
    shift # past argument or value
done

function imageExists() {
    if $DOCKER_REBUILD; then
        return 1
    fi
    if [[ "$1" == "main" ]]; then
        DOCKER_TAG="${DOCKER_IMAGE_TAG}"
    else
        DOCKER_TAG="${TEST_IMAGE_TAG}"
    fi
    docker history -q "${DOCKER_TAG}" > /dev/null 2>&1
    return $?
}

if ! imageExists "main"; then
    docker build -t "${DOCKER_IMAGE_TAG}" --pull \
           --build-arg "GIT_SHA=${GIT_COMMIT}" \
           --build-arg "BRANCH_NAME=${BRANCH_NAME}" .
fi

# build a tester image for non-demo deploys
if $TEST_MODE && ! imageExists "test"; then
    docker build -t "${TEST_IMAGE_TAG}" \
           --build-arg "FROM_TAG=${DOCKER_IMAGE_TAG}" \
           -f Dockerfile.test .
fi
