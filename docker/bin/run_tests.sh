#!/bin/bash
#
# Runs unit_tests
#
set -exo pipefail

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

TEST_IMAGE_TAG="mozorg/bedrock_test:${GIT_COMMIT}"
docker run --env-file docker/envfiles/test.env "$TEST_IMAGE_TAG"
