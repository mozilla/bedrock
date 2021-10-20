#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -ex

source docker/bin/set_git_env_vars.sh

if docker pull "$DEPLOYMENT_DOCKER_IMAGE"; then
    echo "image already exists, skipping the build"
else
    make clean build-ci
fi

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
