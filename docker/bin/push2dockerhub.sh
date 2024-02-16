#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

FROM_DOCKER_REPOSITORY="$1"
IMG_TO_PUSH="$FROM_DOCKER_REPOSITORY:${GIT_COMMIT}"

if docker pull $IMG_TO_PUSH; then
    echo "image already exists, skipping the push"
else
    # Push to docker hub
    docker push "$IMG_TO_PUSH"
fi

if [[ "$BRANCH_NAME" == "main" ]]; then
    docker tag $IMG_TO_PUSH $FROM_DOCKER_REPOSITORY:latest
    docker push $FROM_DOCKER_REPOSITORY:latest
fi

if [[ "$BRANCH_NAME" == "prod" ]]; then
    docker tag $IMG_TO_PUSH $FROM_DOCKER_REPOSITORY:prod-latest
    docker push $FROM_DOCKER_REPOSITORY:prod-latest
fi

if [[ "$GIT_TAG_DATE_BASED" == true ]]; then
    docker tag $IMG_TO_PUSH $FROM_DOCKER_REPOSITORY:$GIT_TAG
    docker push $FROM_DOCKER_REPOSITORY:$GIT_TAG
fi
