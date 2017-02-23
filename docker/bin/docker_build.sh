#!/bin/bash

set -exo pipefail

if [[ -z "$GIT_COMMIT" ]]; then
  export GIT_COMMIT=$(git rev-parse HEAD)
fi

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
FINAL_DOCKERFILE="${DOCKER_CTX}/Dockerfile-$DOCKERFILE"
DOCKER_IMAGE_TAG="${DOCKER_REPO}/bedrock_${DOCKERFILE}:${GIT_COMMIT}"

# generate the dockerfile
rm -f "$FINAL_DOCKERFILE"
cat "docker/dockerfiles/bedrock_$DOCKERFILE" | envsubst '$GIT_COMMIT' > "$FINAL_DOCKERFILE"

# build the docker image
docker build -t "$DOCKER_IMAGE_TAG" --pull="$DOCKER_PULL" --no-cache="$DOCKER_NO_CACHE" -f "$FINAL_DOCKERFILE" "$DOCKER_CTX"
