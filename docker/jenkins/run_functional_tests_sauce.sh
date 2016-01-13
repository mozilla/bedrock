#!/bin/bash -xe
cp docker/dockerfiles/bedrock_functional_tests Dockerfile
docker build -t bedrock_functional_tests:${GIT_COMMIT} --pull=true .
docker run -v `pwd`/results:/app/results \
  -e BASE_URL=${BASE_URL} \
  -e DRIVER=SauceLabs \
  -e SAUCELABS_USERNAME=${SAUCELABS_USERNAME} \
  -e SAUCELABS_API_KEY=${SAUCELABS_API_KEY} \
  -e BROWSER_NAME="${BROWSER_NAME}" \
  -e BROWSER_VERSION=${BROWSER_VERSION} \
  -e PLATFORM="${PLATFORM}" \
  -e SELENIUM_VERSION=${SELENIUM_VERSION} \
  -e BUILD_TAG=${BUILD_TAG} \
  -e SCREEN_RESOLUTION=${SCREEN_RESOLUTION} \
  -e MARK_EXPRESSION="${MARK_EXPRESSION}" \
  bedrock_functional_tests:${GIT_COMMIT}
