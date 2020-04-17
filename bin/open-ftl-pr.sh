#!/bin/bash

set -exo pipefail

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

docker run --rm \
    -e FLUENT_REPO_AUTH \
    -e FLUENT_L10N_TEAM_REPO \
    "$DEPLOYMENT_DOCKER_IMAGE" \
    python manage.py open_ftl_pr
