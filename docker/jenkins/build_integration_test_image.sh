#!/bin/bash -xe
docker build -t bedrock_integration_tests:${GIT_COMMIT} -f docker/dockerfiles/bedrock_integration_tests --pull=true .
