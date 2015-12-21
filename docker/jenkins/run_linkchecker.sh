#!/bin/bash -xe
cp docker/dockerfiles/bedrock_linkchecker Dockerfile
docker build -t bedrock_linkchecker:${GIT_COMMIT} --pull=true .
docker run -v `pwd`/results:/results -e URLS="${URLS}" -e THREADS=${THREADS} -e RECURSION_LEVEL=${RECURSION_LEVEL} -e CHECK_EXTERNAL=${CHECK_EXTERNAL} -e VERBOSE=${VERBOSE} bedrock_linkchecker:${GIT_COMMIT}
