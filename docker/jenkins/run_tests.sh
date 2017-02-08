#!/bin/bash
#
# Runs unit_tests
#
set -exo pipefail

if [[ -z "$GIT_COMMIT" ]]; then
  GIT_COMMIT=$(git rev-parse HEAD)
fi

TEST_IMAGE_TAG="mozorg/bedrock_test:${GIT_COMMIT}"
docker run --env-file docker/test.env "$TEST_IMAGE_TAG"
