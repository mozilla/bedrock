#!/bin/bash

set -exo pipefail

# look for skip string in the commit message
if git log -1 --pretty=%B | grep "\[skip l10n\]"; then
    echo "Skipping Fluent repo pull-request"
    exit 0
fi

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

docker run --rm \
    -e FLUENT_REPO_AUTH \
    -e FLUENT_L10N_TEAM_REPO \
    "$DEPLOYMENT_DOCKER_IMAGE" \
    python manage.py open_ftl_pr
