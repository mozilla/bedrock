#!/bin/bash
set -ex

source docker/bin/set_git_env_vars.sh

if docker pull "$DEPLOYMENT_DOCKER_IMAGE"; then
    # image already exists, skip the build
    exit 0
fi

make clean build-ci

if [[ "$1" == "--push" ]]; then
    docker/bin/push2dockerhub.sh mozmeao/bedrock_test
    docker/bin/push2dockerhub.sh mozmeao/bedrock_assets
    docker/bin/push2dockerhub.sh mozmeao/bedrock_code
    docker/bin/push2dockerhub.sh mozmeao/bedrock_build
    docker/bin/push2dockerhub.sh mozmeao/bedrock
fi
