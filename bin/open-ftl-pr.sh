#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
    -e FLUENT_L10N_TEAM_REPO_BRANCH \
    "$DEPLOYMENT_DOCKER_IMAGE" \
    python manage.py open_ftl_pr
