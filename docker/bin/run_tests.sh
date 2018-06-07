#!/bin/bash
#
# Runs unit_tests
#
set -exo pipefail

source docker/bin/set_git_env_vars.sh

exec docker-compose run test-image
