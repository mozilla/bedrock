#!/bin/bash -xe
GIT_COMMIT=${GIT_COMMIT:-$(git rev-parse HEAD)}
docker build -t bedrock_linkchecker:${GIT_COMMIT} --pull=true -f docker/dockerfiles/bedrock_linkchecker .
docker run --rm -v `pwd`/results:/results -e URLS="${URLS}" -e THREADS=${THREADS} -e RECURSION_LEVEL=${RECURSION_LEVEL} -e CHECK_EXTERNAL=${CHECK_EXTERNAL} -e VERBOSE=${VERBOSE} bedrock_linkchecker:${GIT_COMMIT}
