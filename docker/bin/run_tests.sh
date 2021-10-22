#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#
# Runs unit_tests
#
set -exo pipefail

source docker/bin/set_git_env_vars.sh

exec docker-compose run test-image
