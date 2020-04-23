#!/bin/bash

set -exo pipefail

# look for skip string in the commit message
if echo "$CI_COMMIT_MESSAGE" | grep -F "[skip l10n]"; then
    echo "Skipping Fluent repo pull-request"
    exit 0
fi

source docker/bin/set_git_env_vars.sh

docker run --rm \
    -e FLUENT_REPO_AUTH \
    -e FLUENT_L10N_TEAM_REPO \
    "$DEPLOYMENT_DOCKER_IMAGE" \
    python manage.py open_ftl_pr
