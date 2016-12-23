#!/bin/bash
set -ex

make clean
echo "ENV GIT_SHA ${CIRCLE_SHA1}" >> docker/dockerfiles/bedrock_dev_final
make build-final
