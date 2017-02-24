#!/bin/bash

set -exo pipefail

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

DOCKER_REPO="${DOCKER_REPO:-mozorg}"
DOCKER_NO_CACHE=false
DOCKER_PULL=false
DOCKER_CTX='.'
DOCKERFILE='base'

# parse cli args
while [[ $# -gt 1 ]]; do
    key="$1"
    case $key in
        -c|--context)
            DOCKER_CTX="$2"
            shift
            ;;
        -n|--no-cache)
            DOCKER_NO_CACHE=true
            ;;
        -p|--pull)
            DOCKER_PULL=true
            ;;
    esac
    shift # past argument or value
done

DOCKERFILE="$1"
if [[ "$DOCKERFILE" == "l10n" ]]; then
    DOCKER_TAG="${BRANCH_NAME}-${GIT_COMMIT}"
else
    DOCKER_TAG="${GIT_COMMIT}"
fi
FINAL_DOCKERFILE="${DOCKER_CTX}/Dockerfile-$DOCKERFILE"
DOCKER_IMAGE_TAG="${DOCKER_REPO}/bedrock_${DOCKERFILE}:${DOCKER_TAG}"

# generate the dockerfile
rm -f "$FINAL_DOCKERFILE"
cat "docker/dockerfiles/bedrock_$DOCKERFILE" | envsubst '$GIT_COMMIT' > "$FINAL_DOCKERFILE"

# build the docker image
docker build -t "$DOCKER_IMAGE_TAG" --pull="$DOCKER_PULL" --no-cache="$DOCKER_NO_CACHE" -f "$FINAL_DOCKERFILE" "$DOCKER_CTX"
