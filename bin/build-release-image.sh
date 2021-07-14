#!/bin/bash
set -ex

source docker/bin/set_git_env_vars.sh

#if docker pull "$DEPLOYMENT_DOCKER_IMAGE"; then
#    echo "image already exists, skipping the build"
#else
#    make clean build-ci
#fi

# just build it, skip checking
make clean build-ci

# push and tag images
# we have to do this even if we didn't build a new image so that
# the latest and git-tag tags are pushed
if [[ "$1" == "--push" ]]; then
    docker/bin/push2dockerhub.sh mozmeao/bedrock_test
    docker/bin/push2dockerhub.sh mozmeao/bedrock_assets
    docker/bin/push2dockerhub.sh mozmeao/bedrock_code
    docker/bin/push2dockerhub.sh mozmeao/bedrock_build
    docker/bin/push2dockerhub.sh mozmeao/bedrock
fi
