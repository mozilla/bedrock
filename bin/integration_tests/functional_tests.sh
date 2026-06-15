#!/usr/bin/env bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -euo pipefail

if [ -z "${BASE_URL:-}" ];
then
    echo "No BASE_URL set, exiting"
    exit 0;
fi

docker pull ${TEST_IMAGE}

docker run \
    --name "bedrock-${CI_JOB_ID}" \
    -e "MARK_EXPRESSION=${MARK_EXPRESSION:-}" \
    -e "BASE_URL=${BASE_URL:-}" \
    -e "PYTEST_PROCESSES=${PYTEST_PROCESSES:=4}" \
    -e "BOUNCER_URL=${BOUNCER_URL:=https://download.mozilla.org/}" \
    -e "RERUNS_ALLOWED=${RERUNS_ALLOWED:=2}" \
    -e "RERUNS_DELAY_SECS=${RERUNS_DELAY_SECS:=1}" \
    ${TEST_IMAGE} bin/integration_tests/run_integration_tests.sh
